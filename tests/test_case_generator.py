from pathlib import Path

from ai_test_agent.agents import RequirementAnalysisAgent, TestCaseDesignAgent


def test_case_generator_creates_positive_and_negative_cases():
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")
    analysis = RequirementAnalysisAgent().analyze(text)
    cases = TestCaseDesignAgent().generate(analysis)

    assert len(cases) == 8
    assert cases[0].expected_status == 200
    assert cases[1].expected_status == 404
    assert cases[3].expected_status == 422
