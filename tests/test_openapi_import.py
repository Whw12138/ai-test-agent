from pathlib import Path

import pytest

from ai_test_agent.openapi import OpenAPIAnalysisAgent, OpenAPIImportError
from ai_test_agent.pipeline import AITestAgentPipeline


OPENAPI_SAMPLE = Path("examples/sample_openapi.json").read_text(encoding="utf-8")


def test_openapi_importer_extracts_contracts():
    result = OpenAPIAnalysisAgent().analyze(OPENAPI_SAMPLE, source_name="swagger")

    assert result.source_name == "swagger"
    assert len(result.endpoints) == 4
    assert result.endpoints[1].path == "/login"
    assert result.endpoints[1].request_json == {"username": "demo", "password": "secret"}
    assert result.endpoints[3].success_status == 201
    assert result.endpoints[3].response_keys == ["order_id", "status"]


def test_openapi_importer_rejects_invalid_json():
    with pytest.raises(OpenAPIImportError, match="valid JSON"):
        OpenAPIAnalysisAgent().analyze("{not-json")


def test_pipeline_runs_openapi_sample(tmp_path):
    result = AITestAgentPipeline().run(
        OPENAPI_SAMPLE,
        output_dir=tmp_path,
        source_name="openapi",
        input_format="openapi",
    )

    assert result.execution is not None
    assert result.execution.success is True
    assert result.execution.total == 8
    assert Path(result.html_report).read_text(encoding="utf-8").startswith("<!doctype html>")
