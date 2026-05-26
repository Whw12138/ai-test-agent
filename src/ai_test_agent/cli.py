"""Command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_test_agent.pipeline import AITestAgentPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Test Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Generate and optionally execute pytest tests.")
    run_parser.add_argument("--input", "-i", required=True, help="Path to requirement or API document.")
    run_parser.add_argument("--output", "-o", default="runs/demo", help="Output directory.")
    run_parser.add_argument("--project-name", default="Demo API", help="Name shown in reports.")
    run_parser.add_argument("--source-name", default="requirements", help="Source name shown in analysis.")
    run_parser.add_argument("--no-execute", action="store_true", help="Only generate suite and pytest code.")
    run_parser.add_argument("--json", action="store_true", help="Print machine-readable result.")

    serve_parser = subparsers.add_parser("serve", help="Start FastAPI service.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "serve":
        import uvicorn

        uvicorn.run("ai_test_agent.api:app", host=args.host, port=args.port, reload=False)
        return

    requirement_path = Path(args.input)
    requirement_text = requirement_path.read_text(encoding="utf-8")
    result = AITestAgentPipeline().run(
        requirement_text,
        output_dir=Path(args.output),
        project_name=args.project_name,
        source_name=args.source_name,
        execute=not args.no_execute,
    )

    if args.json:
        print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return

    status = "generated"
    if result.execution is not None:
        status = "passed" if result.execution.success else "failed"
    print(f"AI Test Agent {status}.")
    print(f"Test file: {result.test_file}")
    print(f"Markdown report: {result.markdown_report}")
    print(f"HTML report: {result.html_report}")


if __name__ == "__main__":
    main()
