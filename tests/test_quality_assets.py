import json
import zipfile
from pathlib import Path

from ai_test_agent.assets import QualityAssetBuilder
from ai_test_agent.models import ExecutionFailure, ExecutionResult, GeneratedSuite
from ai_test_agent.pipeline import AITestAgentPipeline


def test_pipeline_exports_bug_summary_and_mindmaps(tmp_path):
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")

    result = AITestAgentPipeline().run(text, output_dir=tmp_path, project_name="Demo API", execute=True)

    bug_summary_path = Path(result.bug_summary_file)
    mindmap_path = Path(result.mindmap_file)
    xmind_path = Path(result.xmind_file)

    assert bug_summary_path.exists()
    assert mindmap_path.exists()
    assert xmind_path.exists()

    bug_items = json.loads(bug_summary_path.read_text(encoding="utf-8"))
    assert bug_items
    assert bug_items[0]["id"].startswith("RISK-")
    assert "recommendation" in bug_items[0]

    mindmap = mindmap_path.read_text(encoding="utf-8")
    assert "mindmap" in mindmap
    assert "接口契约" in mindmap
    assert "疑似Bug与风险" in mindmap

    with zipfile.ZipFile(xmind_path) as archive:
        assert "content.xml" in archive.namelist()
        assert "META-INF/manifest.xml" in archive.namelist()


def test_quality_asset_builder_creates_bug_items_for_failures():
    text = Path("examples/sample_api_requirements.md").read_text(encoding="utf-8")
    pipeline = AITestAgentPipeline()
    analysis = pipeline.analyze_input(text)
    cases = pipeline.case_designer.generate(analysis)
    suite = GeneratedSuite(project_name="Demo API", target_base_url="http://testserver", analysis=analysis, test_cases=cases)
    execution = ExecutionResult(
        success=False,
        returncode=1,
        total=1,
        failed=1,
        failures=[ExecutionFailure(name="test_tc_001_p_health", message="assert 500 == 200")],
    )

    bugs = QualityAssetBuilder().build_bug_summaries(suite, execution)

    assert bugs[0].id == "BUG-001"
    assert bugs[0].severity == "high"
    assert bugs[0].status == "待确认"
    assert bugs[0].reproduction_steps
