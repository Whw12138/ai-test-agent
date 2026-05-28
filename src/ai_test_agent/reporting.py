"""Markdown and HTML report generation."""

from __future__ import annotations

import html

from ai_test_agent.agents import render_suite_as_markdown
from ai_test_agent.models import ExecutionResult, GeneratedSuite, TestCase, TestPoint


STATUS_LABELS = {
    "PASS": "通过",
    "FAIL": "失败",
    "NOT RUN": "未执行",
}

CATEGORY_LABELS = {
    "positive": "正向",
    "boundary": "边界",
    "negative": "异常",
    "security": "安全",
}

RISK_LABELS = {
    "low": "低",
    "medium": "中",
    "high": "高",
}


def _localized_summary(summary: str) -> str:
    if summary.startswith("Parsed ") and " API endpoints covering methods: " in summary:
        count = summary.split("Parsed ", 1)[1].split(" API endpoints", 1)[0]
        methods = summary.split("methods: ", 1)[1].rstrip(".")
        return f"已解析 {count} 个接口，覆盖方法：{methods}。"
    if summary.startswith("Parsed free-form requirement text with "):
        count = summary.split("with ", 1)[1].split(" characters", 1)[0]
        return f"已解析 {count} 个字符的自由格式需求文本。"
    return summary


