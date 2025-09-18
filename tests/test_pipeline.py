import pytest
from analyzer.code_analyzer import CodeAnalyzer
from llm.openai_review import OpenAIReviewer


def test_analyzer_runs(tmp_path):
    code_file = tmp_path / "sample.py"
    code_file.write_text("x=1\nprint(x)\n")

    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(code_file)
    assert isinstance(results, str)
    assert "E" in results or "W" in results or results == ""


def test_llm_reviewer_mock(monkeypatch):
    def fake_review(self, code, lint):
        return "Mock feedback"

    monkeypatch.setattr(OpenAIReviewer, "review", fake_review)

    reviewer = OpenAIReviewer()
    result = reviewer.review("print('hi')", "")
    assert "Mock feedback" in result