"""Shared data contracts for the agent pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TestCategory(str, Enum):
    positive = "positive"
    boundary = "boundary"
    negative = "negative"
    security = "security"


class EndpointSpec(BaseModel):
    method: str
    path: str
    name: str
    description: str = ""
    request_json: dict[str, Any] = Field(default_factory=dict)
    success_status: int = 200
    response_keys: list[str] = Field(default_factory=list)
    required_fields: list[str] = Field(default_factory=list)


class TestPoint(BaseModel):
    id: str
    feature: str
    description: str
    risk_level: RiskLevel = RiskLevel.medium
    source_excerpt: str = ""


class AnalysisResult(BaseModel):
    source_name: str = "requirements"
    summary: str
    endpoints: list[EndpointSpec] = Field(default_factory=list)
    test_points: list[TestPoint] = Field(default_factory=list)


class TestCase(BaseModel):
    id: str
    title: str
    category: TestCategory
    priority: str = "P1"
    method: str
    path: str
    payload: dict[str, Any] = Field(default_factory=dict)
    expected_status: int
    expected_keys: list[str] = Field(default_factory=list)
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_result: str


class GeneratedSuite(BaseModel):
    project_name: str
    target_base_url: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    analysis: AnalysisResult
    test_cases: list[TestCase] = Field(default_factory=list)


class ExecutionFailure(BaseModel):
    name: str
    message: str


class ExecutionResult(BaseModel):
    success: bool
    returncode: int
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    duration_seconds: float = 0.0
    stdout: str = ""
    stderr: str = ""
    junit_xml: str | None = None
    failures: list[ExecutionFailure] = Field(default_factory=list)


class BugSummary(BaseModel):
    id: str
    title: str
    severity: RiskLevel = RiskLevel.medium
    status: str = "待验证"
    source: str = "AI Test Agent"
    related_case: str = ""
    reproduction_steps: list[str] = Field(default_factory=list)
    expected_result: str = ""
    actual_result: str = ""
    recommendation: str = ""


class PipelineResult(BaseModel):
    suite: GeneratedSuite
    test_file: str
    markdown_report: str
    html_report: str
    execution: ExecutionResult | None = None
    bug_summaries: list[BugSummary] = Field(default_factory=list)
    bug_summary_file: str = ""
    mindmap_file: str = ""
    xmind_file: str = ""
