from slack_assistant import main as main_module


def test_main_registers_app_and_starts_socket_handler(monkeypatch):
    calls = {}

    class FakeApp:
        def __init__(self, token):
            calls["app_token"] = token

    class FakeSocketModeHandler:
        def __init__(self, app, token):
            calls["handler"] = (app, token)

        def start(self):
            calls["started"] = True

    monkeypatch.setattr(main_module, "App", FakeApp)
    monkeypatch.setattr(main_module, "SocketModeHandler", FakeSocketModeHandler)
    monkeypatch.setattr(
        main_module,
        "register_handlers",
        lambda app: calls.update(registered_app=app),
    )

    main_module.main()

    assert calls["app_token"] == main_module.settings.slack_bot_token
    assert calls["handler"][1] == main_module.settings.slack_app_token
    assert calls["handler"][0] is calls["registered_app"]
    assert calls["started"] is True