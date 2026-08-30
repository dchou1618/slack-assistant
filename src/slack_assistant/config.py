import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Settings:
    slack_bot_token: str = os.environ["SLACK_BOT_TOKEN"]
    slack_app_token: str = os.environ["SLACK_APP_TOKEN"]

    ollama_host: str = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    ollama_model: str = os.getenv(
        "OLLAMA_MODEL",
        "mistral-small3.1",
    )


settings = Settings()