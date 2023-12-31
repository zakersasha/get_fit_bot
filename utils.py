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
    return result['result']['alternatives'][0]['message']['text']
