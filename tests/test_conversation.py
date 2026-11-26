from ares.conversation.engine import detect_intent


def test_rule_based_intent_detection():
    assert detect_intent("Research Linux security") == "research"
    assert detect_intent("What is my memory") == "memory"
    assert detect_intent("What are your limitations") == "limitations"
