from pathlib import Path

from ai_test_agent.agents import RequirementAnalysisAgent, TestCaseDesignAgent
from ai_test_agent.assets import QualityAssetBuilder
from ai_test_agent.models import ExecutionResult, GeneratedSuite
from ai_test_agent.reporting import ReportGenerator


def test_report_contains_suite_and_execution_summary():
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")
    analysis = RequirementAnalysisAgent().analyze(text)
    suite = GeneratedSuite(
        project_name="Demo API",
        target_base_url="http://testserver",
        analysis=analysis,
        test_cases=TestCaseDesignAgent().generate(analysis),
    )
    execution = ExecutionResult(success=True, returncode=0, total=8, passed=8)
    bug_summaries = QualityAssetBuilder().build_bug_summaries(suite, execution)

    markdown = ReportGenerator().markdown(suite, execution, bug_summaries=bug_summaries)

    assert "执行结果" in markdown
    assert "疑似 Bug 与风险摘要" in markdown
    assert "状态：**通过**" in markdown
    assert "TC-001-P" in markdown
