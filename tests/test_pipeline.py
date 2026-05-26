from pathlib import Path

from ai_test_agent.pipeline import AITestAgentPipeline


def test_pipeline_generates_executes_and_reports(tmp_path):
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")

    result = AITestAgentPipeline().run(
        text,
        output_dir=tmp_path,
        project_name="Demo API",
        source_name="sample",
        execute=True,
    )

    assert Path(result.test_file).exists()
    assert Path(result.markdown_report).exists()
    assert Path(result.html_report).exists()
    assert result.execution is not None
    assert result.execution.success is True
    assert result.execution.total == 8
