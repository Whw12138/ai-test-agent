"""Markdown and HTML report generation."""

from __future__ import annotations

import html

from ai_test_agent.agents import render_suite_as_markdown
from ai_test_agent.models import ExecutionResult, GeneratedSuite


class ReportGenerator:
    def markdown(self, suite: GeneratedSuite, execution: ExecutionResult | None) -> str:
        content = [render_suite_as_markdown(suite), "## Execution Result", ""]
        if execution is None:
            content.append("Tests were generated but not executed.")
            return "\n".join(content).rstrip() + "\n"

        status = "PASS" if execution.success else "FAIL"
        content.extend(
            [
                f"- Status: **{status}**",
                f"- Total: {execution.total}",
                f"- Passed: {execution.passed}",
                f"- Failed: {execution.failed}",
                f"- Errors: {execution.errors}",
                f"- Skipped: {execution.skipped}",
                f"- Duration: {execution.duration_seconds:.2f}s",
                "",
            ]
        )
        if execution.failures:
            content.extend(["### Failure Summary", ""])
            for failure in execution.failures:
                content.append(f"- `{failure.name}`: {failure.message}")
            content.append("")

        content.extend(
            [
                "### Pytest Output",
                "",
                "```text",
                execution.stdout.strip() or "(no stdout)",
                "```",
            ]
        )
        if execution.stderr.strip():
            content.extend(["", "### Stderr", "", "```text", execution.stderr.strip(), "```"])
        return "\n".join(content).rstrip() + "\n"

    def html(self, markdown_report: str) -> str:
        escaped = html.escape(markdown_report)
        return (
            "<!doctype html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "  <title>AI Test Agent Report</title>\n"
            "  <style>\n"
            "    body { font-family: Arial, sans-serif; line-height: 1.55; margin: 32px; color: #1f2937; }\n"
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
