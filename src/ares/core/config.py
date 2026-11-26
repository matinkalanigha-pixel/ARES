from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    name: str = "A.R.E.S."
    data_dir: Path = Path("data")
    database_name: str = "ares.sqlite3"
    log_level: str = "INFO"
    log_file: Path = Path("ares.log")
    conversation_enabled: bool = True
    knowledge_enabled: bool = True
    experience_enabled: bool = True
    skill_enabled: bool = True
    user_context_enabled: bool = True
    allow_network: bool = False
    allow_shell: bool = False
    allow_file_analysis: bool = True
    allow_autonomous_tasks: bool = False
    retention_days: int = 365



def load_settings(config_path: str | os.PathLike[str] | None = None) -> Settings:
    """Load settings using Python's standard-library TOML parser."""
    import tomllib

    path = Path(config_path) if config_path else Path("config/default.toml")
    if not path.is_absolute():
        path = Path.cwd() / path

    values: dict = {}
    if path.exists():
        with path.open("rb") as handle:
            values = tomllib.load(handle)

    system = values.get("system", {})
    logging_cfg = values.get("logging", {})
    memory = values.get("memory", {})
    security = values.get("security", {})

    data_dir = Path(system.get("data_dir", "data"))
    if not data_dir.is_absolute():
        data_dir = Path.cwd() / data_dir

    log_file = Path(logging_cfg.get("file", "ares.log"))
    if not log_file.is_absolute():
        log_file = Path.cwd() / log_file

    return Settings(
        name=system.get("name", "A.R.E.S."),
        data_dir=data_dir,
        database_name=system.get("database_name", "ares.sqlite3"),
        log_level=logging_cfg.get("level", "INFO"),
        log_file=log_file,
        conversation_enabled=memory.get("conversation_enabled", True),
        knowledge_enabled=memory.get("knowledge_enabled", True),
        experience_enabled=memory.get("experience_enabled", True),
        skill_enabled=memory.get("skill_enabled", True),
        user_context_enabled=memory.get("user_context_enabled", True),
        allow_network=security.get("allow_network", False),
        allow_shell=security.get("allow_shell", False),
        allow_file_analysis=security.get("allow_file_analysis", True),
        allow_autonomous_tasks=security.get("allow_autonomous_tasks", False),
        retention_days=memory.get("retention_days", 365),
    )
