"""End-to-end orchestration for AI Test Agent."""

from __future__ import annotations

import json
from pathlib import Path

from ai_test_agent.agents import PytestCodeAgent, RequirementAnalysisAgent, TestCaseDesignAgent
from ai_test_agent.config import settings
from ai_test_agent.models import GeneratedSuite, PipelineResult
from ai_test_agent.reporting import ReportGenerator
from ai_test_agent.runner import PytestRunner


class AITestAgentPipeline:
    def __init__(
        self,
        analyzer: RequirementAnalysisAgent | None = None,
        case_designer: TestCaseDesignAgent | None = None,
        code_agent: PytestCodeAgent | None = None,
        runner: PytestRunner | None = None,
        reporter: ReportGenerator | None = None,
    ) -> None:
        self.analyzer = analyzer or RequirementAnalysisAgent()
        self.case_designer = case_designer or TestCaseDesignAgent()
        self.code_agent = code_agent or PytestCodeAgent()
        self.runner = runner or PytestRunner()
        self.reporter = reporter or ReportGenerator()

    def run(
        self,
        requirement_text: str,
        output_dir: Path | str | None = None,
        project_name: str = "Demo API",
        source_name: str = "requirements",
        target_base_url: str | None = None,
        execute: bool = True,
    ) -> PipelineResult:
        project_root = Path(__file__).resolve().parents[2]
        output = Path(output_dir) if output_dir is not None else settings.output_dir
        if not output.is_absolute():
            output = project_root / output
        output.mkdir(parents=True, exist_ok=True)

        analysis = self.analyzer.analyze(requirement_text, source_name=source_name)
        cases = self.case_designer.generate(analysis)
        suite = GeneratedSuite(
            project_name=project_name,
            target_base_url=target_base_url or settings.target_base_url,
            analysis=analysis,
            test_cases=cases,
        )

        generated_dir = output / "generated_tests"
        generated_dir.mkdir(parents=True, exist_ok=True)
        test_file = generated_dir / "test_generated_api.py"
        code = self.code_agent.generate(suite)
        test_file.write_text(code, encoding="utf-8")

        suite_file = output / "suite.json"
        suite_file.write_text(json.dumps(suite.model_dump(mode="json"), indent=2), encoding="utf-8")

        execution = self.runner.run(test_file, project_root) if execute else None
        markdown_report = self.reporter.markdown(suite, execution)
        html_report = self.reporter.html(markdown_report)

        report_dir = output / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = report_dir / "report.md"
        html_path = report_dir / "report.html"
        markdown_path.write_text(markdown_report, encoding="utf-8")
        html_path.write_text(html_report, encoding="utf-8")

        return PipelineResult(
            suite=suite,
            test_file=str(test_file),
            markdown_report=str(markdown_path),
            html_report=str(html_path),
            execution=execution,
        )
