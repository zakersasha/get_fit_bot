import base64
import datetime
import json
import os
import re
import time
import uuid

import requests

from config import Config
from db import get_food_protocols_by_id


def make_gpt_request(food_protocol_id, allergic):
    food_data = get_food_protocols_by_id(food_protocol_id)
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {Config.API_SECRET}"
    }
    not_allowed = food_data['not_allowed'].replace('\n', '')
    allowed = food_data['allowed'].replace('\n', '')
    prompt = {
        "modelUri": f"gpt://{Config.CATALOG_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "4000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты диетолог, который будет составлять меню на каждый день недели."
            },
            {
                "role": "user",
                "text": ("Мне нужно составить меню из 3-х блюд и перекуса на каждый день недели для человека" +
                         (f" с аллергией на {allergic}" if allergic is not None else "") +
                         ". У меня есть список разрешенных и запрещенных продуктов.")
            },
            {
                "role": "assistant",
                "text": "Поняла. Пожалуйста, предоставьте мне список разрешенных продуктов, которые можно "
                        "использовать для приготовления блюд."
            },
            {
                "role": "user",
                "text": f"Список разрешенных продуктов: {allowed}"
            },
            {
                "role": "assistant",
                "text": "Спасибо. А теперь, пожалуйста, укажите список запрещенных продуктов, чтобы исключить их из "
                        "блюд. "
            },
            {
                "role": "user",
                "text": f"Список запрещенных продуктов:{not_allowed}"
            },
        ]
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    image_descriptions = result['result']['alternatives'][0]['message']['text'].split("\n")

    return result['result']['alternatives'][0]['message']['text'], image_descriptions


def execute_fusion_api(client_name, description):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', Config.FUSION_KEY, Config.FUSION_SECRET)
    model_id = api.get_model()
    descriptions = api.prepare_descriptions(description)
    if descriptions:
        for desc in descriptions:
            uuid = api.generate(desc, model_id)
            images = api.check_generation(uuid)
            api.save_images(images, client_name)


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url

        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models',
                                headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run',
                                 headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' +
                                    request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)

    def save_images(self, images, client_name):
        cur_date = datetime.date.today()
        if images:
            for idx, img_data in enumerate(images):
                binary_data = base64.b64decode(img_data)
                generated_uuid = uuid.uuid4()
                os.makedirs(f'images/{client_name}/{cur_date}', exist_ok=True)
                with open(f'images/{client_name}/{cur_date}/{generated_uuid}.jpg', 'wb') as file:
                    file.write(binary_data)

    def prepare_descriptions(self, description):
        prepared_response = list(filter(None, description))
        try:
            monday_menu = prepared_response[prepared_response.index('Понедельник:') + 1]
            tuesday_menu = prepared_response[prepared_response.index('Вторник:') + 1]
            wednesday_menu = prepared_response[prepared_response.index('Среда:') + 1]
            thursday_menu = prepared_response[prepared_response.index('Четверг:') + 1]
            friday_menu = prepared_response[prepared_response.index('Пятница:') + 1]
            saturday_menu = prepared_response[prepared_response.index('Суббота:') + 1]
            sunday_menu = prepared_response[prepared_response.index('Воскресенье:') + 1]
        except ValueError:
            try:
                monday_menu = prepared_response[prepared_response.index('Понедельник') + 1]
                tuesday_menu = prepared_response[prepared_response.index('Вторник') + 1]
                wednesday_menu = prepared_response[prepared_response.index('Среда') + 1]
                thursday_menu = prepared_response[prepared_response.index('Четверг') + 1]
                friday_menu = prepared_response[prepared_response.index('Пятница') + 1]
                saturday_menu = prepared_response[prepared_response.index('Суббота') + 1]
                sunday_menu = prepared_response[prepared_response.index('Воскресенье') + 1]
            except ValueError:
                return None
        monday_meals = re.findall(r'\: (.*?)\.', monday_menu)
        tuesday_meals = re.findall(r'\: (.*?)\.', tuesday_menu)
        wednesday_meals = re.findall(r'\: (.*?)\.', wednesday_menu)
        thursday_meals = re.findall(r'\: (.*?)\.', thursday_menu)
        friday_meals = re.findall(r'\: (.*?)\.', friday_menu)
        saturday_meals = re.findall(r'\: (.*?)\.', saturday_menu)
        sunday_meals = re.findall(r'\: (.*?)\.', sunday_menu)

        week_meals = monday_meals + tuesday_meals + wednesday_meals + \
                     thursday_meals + friday_meals + saturday_meals + sunday_meals

        return week_meals
