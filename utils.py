import base64
import datetime
import json
import os
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
            "temperature": 0.3,
            "maxTokens": "6000"
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
                        f"Вот список разрешенных продуктов: {allowed}. И список запрещенных продуктов:{not_allowed}. Пожалуйста, расписывайте каждое блюдо подробно, напитки упоминать не нужно. "
                )
            },
            {
                "role": "assistant",
                "text": (
                        "Понедельник.\n" +
                        "Завтрак: Омлет на растительном молоке с овощами и зеленью.\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Вторник.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Среда.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Четверг.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Пятница.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Суббота.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]\n\n"
                        "Воскресенье.\n" +
                        "Завтрак: [Тут описание блюда на завтрак]\n" +
                        "Обед: [Тут описание блюда на обед]\n" +
                        "Ужин: [Тут описание блюда на ужин]"
                )
            },
        ]
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()

    return result['result']['alternatives'][0]['message']['text']


def execute_fusion_api(client_name, description):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', Config.FUSION_KEY, Config.FUSION_SECRET)
    model_id = api.get_model()
    descriptions = api.prepare_descriptions(description)
    image_paths = []
    if descriptions:
        for desc in descriptions:
            uuid = api.generate(desc, model_id)
            images = api.check_generation(uuid)
            path = api.save_images(images, client_name)
            image_paths.append(path)
    return image_paths


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
                os.makedirs(os.path.join(Config.IMAGES_PATH, client_name, str(cur_date)), exist_ok=True)
                img_path = os.path.join(Config.IMAGES_PATH, client_name, str(cur_date), str(generated_uuid)) + '.jpg'
                with open(img_path, 'wb') as file:
                    file.write(binary_data)
            return img_path

    def prepare_descriptions(self, description):
        filtered_list = [item for item in description.split('\n') if item != ""]
        filtered_list = [item for item in filtered_list if
                         not any(
                             day in item for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
                                                     'Воскресенье'])]
        filtered_list = [item for item in filtered_list if
                         any(keyword in item for keyword in ['Завтрак', 'Обед', 'Ужин'])]
        return filtered_list
