import os
import openai
from config import settings

# os.environ["https_proxy"] = "http://ZEKgZw:dKkhVk@181.177.87.132:9387"


client = openai.OpenAI(
    base_url="https://api.proxyapi.ru/openai/v1",
)

chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": "Привет"}],
)

        # Получаем ответ от нейросети
response_content = chat_completion.choices[0].message.content
print(response_content)