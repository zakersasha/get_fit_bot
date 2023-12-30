import aiohttp

from config import Config


async def make_gpt_request(food_protocol_id, allergic):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        # "Authorization": f"Bearer {IAM_token}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{Config.CATALOG_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — опытный копирайтер. Напиши маркетинговый текст с учётом вида текста и заданной темы."
            },
            {
                "role": "user",
                "text": "Вид текста: пост в телеграмме. Тема: преимущества YandexGPT в копирайтинге."
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return None
