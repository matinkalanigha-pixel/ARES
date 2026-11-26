import tempfile

from ares.storage.database import Database


def test_database_migration_creates_tables():
    with tempfile.TemporaryDirectory() as directory:
        database = Database(f"{directory}/test.sqlite3")
        database.migrate()

        tables = {
            row[0]
            for row in database.connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        assert "conversations" in tables
        assert "messages" in tables
        assert "preferences" in tables
        assert "feedback" in tables
        database.close()
