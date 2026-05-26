"""FastAPI interface for AI Test Agent."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ai_test_agent.agents import TestCaseDesignAgent
from ai_test_agent.models import AnalysisResult, GeneratedSuite, PipelineResult
from ai_test_agent.pipeline import AITestAgentPipeline


app = FastAPI(
    title="AI Test Agent",
    version="0.1.0",
    description="Generate test cases, pytest code, and execution reports from API requirements.",
)


class RequirementRequest(BaseModel):
    text: str = Field(min_length=1)
    source_name: str = "requirements"
    project_name: str = "Demo API"
    output_dir: str = "runs/api"
    execute: bool = True
    input_format: str = Field(default="auto", pattern="^(auto|text|openapi)$")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
def analyze(request: RequirementRequest) -> AnalysisResult:
    try:
        return AITestAgentPipeline().analyze_input(
            request.text,
            source_name=request.source_name,
            input_format=request.input_format,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/generate", response_model=GeneratedSuite)
def generate(request: RequirementRequest) -> GeneratedSuite:
    try:
        analysis = AITestAgentPipeline().analyze_input(
            request.text,
            source_name=request.source_name,
            input_format=request.input_format,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    cases = TestCaseDesignAgent().generate(analysis)
    return GeneratedSuite(
        project_name=request.project_name,
        target_base_url="http://testserver",
        analysis=analysis,
        test_cases=cases,
    )


@app.post("/run", response_model=PipelineResult)
def run_pipeline(request: RequirementRequest) -> PipelineResult:
    try:
        return AITestAgentPipeline().run(
            request.text,
            output_dir=Path(request.output_dir),
            project_name=request.project_name,
            source_name=request.source_name,
            input_format=request.input_format,
            execute=request.execute,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
