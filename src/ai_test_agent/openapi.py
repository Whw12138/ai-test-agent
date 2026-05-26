"""OpenAPI/Swagger import support."""

from __future__ import annotations

import json
import re
from typing import Any

from ai_test_agent.models import AnalysisResult, EndpointSpec, RiskLevel, TestPoint


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


class OpenAPIImportError(ValueError):
    """Raised when an OpenAPI document cannot be parsed."""


class OpenAPIAnalysisAgent:
    """Converts an OpenAPI JSON document into the internal analysis model."""

    def analyze(self, raw_document: str | dict[str, Any], source_name: str = "openapi") -> AnalysisResult:
        document = self._load_document(raw_document)
        paths = document.get("paths")
        if not isinstance(paths, dict) or not paths:
            raise OpenAPIImportError("OpenAPI document must include a non-empty 'paths' object.")

        endpoints: list[EndpointSpec] = []
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                    continue
                endpoints.append(self._operation_to_endpoint(method.upper(), path, operation))

        if not endpoints:
            raise OpenAPIImportError("OpenAPI document does not contain supported HTTP operations.")

        test_points = [
            TestPoint(
                id=f"TP-{index:03d}",
                feature=endpoint.name,
                description=f"Validate OpenAPI contract for {endpoint.name}.",
                risk_level=RiskLevel.high if endpoint.method in {"POST", "PUT", "PATCH", "DELETE"} else RiskLevel.medium,
                source_excerpt=endpoint.description[:180],
            )
            for index, endpoint in enumerate(endpoints, start=1)
        ]
        title = document.get("info", {}).get("title", "OpenAPI service")
        return AnalysisResult(
            source_name=source_name,
            summary=f"Imported {len(endpoints)} endpoints from {title}.",
            endpoints=endpoints,
            test_points=test_points,
        )

    def _load_document(self, raw_document: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(raw_document, dict):
            document = raw_document
        else:
            try:
                document = json.loads(raw_document)
            except json.JSONDecodeError as exc:
                raise OpenAPIImportError("OpenAPI input must be valid JSON.") from exc
        if not isinstance(document, dict):
            raise OpenAPIImportError("OpenAPI input must be a JSON object.")
        if "openapi" not in document and "swagger" not in document:
            raise OpenAPIImportError("OpenAPI input must include 'openapi' or 'swagger'.")
        return document

    def _operation_to_endpoint(self, method: str, path: str, operation: dict[str, Any]) -> EndpointSpec:
        success_status, response_keys = self._extract_response_contract(operation)
        request_json = self._extract_request_example(operation)
        operation_name = operation.get("summary") or operation.get("operationId") or f"{method} {path}"
        executable_path = self._path_with_examples(path, operation)
        return EndpointSpec(
            method=method,
            path=executable_path,
            name=f"{method} {path}",
            description=str(operation_name),
            request_json=request_json,
            success_status=success_status,
            response_keys=response_keys,
            required_fields=list(request_json.keys()),
        )

    def _extract_request_example(self, operation: dict[str, Any]) -> dict[str, Any]:
        request_body = operation.get("requestBody", {})
        if not isinstance(request_body, dict):
            return {}
        content = request_body.get("content", {})
        if not isinstance(content, dict):
            return {}
        media = content.get("application/json", {})
        if not isinstance(media, dict):
            return {}
        if isinstance(media.get("example"), dict):
            return media["example"]
        schema = media.get("schema", {})
        if not isinstance(schema, dict):
            return {}
        return self._example_from_schema(schema)

    def _extract_response_contract(self, operation: dict[str, Any]) -> tuple[int, list[str]]:
        responses = operation.get("responses", {})
        if not isinstance(responses, dict):
            return 200, []
        success_codes = sorted(str(code) for code in responses if str(code).startswith("2"))
        status = int(success_codes[0]) if success_codes else 200
        response = responses.get(str(status), {})
        if not isinstance(response, dict):
            return status, []
        content = response.get("content", {})
        if not isinstance(content, dict):
            return status, []
        media = content.get("application/json", {})
        if not isinstance(media, dict):
            return status, []
        schema = media.get("schema", {})
        if not isinstance(schema, dict):
            return status, []
        properties = schema.get("properties", {})
        keys = list(properties.keys()) if isinstance(properties, dict) else []
        return status, keys

    def _example_from_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            return {}
        required = schema.get("required", [])
        selected_keys = required if isinstance(required, list) and required else list(properties.keys())
        return {
            str(key): self._example_value(properties.get(key, {}))
            for key in selected_keys
            if isinstance(properties.get(key, {}), dict)
        }

    def _example_value(self, schema: dict[str, Any]) -> Any:
        if "example" in schema:
            return schema["example"]
        schema_type = schema.get("type")
        if schema_type == "integer":
            return 1
        if schema_type == "number":
            return 1.0
        if schema_type == "boolean":
            return True
        if schema_type == "array":
            return []
        if schema_type == "object":
            return {}
        return "demo"

    def _path_with_examples(self, path: str, operation: dict[str, Any]) -> str:
        parameter_examples = self._path_parameter_examples(operation)

        def replace(match: re.Match[str]) -> str:
            name = match.group(1)
            return str(parameter_examples.get(name, 1))

        return re.sub(r"\{([^}]+)\}", replace, path)

    def _path_parameter_examples(self, operation: dict[str, Any]) -> dict[str, Any]:
        examples: dict[str, Any] = {}
        parameters = operation.get("parameters", [])
        if not isinstance(parameters, list):
            return examples
        for parameter in parameters:
            if not isinstance(parameter, dict) or parameter.get("in") != "path":
                continue
            name = parameter.get("name")
            if not isinstance(name, str):
                continue
            if "example" in parameter:
                examples[name] = parameter["example"]
                continue
            schema = parameter.get("schema", {})
            examples[name] = self._example_value(schema if isinstance(schema, dict) else {})
        return examples
