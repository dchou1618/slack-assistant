import ollama
from slack_assistant.config import settings

class OllamaClient:
    def __init__(self):
        self.client = ollama.Client(
            host=settings.ollama_host
        )
    def generate(self, question: str, context: str) -> str:
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
        return response["message"]["content"]