class ReportGenerator:
    def markdown(self, suite: GeneratedSuite, execution: ExecutionResult | None) -> str:
        content = [render_suite_as_markdown(suite), "## 执行结果", ""]
        if execution is None:
            content.append("测试已生成，但未执行。")
            return "\n".join(content).rstrip() + "\n"

        status = "PASS" if execution.success else "FAIL"
        content.extend(
            [
                f"- 状态：**{STATUS_LABELS[status]}**",
                f"- 用例总数：{execution.total}",
                f"- 通过：{execution.passed}",
                f"- 失败：{execution.failed}",
                f"- 错误：{execution.errors}",
                f"- 跳过：{execution.skipped}",
                f"- 耗时：{execution.duration_seconds:.2f}s",
                "",
            ]
        )
        if execution.failures:
            content.extend(["### 失败摘要", ""])
            for failure in execution.failures:
                content.append(f"- `{failure.name}`: {failure.message}")
            content.append("")

        content.extend(
            [
                "### Pytest 输出",
                "",
                "```text",
                execution.stdout.strip() or "(无标准输出)",
                "```",
            ]
        )
        if execution.stderr.strip():
            content.extend(["", "### 标准错误", "", "```text", execution.stderr.strip(), "```"])
        return "\n".join(content).rstrip() + "\n"

    def html(
        self,
        markdown_report: str,
        suite: GeneratedSuite | None = None,
        execution: ExecutionResult | None = None,
    ) -> str:
        if suite is None:
            return self._plain_html(markdown_report)

        status = "NOT RUN"
        status_class = "neutral"
        if execution is not None:
            status = "PASS" if execution.success else "FAIL"
            status_class = "pass" if execution.success else "fail"
        status_label = STATUS_LABELS[status]

        return (
            "<!doctype html>\n"
            "<html lang=\"zh-CN\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"  <title>{html.escape(suite.project_name)} 测试报告</title>\n"
            f"{self._style()}"
            "</head>\n"
            "<body>\n"
            "  <main>\n"
            "    <section class=\"hero\">\n"
            "      <div>\n"
            f"        <p class=\"eyebrow\">AI Test Agent 测试报告</p>\n"
            f"        <h1>{html.escape(suite.project_name)} 测试套件</h1>\n"
            f"        <p>{html.escape(_localized_summary(suite.analysis.summary))}</p>\n"
            "      </div>\n"
            f"      <div class=\"status {status_class}\">{status_label}</div>\n"
            "    </section>\n"
            f"{self._metrics(execution, suite)}"
            "    <section>\n"
            "      <h2>测试点</h2>\n"
            f"{self._test_points_table(suite.analysis.test_points)}"
            "    </section>\n"
            "    <section>\n"
            "      <h2>生成的测试用例</h2>\n"
            f"{self._test_cases_table(suite.test_cases)}"
            "    </section>\n"
            f"{self._failure_section(execution)}"
            "    <section>\n"
            "      <h2>Pytest 输出</h2>\n"
            f"      <pre>{html.escape(execution.stdout.strip() if execution else '测试已生成，但未执行。')}</pre>\n"
            "    </section>\n"
            "  </main>\n"
            "</body>\n"
            "</html>\n"
        )

    def _plain_html(self, markdown_report: str) -> str:
        escaped = html.escape(markdown_report)
        return (
            "<!doctype html>\n"
            "<html lang=\"zh-CN\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "  <title>AI Test Agent 测试报告</title>\n"
            "  <style>\n"
            "    body { font-family: Arial, 'Microsoft YaHei', 'PingFang SC', sans-serif; line-height: 1.55; margin: 32px; color: #1f2937; }\n"
            "    pre { background: #f3f4f6; border: 1px solid #e5e7eb; padding: 16px; overflow: auto; }\n"
            "    code { background: #f3f4f6; padding: 2px 4px; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <pre>"
            f"{escaped}"
            "</pre>\n"
            "</body>\n"
            "</html>\n"
        )

    def _style(self) -> str:
        return (
            "  <style>\n"
            "    :root { color-scheme: light; --ink: #172033; --muted: #5f6b7a; --line: #d8dee8; }\n"
            "    body { margin: 0; font-family: Arial, 'Microsoft YaHei', 'PingFang SC', sans-serif; background: #f6f8fb; color: var(--ink); }\n"
            "    main { max-width: 1120px; margin: 0 auto; padding: 32px 20px 48px; }\n"
            "    section { margin-top: 20px; background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 20px; }\n"
            "    .hero { display: flex; justify-content: space-between; gap: 24px; align-items: center; }\n"
            "    .eyebrow { margin: 0 0 8px; color: #2563eb; font-size: 12px; font-weight: 700; text-transform: uppercase; }\n"
            "    h1 { margin: 0 0 8px; font-size: 28px; }\n"
            "    h2 { margin: 0 0 14px; font-size: 18px; }\n"
            "    p { margin: 0; color: var(--muted); }\n"
            "    .status { min-width: 96px; padding: 12px 14px; border-radius: 8px; text-align: center; font-weight: 700; }\n"
            "    .pass { background: #dcfce7; color: #166534; }\n"
            "    .fail { background: #fee2e2; color: #991b1b; }\n"
            "    .neutral { background: #e5e7eb; color: #374151; }\n"
            "    .metrics { display: grid; grid-template-columns: repeat(5, minmax(120px, 1fr)); gap: 12px; }\n"
            "    .metric { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 16px; }\n"
            "    .metric span { display: block; color: var(--muted); font-size: 12px; }\n"
            "    .metric strong { display: block; margin-top: 8px; font-size: 24px; }\n"
            "    table { width: 100%; border-collapse: collapse; }\n"
            "    th, td { padding: 10px 12px; border-bottom: 1px solid #edf0f5; text-align: left; vertical-align: top; }\n"
            "    th { color: var(--muted); font-size: 12px; text-transform: uppercase; }\n"
            "    code { background: #eef2ff; border-radius: 4px; padding: 2px 5px; }\n"
            "    pre { margin: 0; overflow: auto; background: #111827; color: #f9fafb; border-radius: 8px; padding: 16px; }\n"
            "    @media (max-width: 760px) { .hero { align-items: flex-start; flex-direction: column; } .metrics { grid-template-columns: 1fr 1fr; } }\n"
            "  </style>\n"
        )

    def _metrics(self, execution: ExecutionResult | None, suite: GeneratedSuite) -> str:
        total = execution.total if execution else len(suite.test_cases)
        passed = execution.passed if execution else 0
        failed = execution.failed if execution else 0
        errors = execution.errors if execution else 0
        duration = f"{execution.duration_seconds:.2f}s" if execution else "-"
        items = [
            ("用例总数", str(total)),
            ("通过", str(passed)),
            ("失败", str(failed)),
            ("错误", str(errors)),
            ("耗时", duration),
        ]
        cards = "".join(f"<div class=\"metric\"><span>{label}</span><strong>{value}</strong></div>" for label, value in items)
        return f"    <section class=\"metrics\">{cards}</section>\n"

    def _test_points_table(self, points: list[TestPoint]) -> str:
        rows = [
            "<tr>"
            f"<td>{html.escape(point.id)}</td>"
            f"<td>{html.escape(point.feature)}</td>"
            f"<td>{html.escape(RISK_LABELS.get(point.risk_level.value, point.risk_level.value))}</td>"
            f"<td>{html.escape(point.description)}</td>"
            "</tr>"
            for point in points
        ]
        return "<table><thead><tr><th>ID</th><th>功能</th><th>风险</th><th>说明</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>\n"

    def _test_cases_table(self, cases: list[TestCase]) -> str:
        rows = [
            "<tr>"
            f"<td>{html.escape(case.id)}</td>"
            f"<td>{html.escape(CATEGORY_LABELS.get(case.category.value, case.category.value))}</td>"
            f"<td>{html.escape(case.priority)}</td>"
            f"<td><code>{html.escape(case.method)} {html.escape(case.path)}</code></td>"
            f"<td>{case.expected_status}</td>"
            "</tr>"
            for case in cases
        ]
        return "<table><thead><tr><th>ID</th><th>类别</th><th>优先级</th><th>请求</th><th>预期状态</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>\n"

    def _failure_section(self, execution: ExecutionResult | None) -> str:
        if execution is None or not execution.failures:
            return ""
        rows = "".join(
            "<tr>"
            f"<td>{html.escape(failure.name)}</td>"
            f"<td>{html.escape(failure.message)}</td>"
            "</tr>"
            for failure in execution.failures
        )
        return (
            "    <section>\n"
            "      <h2>失败摘要</h2>\n"
            "      <table><thead><tr><th>测试</th><th>信息</th></tr></thead><tbody>"
            f"{rows}"
            "</tbody></table>\n"
            "    </section>\n"
        )
