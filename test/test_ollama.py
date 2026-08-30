from slack_assistant.clients import ollama as ollama_module


def test_generate_sends_question_and_context(monkeypatch):
    calls = {}

    class FakeClient:
        def chat(self, **kwargs):
            calls.update(kwargs)
            return {"message": {"content": "answer"}}

    monkeypatch.setattr(ollama_module.ollama, "Client", lambda host: FakeClient())
    client = ollama_module.OllamaClient()

    assert client.generate("question", "context") == "answer"
    assert calls["model"] == ollama_module.settings.ollama_model
    assert calls["messages"] == [{
        "role": "user",
        "content": "question\n\nContext: context",
    }]
    assert calls["keep_alive"] == -1


def test_generate_omits_empty_context(monkeypatch):
    class FakeClient:
        def chat(self, **kwargs):
            return {"message": {"content": kwargs["messages"][0]["content"]}}

    monkeypatch.setattr(ollama_module.ollama, "Client", lambda host: FakeClient())

    assert ollama_module.OllamaClient().generate("question", "") == "question"