import logging
import sys

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_assistant.handlers import register_handlers
from slack_assistant.config import settings


def configure_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
    )


def main():
    configure_logging()
    logging.getLogger(__name__).info("Starting Slack assistant")
    app = App(token=settings.slack_bot_token)

    register_handlers(app)

    handler = SocketModeHandler(
        app,
        settings.slack_app_token,
    )

    handler.start()

if __name__ == "__main__":
    main()