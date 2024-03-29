import asyncio
import base64
import datetime
import json
import os
from typing import Optional

import aiohttp
import requests

from config import Config
from db import get_food_protocols_by_id


async def get_dish_receipt(dish_description: str):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {Config.API_SECRET}"
    }
    prompt = {
        "modelUri": f"gpt://{Config.CATALOG_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"Ты повар, который формирует подробные рецепты блюд. Нужно составить подробный рецепт для "
                        f"приготовления {dish_description} с указанием ингридиентов. "
            },
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=prompt) as response:
            result = await response.json()

    return result['result']['alternatives'][0]['message']['text']


async def make_gpt_request(food_protocol_id, allergic: Optional[str]):
    food_data = await get_food_protocols_by_id(food_protocol_id)
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
                "text": "Ты диетолог, который будет составлять меню на каждый день недели. Нужно составить меню на завтрак, обед и ужин на каждый день недели." +
                        (f"Нужно учесть аллергию клиента на {allergic}" if allergic is not None else "") +
                        f"Вот список разрешенных продуктов: {allowed}. И список запрещенных продуктов:{not_allowed}"
            },
            {
                "role": "user",
                "text": (
                    "Пожалуйста, расписывайте каждое блюдо подробно, напитки упоминать не нужно. "
                )
            },
            {
                "role": "assistant",
                "text": (
                        "Понедельник.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Вторник.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Среда.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Четверг.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Пятница.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Суббота.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]\n\n"
                        "Воскресенье.\n" +
                        "Завтрак: [Тут описание блюда на завтрак и ингридиенты]\n" +
                        "Обед: [Тут описание блюда на обед и ингридиенты]\n" +
                        "Ужин: [Тут описание блюда на ужин и ингридиенты]"
                )
            },
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=prompt) as response:
            result = await response.json()

    return result['result']['alternatives'][0]['message']['text']


async def execute_fusion_api(client_name, description):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', Config.FUSION_KEY, Config.FUSION_SECRET)
    model_id = await api.get_model()
    descriptions = await api.prepare_descriptions(description)
    image_paths = []
    day_counter = 1
    dish_counter = 0
    if descriptions:
        for desc in descriptions:
            dish_counter += 1
            if dish_counter == 4:
                dish_counter = 1
                day_counter += 1
            uuid = await api.generate(desc, model_id)
            images = await api.check_generation(uuid)
            path = await api.save_images(images, client_name, f"{day_counter}_{dish_counter}")
            image_paths.append(path)
    return image_paths


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) as response:
                data = await response.json()
                return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
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

    async def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.URL + 'key/api/v1/text2image/status/' + request_id,
                                       headers=self.AUTH_HEADERS) as response:
                    data = await response.json()
                    if data['status'] == 'DONE':
                        return data['images']
            attempts -= 1
            await asyncio.sleep(delay)

    async def save_images(self, images, client_name, img_name):
        cur_date = datetime.date.today()
        if images:
            for idx, img_data in enumerate(images):
                binary_data = base64.b64decode(img_data)
                os.makedirs(os.path.join(Config.IMAGES_PATH, client_name, str(cur_date)), exist_ok=True)
                img_path = os.path.join(Config.IMAGES_PATH, client_name, str(cur_date), img_name + '.jpg')
                with open(img_path, 'wb') as file:
                    file.write(binary_data)
            return img_path

    async def prepare_descriptions(self, description):
        filtered_list = [item for item in description.split('\n') if item != ""]
        filtered_list = [item for item in filtered_list if
                         not any(
                             day in item for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
                                                     'Воскресенье'])]
        filtered_list = [item for item in filtered_list if
                         any(keyword in item for keyword in ['Завтрак', 'Обед', 'Ужин'])]
        return filtered_list


async def remove_all_files_and_folders(path):
    os.remove(Config.ZIP_PATH)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
