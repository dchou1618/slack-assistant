import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import ollama
from bs4 import BeautifulSoup
import requests

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

def process_files(event, say) -> str:
    for file in event.get("files", []):
        file_name = file.get("name")
        file_url = file.get("url_private")
        try:
            headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
            response = requests.get(file_url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                say("Failed to securely download the file.")
                continue

            extracted_text = ""
            file_bytes = response.content
            if file_name.endswith((".txt", ".md")):
                extracted_text = file_bytes.decode("utf-8")
            elif file_name.endswith(".pdf"):
                from PyPDF2 import PdfReader
                pdf_reader = PdfReader(file_bytes)
                extracted_text = "\n".join(page.extract_text() for page in pdf_reader.pages)
            elif file_name.endswith(".docx"):
                from docx import Document
                from io import BytesIO
                doc = Document(BytesIO(file_bytes))
                extracted_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            elif file_name.endswith(".html"):
                soup = BeautifulSoup(file_bytes, "html.parser")
                extracted_text = soup.get_text()
            else:
                say(f"Unsupported file type: {file_name}")
                continue
        except Exception as e:
            print(f"Error processing file: {e}")
            say(f"An error occurred while analyzing the document.")
    return extracted_text


@app.event("app_mention")
def handle_mention(event, say, client):
    question = event["text"]
    file_txt = process_files(event, say)

    slack_response = say("🧠 Thinking...")

    ollama_response = ollama.chat(
        model="mistral-small3.1",
        messages=[
            {
                "role": "user",
                "content": f"{question}\n\nContext: {file_txt}",
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