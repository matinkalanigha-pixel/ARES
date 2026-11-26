from __future__ import annotations

import re


INTENT_PATTERNS = {
    "help": (r"\b(help|راهنما|کمک)\b", "help"),
    "memory": (r"\b(memory|حافظه|ذخیره|remember)\b", "memory"),
    "status": (r"\b(status|وضعیت|what.+can)\b", "status"),
    "research": (r"\b(research|investigate|پژوهش|تحقیق)\b", "research"),
    "market": (r"\b(market|stock|crypto|بازار|سهام)\b", "market"),
    "limitations": (r"\b(limit|limitations|محدودیت|cannot|نمی.?توان)\b", "limitations"),
}


def detect_intent(text: str) -> str:
    normalized = text.lower().strip()
    for intent, (pattern, _label) in INTENT_PATTERNS.items():
        if re.search(pattern, normalized, re.IGNORECASE):
            return intent
    return "general"


def generate_response(text: str, intent: str) -> str:
    if intent == "help":
        return "Type /help to see available commands. Free-text responses are currently rule-based."
    if intent == "memory":
        return "Memory is stored locally in SQLite. Use /memory to inspect recent messages."
    if intent == "status":
        return "A.R.E.S. is running locally. Phase 1 provides storage and a terminal interface."
    if intent == "research":
        return "The research engine is planned for a later phase and is not active in Phase 1."
    if intent == "market":
        return "Market analysis is planned for a later phase. No financial advice or prediction is provided."
    if intent == "limitations":
        return "A.R.E.S. uses rule-based processing and does not use pretrained language models. Its language understanding is intentionally limited."
    return "Message received and stored. In Phase 1, I can track conversations but cannot yet perform the requested research or analysis."
