from slack_assistant.config import Settings, settings


def test_settings_values():
    configured = Settings(
        slack_bot_token="bot-token",
        slack_app_token="app-token",
        ollama_host="http://ollama.test",
        ollama_model="test-model",
    )

    assert configured.slack_bot_token == "bot-token"
    assert configured.slack_app_token == "app-token"
    assert configured.ollama_host == "http://ollama.test"
    assert configured.ollama_model == "test-model"
    assert settings.slack_bot_token == "test-bot-token"