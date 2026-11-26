from ares.core.config import Settings
from ares.cli import AresApp


def test_free_text_is_stored(tmp_path):
    settings = Settings(
        data_dir=tmp_path,
        database_name="test.sqlite3",
        log_file=tmp_path / "ares.log",
    )
    app = AresApp(settings)

    response, should_exit = app.handle_command("سلام، حالت چطور است؟")

    assert should_exit is False
    assert response
    messages = app.memory.list_messages()
    assert any(message["text"] == "سلام، حالت چطور است؟" for message in messages)
    app.close()


def test_help_command(tmp_path):
    settings = Settings(
        data_dir=tmp_path,
        database_name="test.sqlite3",
        log_file=tmp_path / "ares.log",
    )
    app = AresApp(settings)

    response, should_exit = app.handle_command("/help")

    assert should_exit is False
    assert "/status" in response
    app.close()
