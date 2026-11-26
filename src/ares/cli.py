from __future__ import annotations

from pathlib import Path

from ares.core.config import Settings, load_settings
from ares.core.logging import configure_logging
from ares.conversation.engine import detect_intent, generate_response
from ares.memory.conversations import ConversationMemory
from ares.storage.database import Database


COMMANDS = {
    "/help": "Show available commands",
    "/status": "Show local system status",
    "/memory": "Inspect recent conversation messages",
    "/feedback": "Record feedback: /feedback <text>",
    "/quit": "Exit A.R.E.S.",
}


class AresApp:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        self.database = Database(settings.data_dir / settings.database_name)
        self.database.migrate()
        self.memory = ConversationMemory(self.database.connection)
        self.conversation_id = self.memory.new_conversation()
        self.logger = configure_logging(settings.log_level, settings.log_file)
        self.logger.info("A.R.E.S. Phase 1 started")

    def close(self) -> None:
        self.database.close()
        self.logger.info("A.R.E.S. stopped")

    def handle_command(self, text: str) -> tuple[str, bool]:
        stripped = text.strip()
        if not stripped:
            return "", False

        if stripped == "/quit":
            return "Goodbye.", True
        if stripped == "/help":
            lines = ["Available commands:"]
            lines.extend(f"  {command:<12} {description}" for command, description in COMMANDS.items())
            return "\n".join(lines), False
        if stripped == "/status":
            status = (
                "A.R.E.S. Phase 1\n"
                f"Database: {self.database.path}\n"
                "Conversation memory: " + ("enabled" if self.settings.conversation_enabled else "disabled") + "\n"
                "Network: disabled\n"
                "Shell execution: disabled"
            )
            return status, False
        if stripped == "/memory":
            messages = self.memory.list_messages(limit=20)
            if not messages:
                return "No stored messages.", False
            lines = []
            for message in messages:
                lines.append(f"[{message['created_at']}] {message['role']}: {message['text']}")
            return "\n".join(lines), False
        if stripped.startswith("/feedback"):
            parts = stripped.split(maxsplit=1)
            if len(parts) != 2:
                return "Usage: /feedback <text>", False
            self.memory.add_feedback(parts[1])
            return "Feedback stored locally.", False

        if not stripped.startswith("/"):
            intent = detect_intent(stripped)
            self.memory.add_message(self.conversation_id, "user", stripped, intent)
            response = generate_response(stripped, intent)
            self.memory.add_message(self.conversation_id, "assistant", response, intent)
            return response, False

        return "Unknown command. Type /help for available commands.", False


def main() -> None:
    settings = load_settings()
    app = AresApp(settings)
    print(f"{settings.name} — local terminal interface")
    print("Type /help for commands or /quit to exit.")

    try:
        while True:
            try:
                text = input("A.R.E.S.> ")
            except EOFError:
                break
            response, should_exit = app.handle_command(text)
            if response:
                print(response)
            if should_exit:
                break
    finally:
        app.close()


if __name__ == "__main__":
    main()
