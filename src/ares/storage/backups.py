from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


class BackupManager:
    def __init__(self, database, backup_dir: str | Path) -> None:
        self.database = database
        self.backup_dir = Path(backup_dir)

    def create_backup(self) -> Path:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = self.backup_dir / f"ares-{timestamp}.sqlite3"
        return self.database.backup(target)
