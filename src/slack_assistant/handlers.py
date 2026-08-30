from slack_assistant.clients.ollama import OllamaClient
from slack_assistant.utils.file_processing import process_files

llm = OllamaClient()

def register_handlers(app):
    @app.event("app_mention")
    def handle_mention(event, say, client):
        question = event["text"]
        file_txt = process_files(event, say)

        slack_response = say("🧠 Thinking...")

        answer = llm.generate(question, file_txt)
        client.chat_update(
            channel=event["channel"],
            ts=slack_response["ts"],
            text=answer,
        )