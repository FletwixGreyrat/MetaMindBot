from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



TOKEN = getenv("bot_token")
openai_api_token = getenv("openai_key")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")


class DataBaseSettings():
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class OpenAISettings():
    token: str = openai_api_token


class BotSettings():
    token: str = TOKEN


class Settings():
    bot: BotSettings = BotSettings()
    openai: OpenAISettings = OpenAISettings()
    db: DataBaseSettings = DataBaseSettings()


settings = Settings()