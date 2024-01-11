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
            "maxTokens": "8000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты диетолог, который будет составлять меню на каждый день недели."
            },
            {
                "role": "user",
                "text": (
                        "Мне нужно составить меню на завтрак, обед и ужин на каждый день недели." +
                        (f"Нужно учесть аллергию клиента на {allergic}" if allergic is not None else "") +
                        f"Вот список разрешенных продуктов: {allowed}. И список запрещенных продуктов:{not_allowed}. Пожалуйста, расписывайте каждое блюдо подробно, включая ингредиенты, напитки упоминать не нужно. "
                )
            },
            {
                "role": "assistant",
                "text": (
                        "Понедельник.\n" +
                        "Завтрак: Омлет на растительном молоке с овощами и зеленью.\n" +
                        "Ингредиенты: 3 яйца, 1 стакан растительного молока, 1/2 кабачка, 2 соцветия цветной капусты, 5 листьев зелени (укроп, петрушка, базилик).\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Вторник.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Среда.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Четверг.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Пятница.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Суббота.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]\n\n"
                        "Воскресенье.\n" +
                        "Завтрак: [Тут описание завтрака и ингридиентов для приготовления]\n" +
                        "Обед: [Тут описание обеда и ингридиентов для приготовления]\n" +
                        "Ужин: [Тут описание ужина и ингридиентов для приготовления]"
                )
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
