import threading

from slack_assistant.clients.ollama import OllamaClient
from slack_assistant.utils.file_processing import process_files


llm = OllamaClient()
THINKING_PHRASES = (
    "Thinking",
    "Pontificating",
    "Pondering",
    "Connecting the dots",
)
THINKING_SPINNER = ("◐", "◓", "◑", "◒")
THINKING_INTERVAL = 1.5


def _animate_thinking(client, channel, timestamp, stop_event):
    phrase_index = 0
    while not stop_event.wait(THINKING_INTERVAL):
        phrase = THINKING_PHRASES[phrase_index % len(THINKING_PHRASES)]
        spinner = THINKING_SPINNER[phrase_index % len(THINKING_SPINNER)]
        client.chat_update(
            channel=channel,
            ts=timestamp,
            text=f"{spinner} {phrase}...",
        )
        phrase_index += 1

def register_handlers(app):
    @app.event("app_mention")
    def handle_mention(event, say, client):
        question = event["text"]
        file_txt = process_files(event, say)

        slack_response = say(f"{THINKING_SPINNER[0]} Thinking...")
        stop_animation = threading.Event()
        animation = threading.Thread(
            target=_animate_thinking,
            args=(client, event["channel"], slack_response["ts"], stop_animation),
            daemon=True,
        )
        animation.start()

        try:
            answer = llm.generate(question, file_txt)
        finally:
            stop_animation.set()
            animation.join()

        client.chat_update(
            channel=event["channel"],
            ts=slack_response["ts"],
            text=answer,
        )