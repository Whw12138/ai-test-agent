"""Quality asset generation for bug summaries and test mindmaps."""

from __future__ import annotations

import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from xml.sax.saxutils import escape

from ai_test_agent.models import BugSummary, ExecutionResult, GeneratedSuite, RiskLevel, TestCase


CATEGORY_LABELS = {
    "positive": "正向",
    "boundary": "边界",
    "negative": "异常",
    "security": "安全",
}

RISK_LABELS = {
    "low": "低风险",
    "medium": "中风险",
    "high": "高风险",
}

RISK_SORT = {
    RiskLevel.high: 0,
    RiskLevel.medium: 1,
    RiskLevel.low: 2,
}


class QualityAssetBuilder:
    """Builds recruiter-friendly QA artifacts from the generated test suite."""

    def build_bug_summaries(
        self,
        suite: GeneratedSuite,
        execution: ExecutionResult | None,
    ) -> list[BugSummary]:
        if execution and execution.failures:
            return [
                BugSummary(
                    id=f"BUG-{index:03d}",
                    title=f"自动化失败：{failure.name}",
                    severity=RiskLevel.high,
                    status="待确认",
                    source="pytest 执行结果",
                    related_case=self._match_case_id(failure.name, suite.test_cases),
                    reproduction_steps=[
                        "在本地启动 AI Test Agent 示例服务。",
                        "运行生成的 pytest 脚本。",
                        f"定位失败用例：{failure.name}。",
                    ],
                    expected_result="接口响应满足生成用例中的状态码和字段契约。",
                    actual_result=failure.message,
                    recommendation="优先核对接口实现、请求参数、预期状态码和响应字段；必要时补充缺陷复现截图。",
                )
                for index, failure in enumerate(execution.failures, start=1)
            ]

        risk_points = sorted(
            suite.analysis.test_points,
            key=lambda point: (RISK_SORT.get(point.risk_level, 9), point.id),
        )
        summaries: list[BugSummary] = []
        for index, point in enumerate(risk_points[:5], start=1):
            related_case = self._first_related_case(point.feature, suite.test_cases)
            summaries.append(
                BugSummary(
                    id=f"RISK-{index:03d}",
                    title=f"风险关注：{point.feature}",
                    severity=point.risk_level,
                    status="待验证" if point.risk_level != RiskLevel.low else "观察中",
                    source="需求分析",
                    related_case=related_case,
                    reproduction_steps=[
                        "根据需求文档确认业务规则和接口契约。",
                        "执行相关正向、异常和边界测试用例。",
                        "结合响应状态码、字段完整性和日志判断是否形成缺陷。",
                    ],
                    expected_result="关键业务路径稳定，异常输入得到明确错误响应。",
                    actual_result="当前自动化执行未发现失败，仍建议作为回归关注项保留。",
                    recommendation=self._risk_recommendation(point.risk_level),
                )
            )
        return summaries

    def render_mindmap_markdown(
        self,
        suite: GeneratedSuite,
        execution: ExecutionResult | None,
        bug_summaries: list[BugSummary],
    ) -> str:
        lines = [
            f"# {suite.project_name} 测试脑图",
            "",
            "```mermaid",
            "mindmap",
            f"  root(({_mindmap_label(suite.project_name)} 测试脑图))",
            "    接口契约",
        ]
        for endpoint in suite.analysis.endpoints:
            lines.append(f"      {_mindmap_label(endpoint.method + ' ' + endpoint.path)}")
            if endpoint.required_fields:
                lines.append(f"        必填字段 {_mindmap_label(', '.join(endpoint.required_fields))}")
            if endpoint.response_keys:
                lines.append(f"        响应字段 {_mindmap_label(', '.join(endpoint.response_keys))}")

        lines.append("    测试点")
        for point in suite.analysis.test_points:
            risk = RISK_LABELS.get(point.risk_level.value, point.risk_level.value)
            lines.append(f"      {_mindmap_label(point.feature)}")
            lines.append(f"        {risk}")

        lines.append("    测试用例")
        grouped_cases: dict[str, list[TestCase]] = defaultdict(list)
        for case in suite.test_cases:
            grouped_cases[case.category.value].append(case)
        for category, cases in grouped_cases.items():
            lines.append(f"      {CATEGORY_LABELS.get(category, category)}")
            for case in cases:
                lines.append(f"        {_mindmap_label(case.id + ' ' + case.method + ' ' + case.path)}")

        lines.append("    疑似Bug与风险")
        if bug_summaries:
            for item in bug_summaries:
                severity = RISK_LABELS.get(item.severity.value, item.severity.value)
                lines.append(f"      {_mindmap_label(item.id + ' ' + item.title)}")
                lines.append(f"        {severity}")
                if item.related_case:
                    lines.append(f"        关联用例 {_mindmap_label(item.related_case)}")
        else:
            lines.append("      本次未发现执行失败")

        status = "未执行"
        pass_rate = "-"
        if execution is not None:
            status = "通过" if execution.success else "失败"
            pass_rate = f"{round((execution.passed / execution.total) * 100)}%" if execution.total else "-"
        lines.extend(
            [
                "    测试报告",
                f"      状态 {status}",
                f"      通过率 {pass_rate}",
                f"      用例数 {len(suite.test_cases)}",
            ]
        )
        return "\n".join(lines) + "\n```\n"

    def write_xmind(
        self,
        path: Path,
        suite: GeneratedSuite,
        execution: ExecutionResult | None,
        bug_summaries: list[BugSummary],
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        branches = self._xmind_branches(suite, execution, bug_summaries)
        timestamp = str(int(datetime.now(timezone.utc).timestamp() * 1000))
        root = _topic_xml(f"{suite.project_name} 测试脑图", branches, timestamp, structure=True)
        content_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            f'<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" timestamp="{timestamp}">\n'
            f'  <sheet id="{uuid4().hex}" timestamp="{timestamp}">\n'
            f"    <title>{escape(suite.project_name)} 测试脑图</title>\n"
            f"{root}"
            "  </sheet>\n"
            "</xmap-content>\n"
        )
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<xmap-styles xmlns="urn:xmind:xmap:xmlns:style:2.0"/>\n'
        )
        meta_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<meta xmlns="urn:xmind:xmap:xmlns:meta:2.0">\n'
            "  <Creator><Name>AI Test Agent</Name><Version>0.1.0</Version></Creator>\n"
            "</meta>\n"
        )
        manifest_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">\n'
            '  <file-entry full-path="content.xml" media-type="text/xml"/>\n'
            '  <file-entry full-path="styles.xml" media-type="text/xml"/>\n'
            '  <file-entry full-path="meta.xml" media-type="text/xml"/>\n'
            "</manifest>\n"
        )
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("content.xml", content_xml)
            archive.writestr("styles.xml", styles_xml)
            archive.writestr("meta.xml", meta_xml)
            archive.writestr("META-INF/manifest.xml", manifest_xml)

    def _xmind_branches(
        self,
        suite: GeneratedSuite,
        execution: ExecutionResult | None,
        bug_summaries: list[BugSummary],
    ) -> list[tuple[str, list]]:
        endpoint_children = [
            (
                f"{endpoint.method} {endpoint.path}",
                [
                    (f"成功状态码 {endpoint.success_status}", []),
                    (f"必填字段 {', '.join(endpoint.required_fields) or '-'}", []),
                    (f"响应字段 {', '.join(endpoint.response_keys) or '-'}", []),
                ],
            )
            for endpoint in suite.analysis.endpoints
        ]
        point_children = [
            (
                point.feature,
                [
                    (RISK_LABELS.get(point.risk_level.value, point.risk_level.value), []),
                    (point.description, []),
                ],
            )
            for point in suite.analysis.test_points
        ]
        grouped_cases: dict[str, list[TestCase]] = defaultdict(list)
        for case in suite.test_cases:
            grouped_cases[case.category.value].append(case)
        case_children = [
            (
                CATEGORY_LABELS.get(category, category),
                [(f"{case.id} {case.method} {case.path}", []) for case in cases],
            )
            for category, cases in grouped_cases.items()
        ]
        bug_children = [
            (
                f"{item.id} {item.title}",
                [
                    (RISK_LABELS.get(item.severity.value, item.severity.value), []),
                    (f"状态 {item.status}", []),
                    (f"关联用例 {item.related_case or '-'}", []),
                ],
            )
            for item in bug_summaries
        ] or [("本次未发现执行失败", [])]
        status = "未执行"
        pass_rate = "-"
        if execution is not None:
            status = "通过" if execution.success else "失败"
            pass_rate = f"{round((execution.passed / execution.total) * 100)}%" if execution.total else "-"
        report_children = [
            (f"状态 {status}", []),
            (f"通过率 {pass_rate}", []),
            (f"用例数 {len(suite.test_cases)}", []),
        ]
        return [
            ("接口契约", endpoint_children),
            ("测试点", point_children),
            ("测试用例", case_children),
            ("疑似 Bug 与风险", bug_children),
            ("测试报告", report_children),
        ]

    @staticmethod
    def _match_case_id(failure_name: str, cases: list[TestCase]) -> str:
        normalized = failure_name.lower().replace("_", "")
        for case in cases:
            if case.id.lower().replace("-", "") in normalized:
                return case.id
        return ""

    @staticmethod
    def _first_related_case(feature: str, cases: list[TestCase]) -> str:
        feature_text = feature.lower()
        for case in cases:
            if case.path.lower() in feature_text or feature_text in case.title.lower():
                return case.id
        return cases[0].id if cases else ""

    @staticmethod
    def _risk_recommendation(risk_level: RiskLevel) -> str:
        if risk_level == RiskLevel.high:
            return "建议优先补充鉴权、异常输入、幂等和数据一致性验证，并纳入回归清单。"
        if risk_level == RiskLevel.medium:
            return "建议保留为回归关注项，补充边界值、字段缺失和响应契约校验。"
        return "当前风险较低，可在核心流程稳定后补充覆盖。"


def _mindmap_label(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    return (
        cleaned.replace("(", "（")
        .replace(")", "）")
        .replace("[", "【")
        .replace("]", "】")
        .replace("{", "｛")
        .replace("}", "｝")
        .replace(":", "：")
    )


def _topic_xml(title: str, children: list[tuple[str, list]], timestamp: str, structure: bool = False) -> str:
    topic_id = uuid4().hex
    structure_attr = ' structure-class="org.xmind.ui.logic.right"' if structure else ""
    child_xml = ""
    if children:
        child_xml = (
            "      <children><topics type=\"attached\">\n"
            + "".join(_topic_xml(child_title, child_children, timestamp) for child_title, child_children in children)
            + "      </topics></children>\n"
        )
    return (
        f'    <topic id="{topic_id}"{structure_attr} timestamp="{timestamp}">\n'
        f"      <title>{escape(_one_line(title))}</title>\n"
        f"{child_xml}"
        "    </topic>\n"
    )


def _one_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()
