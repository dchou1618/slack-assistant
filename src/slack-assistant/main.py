import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import ollama

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say, client):
    question = event["text"]

    slack_response = say("🧠 Thinking...")

    ollama_response = ollama.chat(
        model="mistral-small3.1",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        keep_alive=-1,
    )

    answer = ollama_response["message"]["content"]
    client.chat_update(
        channel=event["channel"],
        ts=slack_response["ts"],
        text=answer,
    )


if __name__ == "__main__":
    print("⚡️ Bolt app is running!")

    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"],
    )

    handler.start()