from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_assistant.handlers import register_handlers
from slack_assistant.config import settings


def main():
    app = App(token=settings.slack_bot_token)

    register_handlers(app)

    handler = SocketModeHandler(
        app,
        settings.slack_app_token,
    )

    handler.start()

if __name__ == "__main__":
    main()