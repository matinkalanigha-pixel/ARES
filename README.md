# A.R.E.S.

A.R.E.S. (**Autonomous Research & Evolving System**) is a local, modular research and analysis platform. It does **not** use pretrained language models, LLM APIs, or model runtimes.

## Implemented in Phase 1

- Local SQLite storage
- Conversational memory
- TOML configuration
- Logging
- Terminal CLI
- `/help`, `/status`, `/memory`, `/feedback`, `/quit`
- Database migrations and backups
- Basic intent detection
- User preference storage
- Unit and integration tests

## Requirements

- Ubuntu Linux
- Python 3.11 or newer

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e '.[dev]'  # for tests
```

## Run

```bash
python -m ares
```

Or, after installation:

```bash
ares
```

## Test

```bash
pytest -q
```

## CLI commands

- `/help` — list commands
- `/status` — show system status
- `/memory` — inspect stored conversations
- `/feedback <text>` — record feedback
- `/quit` — stop A.R.E.S.

Free-form text is stored as a conversation turn and receives a rule-based, low-overconfidence response.
