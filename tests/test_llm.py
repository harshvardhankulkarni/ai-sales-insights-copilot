"""Tests for the LLM failover chain in app/llm.py.

The chain must skip a failing slot, skip an empty reply, and return ""
when every slot fails. No network calls in these tests.
"""

from app.llm import first_reply, build_chain


class _FakeReply:
    def __init__(self, content):
        self.content = content


class _Raises:
    def invoke(self, prompt):
        raise RuntimeError("provider down")


class _Answers:
    def __init__(self, content):
        self._content = content

    def invoke(self, prompt):
        return _FakeReply(self._content)


class _Empty:
    def invoke(self, prompt):
        return _FakeReply("   ")


def test_returns_first_reply():
    chain = [_Answers("first"), _Answers("second")]
    assert first_reply("q", chain) == "first"


def test_skips_failing_slot():
    chain = [_Raises(), _Answers("second")]
    assert first_reply("q", chain) == "second"


def test_skips_empty_slot():
    chain = [_Empty(), _Answers("second")]
    assert first_reply("q", chain) == "second"


def test_all_fail_returns_empty():
    chain = [_Raises(), _Raises()]
    assert first_reply("q", chain) == ""


def test_empty_chain_returns_empty():
    assert first_reply("q", []) == ""


def test_build_chain_without_keys_is_empty(monkeypatch):
    for name in ("OPENROUTER_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    assert build_chain() == []
