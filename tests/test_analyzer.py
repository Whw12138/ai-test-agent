from pathlib import Path

import pytest

from ai_test_agent.agents import RequirementAnalysisAgent


SAMPLE = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")


def test_analyzer_extracts_endpoints_and_test_points():
    result = RequirementAnalysisAgent().analyze(SAMPLE, source_name="sample")

    assert result.source_name == "sample"
    assert len(result.endpoints) == 4
    assert len(result.test_points) == 4
    assert result.endpoints[1].method == "POST"
    assert result.endpoints[1].path == "/login"
    assert result.endpoints[1].request_json == {"username": "demo", "password": "secret"}


def test_analyzer_rejects_empty_text():
    with pytest.raises(ValueError, match="empty"):
        RequirementAnalysisAgent().analyze("   ")
