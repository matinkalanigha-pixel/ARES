from __future__ import annotations

import sqlite3


class ConversationMemory:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def new_conversation(self, title: str = "Terminal conversation") -> int:
        cursor = self.connection.execute(
            "INSERT INTO conversations(title) VALUES (?)",
            (title,),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def add_message(
        self,
        conversation_id: int,
        role: str,
        text: str,
        intent: str | None = None,
    ) -> int:
        if role not in {"user", "assistant", "system"}:
            raise ValueError("Invalid message role")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Message text cannot be empty")

        cursor = self.connection.execute(
            """
            INSERT INTO messages(conversation_id, role, text, intent)
            VALUES (?, ?, ?, ?)
            """,
            (conversation_id, role, text.strip(), intent),
        )
        self.connection.execute(
            "UPDATE conversations SET updated_at=datetime('now') WHERE id=?",
            (conversation_id,),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_messages(self, limit: int = 20) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT c.id AS conversation_id, c.title, m.role, m.text,
                   m.intent, m.created_at
            FROM messages m
            JOIN conversations c ON c.id = m.conversation_id
            ORDER BY m.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def add_feedback(self, text: str) -> int:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Feedback cannot be empty")
        cursor = self.connection.execute(
            "INSERT INTO feedback(text) VALUES (?)",
            (text.strip(),),
        )
        self.connection.commit()
        return int(cursor.lastrowid)
