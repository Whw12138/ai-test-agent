from pathlib import Path

from ai_test_agent.agents import PytestCodeAgent, RequirementAnalysisAgent, TestCaseDesignAgent
from ai_test_agent.models import GeneratedSuite


def test_pytest_code_agent_generates_runnable_test_code():
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")
    analysis = RequirementAnalysisAgent().analyze(text)
    suite = GeneratedSuite(
        project_name="Demo API",
        target_base_url="http://testserver",
        analysis=analysis,
        test_cases=TestCaseDesignAgent().generate(analysis),
    )

    code = PytestCodeAgent().generate(suite)

    assert "TestClient" in code
    assert "client.post(\"/login\"" in code
    assert "assert response.status_code == 201" in code
