"""Agent-style pipeline steps for analysis, case design, and code generation."""

from __future__ import annotations

import json
import re
from textwrap import indent
from typing import Any

from ai_test_agent.models import (
    AnalysisResult,
    EndpointSpec,
    GeneratedSuite,
    RiskLevel,
    TestCase,
    TestCategory,
    TestPoint,
)


ENDPOINT_RE = re.compile(r"^\s*(?:#{1,6}\s*)?(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s`#]+)", re.IGNORECASE)
STATUS_RE = re.compile(r"(?:Success|status|status code)\s*[:=]\s*(\d{3})", re.IGNORECASE)
KEYS_RE = re.compile(r"(?:Response Keys|response fields|return fields)\s*[:=]\s*([A-Za-z0-9_,\s-]+)", re.IGNORECASE)
JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.IGNORECASE | re.DOTALL)


def _slug(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return safe or "case"


def _extract_request_json(block: str) -> dict[str, Any]:
    match = JSON_BLOCK_RE.search(block)
    if not match:
        return {}
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _extract_response_keys(block: str) -> list[str]:
    match = KEYS_RE.search(block)
    if not match:
        return []
    raw = match.group(1)
    return [item.strip() for item in re.split(r"[,\s]+", raw) if item.strip()]


def _extract_success_status(block: str, method: str) -> int:
    match = STATUS_RE.search(block)
    if match:
        return int(match.group(1))
    return 201 if method.upper() == "POST" else 200


class RequirementAnalysisAgent:
    """Extracts endpoints and risk-oriented test points from requirement text."""

    def analyze(self, requirement_text: str, source_name: str = "requirements") -> AnalysisResult:
        text = requirement_text.strip()
        if not text:
            raise ValueError("需求文本不能为空。")

        endpoints = self._parse_endpoints(text)
        test_points = self._build_test_points(endpoints, text)
        summary = self._summarize(endpoints, text)
        return AnalysisResult(
            source_name=source_name,
            summary=summary,
            endpoints=endpoints,
            test_points=test_points,
        )

    def _parse_endpoints(self, text: str) -> list[EndpointSpec]:
        lines = text.splitlines()
        endpoint_starts: list[tuple[int, re.Match[str]]] = []
        for index, line in enumerate(lines):
            match = ENDPOINT_RE.match(line)
            if match:
                endpoint_starts.append((index, match))

        endpoints: list[EndpointSpec] = []
        for position, (start, match) in enumerate(endpoint_starts):
            end = endpoint_starts[position + 1][0] if position + 1 < len(endpoint_starts) else len(lines)
            block = "\n".join(lines[start:end])
            method = match.group(1).upper()
            path = match.group(2).strip()
            request_json = _extract_request_json(block)
            required_fields = list(request_json.keys())
            endpoints.append(
                EndpointSpec(
                    method=method,
                    path=path,
                    name=f"{method} {path}",
                    description=self._first_description(block),
                    request_json=request_json,
                    success_status=_extract_success_status(block, method),
                    response_keys=_extract_response_keys(block),
                    required_fields=required_fields,
                )
            )
        return endpoints

    def _build_test_points(self, endpoints: list[EndpointSpec], text: str) -> list[TestPoint]:
        points: list[TestPoint] = []
        if endpoints:
            for index, endpoint in enumerate(endpoints, start=1):
                risk = RiskLevel.high if endpoint.method in {"POST", "PUT", "PATCH", "DELETE"} else RiskLevel.medium
                points.append(
                    TestPoint(
                        id=f"TP-{index:03d}",
                        feature=endpoint.name,
                        description=f"验证 {endpoint.name} 的成功响应、参数校验和响应契约。",
                        risk_level=risk,
                        source_excerpt=endpoint.description[:180],
                    )
                )
            return points

        sentences = [item.strip() for item in re.split(r"[.!?\n]+", text) if item.strip()]
        for index, sentence in enumerate(sentences[:5], start=1):
            points.append(
                TestPoint(
                    id=f"TP-{index:03d}",
                    feature=f"需求 {index}",
                    description=sentence,
                    risk_level=RiskLevel.medium,
                    source_excerpt=sentence[:180],
                )
            )
        return points

    @staticmethod
    def _first_description(block: str) -> str:
        for line in block.splitlines()[1:]:
            stripped = line.strip(" -")
            if stripped and not stripped.startswith("```") and ":" not in stripped[:24]:
                return stripped
        return block.splitlines()[0].strip("# ")

    @staticmethod
    def _summarize(endpoints: list[EndpointSpec], text: str) -> str:
        if endpoints:
            methods = ", ".join(sorted({endpoint.method for endpoint in endpoints}))
            return f"Parsed {len(endpoints)} API endpoints covering methods: {methods}."
        return f"Parsed free-form requirement text with {len(text)} characters."


class TestCaseDesignAgent:
    """Turns analysis output into executable API test cases."""

    def generate(self, analysis: AnalysisResult) -> list[TestCase]:
        cases: list[TestCase] = []
        for index, endpoint in enumerate(analysis.endpoints, start=1):
            cases.append(self._positive_case(index, endpoint))
            cases.append(self._negative_case(index, endpoint))
        return cases

    def _positive_case(self, index: int, endpoint: EndpointSpec) -> TestCase:
        return TestCase(
            id=f"TC-{index:03d}-P",
            title=f"{endpoint.name} 返回预期成功响应",
            category=TestCategory.positive,
            priority="P0" if endpoint.method == "POST" else "P1",
            method=endpoint.method,
            path=endpoint.path,
            payload=endpoint.request_json,
            expected_status=endpoint.success_status,
            expected_keys=endpoint.response_keys,
            preconditions=["示例 API 服务可用。"],
            steps=[
                f"发送 {endpoint.method} 请求到 {endpoint.path}。",
                "校验 HTTP 状态码。",
                "校验响应 JSON 契约。",
            ],
            expected_result=f"响应状态码为 {endpoint.success_status}，且必要响应字段存在。",
        )

    def _negative_case(self, index: int, endpoint: EndpointSpec) -> TestCase:
        payload = dict(endpoint.request_json)
        expected_status = 422
        if payload:
            payload.pop(next(iter(payload)))
            title = f"{endpoint.name} 拒绝缺失必填字段"
        else:
            title = f"{endpoint.name} 拒绝不存在的资源"
            expected_status = 404

        path = endpoint.path if endpoint.request_json else f"{endpoint.path.rstrip('/')}/missing"
        return TestCase(
            id=f"TC-{index:03d}-N",
            title=title,
            category=TestCategory.negative,
            priority="P1",
            method=endpoint.method,
            path=path,
            payload=payload,
            expected_status=expected_status,
            expected_keys=[],
            preconditions=["示例 API 服务可用。"],
            steps=[
                f"发送无效的 {endpoint.method} 请求到 {path}。",
                "校验服务返回明确的客户端错误。",
            ],
            expected_result=f"响应状态码为 {expected_status}。",
        )


class PytestCodeAgent:
    """Generates runnable pytest code for FastAPI TestClient."""

    def generate(self, suite: GeneratedSuite) -> str:
        test_functions = "\n\n".join(self._render_case(case) for case in suite.test_cases)
        return (
            '"""Generated by AI Test Agent. Do not edit by hand."""\n\n'
            "from fastapi.testclient import TestClient\n\n"
            "from ai_test_agent.sample_api import app\n\n\n"
            "client = TestClient(app)\n\n\n"
            f"{test_functions}\n"
        )

    def _render_case(self, case: TestCase) -> str:
        function_name = f"test_{_slug(case.id)}_{_slug(case.title)}"
        call = self._render_client_call(case)
        key_assertions = "\n".join(f'    assert "{key}" in data' for key in case.expected_keys)
        data_block = "    data = response.json()\n" if case.expected_keys else ""
        if key_assertions:
            key_assertions = f"\n{key_assertions}"

        body = (
            f"def {function_name}():\n"
            f"    response = {call}\n"
            f"    assert response.status_code == {case.expected_status}\n"
            f"{data_block}"
            f"{key_assertions}"
        )
        return body.rstrip()

    @staticmethod
    def _render_client_call(case: TestCase) -> str:
        method = case.method.lower()
        path = json.dumps(case.path)
        if method in {"post", "put", "patch"}:
            payload = json.dumps(case.payload, ensure_ascii=True, sort_keys=True)
            return f"client.{method}({path}, json={payload})"
        return f"client.{method}({path})"


def render_suite_as_markdown(suite: GeneratedSuite) -> str:
    risk_labels = {"low": "低", "medium": "中", "high": "高"}
    category_labels = {"positive": "正向", "boundary": "边界", "negative": "异常", "security": "安全"}
    summary = suite.analysis.summary
    if summary.startswith("Parsed ") and " API endpoints covering methods: " in summary:
        count = summary.split("Parsed ", 1)[1].split(" API endpoints", 1)[0]
        methods = summary.split("methods: ", 1)[1].rstrip(".")
        summary = f"已解析 {count} 个接口，覆盖方法：{methods}。"
    elif summary.startswith("Parsed free-form requirement text with "):
        count = summary.split("with ", 1)[1].split(" characters", 1)[0]
        summary = f"已解析 {count} 个字符的自由格式需求文本。"
    lines = [
        f"# {suite.project_name} 测试套件",
        "",
        f"- 目标地址：`{suite.target_base_url}`",
        f"- 生成时间：`{suite.generated_at.isoformat()}`",
        f"- 摘要：{summary}",
        "",
        "## 测试点",
        "",
        "| ID | 功能 | 风险 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for point in suite.analysis.test_points:
        risk = risk_labels.get(point.risk_level.value, point.risk_level.value)
        lines.append(f"| {point.id} | {point.feature} | {risk} | {point.description} |")

    lines.extend(
        [
            "",
            "## 测试用例",
            "",
            "| ID | 类别 | 优先级 | 请求 | 预期状态 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for case in suite.test_cases:
        request = f"{case.method} {case.path}"
        category = category_labels.get(case.category.value, case.category.value)
        lines.append(f"| {case.id} | {category} | {case.priority} | `{request}` | {case.expected_status} |")
    return "\n".join(lines) + "\n"


def indent_code(code: str, prefix: str = "    ") -> str:
    return indent(code, prefix)
