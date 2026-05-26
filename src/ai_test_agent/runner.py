"""Pytest execution utilities."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from ai_test_agent.models import ExecutionFailure, ExecutionResult


class PytestRunner:
    def run(self, test_file: Path, project_root: Path) -> ExecutionResult:
        junit_xml = test_file.parent / "junit.xml"
        env = os.environ.copy()
        src_path = str(project_root / "src")
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = src_path if not existing_pythonpath else f"{src_path}{os.pathsep}{existing_pythonpath}"

        command = [
            sys.executable,
            "-m",
            "pytest",
            str(test_file),
            "-q",
            "--tb=short",
            f"--junitxml={junit_xml}",
        ]
        start = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=project_root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        duration = time.perf_counter() - start
        parsed = self._parse_junit(junit_xml)
        return ExecutionResult(
            success=completed.returncode == 0,
            returncode=completed.returncode,
            duration_seconds=duration,
            stdout=completed.stdout,
            stderr=completed.stderr,
            junit_xml=str(junit_xml) if junit_xml.exists() else None,
            **parsed,
        )

    def _parse_junit(self, junit_xml: Path) -> dict[str, object]:
        if not junit_xml.exists():
            return {"failures": []}

        root = ET.parse(junit_xml).getroot()
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        if suite is None:
            return {"failures": []}

        failures: list[ExecutionFailure] = []
        for case in suite.findall(".//testcase"):
            name = case.attrib.get("name", "unknown")
            failure_node = case.find("failure") or case.find("error")
            if failure_node is not None:
                failures.append(
                    ExecutionFailure(
                        name=name,
                        message=failure_node.attrib.get("message", failure_node.text or ""),
                    )
                )

        total = int(float(suite.attrib.get("tests", 0)))
        failed = int(float(suite.attrib.get("failures", 0)))
        errors = int(float(suite.attrib.get("errors", 0)))
        skipped = int(float(suite.attrib.get("skipped", 0)))
        return {
            "total": total,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "passed": max(total - failed - errors - skipped, 0),
            "failures": failures,
        }
