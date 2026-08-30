import logging
import time

import ollama
from slack_assistant.config import settings


logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self):
        self.client = ollama.Client(
            host=settings.ollama_host
        )

    def generate(self, question: str, context: str) -> str:
        started_at = time.monotonic()
        logger.info(
            "Starting Ollama inference model=%s host=%s context=%s",
            settings.ollama_model,
            settings.ollama_host,
            bool(context),
        )
        response = self.client.chat(
            model=settings.ollama_model,
            messages=[
                {
                    "role": "user",
                    "content": question + f"\n\nContext: {context}" if context else question,
                }
            ],
            keep_alive=-1,
        )
        answer = response["message"]["content"]
        logger.info(
            "Finished Ollama inference model=%s duration=%.2fs",
            settings.ollama_model,
            time.monotonic() - started_at,
        )
        return answer