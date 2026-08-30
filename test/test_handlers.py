from slack_assistant import handlers


def test_register_handlers_processes_mention(monkeypatch):
    registered = {}

    class FakeApp:
        def event(self, event_name):
            def decorator(handler):
                registered[event_name] = handler
                return handler

            return decorator

    say_calls = []
    update_calls = []
    monkeypatch.setattr(handlers, "process_files", lambda event, say: "file text")
    monkeypatch.setattr(handlers.llm, "generate", lambda question, context: "answer")
    handlers.register_handlers(FakeApp())

    event = {"text": "question", "channel": "C123"}
    response = registered["app_mention"](
        event,
        lambda message: say_calls.append(message) or {"ts": "123.456"},
        type("Client", (), {"chat_update": lambda self, **kwargs: update_calls.append(kwargs)})(),
    )

    assert response is None
    assert say_calls == ["🧠 Thinking..."]
    assert update_calls == [{"channel": "C123", "ts": "123.456", "text": "answer"}]