"""Unit tests for the question classifier.

A fake model stands in for the LLM. No network, no API key needed.
"""


class FakeReply:
    def __init__(self, content):
        self.content = content


class FakeLLM:
    def __init__(self, reply):
        self.reply = reply

    def invoke(self, messages):
        return FakeReply(self.reply)


from app import understand


def test_classifies_best_day():
    llm = FakeLLM("best_day")
    result = understand.classify_question(
        "what was our best day of the week?", llm=llm
    )
    assert result["type"] == "best_day"


def test_classifies_trend():
    llm = FakeLLM("trend")
    result = understand.classify_question(
        "is revenue going up over 30 days?", llm=llm
    )
    assert result["type"] == "trend"


def test_classifies_comparison():
    llm = FakeLLM("comparison")
    result = understand.classify_question(
        "how does this month compare to last month?", llm=llm
    )
    assert result["type"] == "comparison"


def test_unknown_reply_becomes_fallback():
    llm = FakeLLM("please ask something else")
    result = understand.classify_question("hello?", llm=llm)
    assert result["type"] == "fallback"


def test_empty_reply_becomes_fallback():
    llm = FakeLLM("")
    result = understand.classify_question("...", llm=llm)
    assert result["type"] == "fallback"


def test_crash_becomes_fallback():
    class BrokenLLM:
        def invoke(self, messages):
            raise RuntimeError("api down")

    result = understand.classify_question("anything", llm=BrokenLLM())
    assert result["type"] == "fallback"


def test_validate_handles_case_and_punctuation():
    assert understand._validate("Best_Day.") == "best_day"
    assert understand._validate(None) == "fallback"
