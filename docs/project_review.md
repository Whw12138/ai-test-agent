# Project Review

## Why This Project

纯手工测试岗位的竞争力正在变弱，但测试开发仍然需要扎实的测试思维、自动化能力和工程化能力。AI Test Agent 的目标是把这些能力放在一个可运行项目里展示出来。

## What It Demonstrates

- 能把需求文档转成测试点和测试用例。
- 能用 Python 写自动化测试工具，而不只是执行测试。
- 能生成和运行 `pytest` 测试代码。
- 能把测试结果整理成报告。
- 能通过 CLI、FastAPI、CI 把项目包装成完整工程。

## Interview Talking Points

1. 需求分析不是直接让模型随便生成，而是先提取接口、状态码、请求体、响应字段，再生成用例。
2. 项目默认不依赖大模型 API，避免演示时因为网络或 Key 出问题。
3. 生成的测试不是静态文本，而是真正会被 `pytest` 执行。
4. 通过 JUnit XML 解析执行结果，比只看控制台输出更工程化。
5. 后续可以扩展到 OpenAPI、Postman、真实测试环境和 AI 测试评估。

## Resume Version

项目：AI Test Agent：基于大模型思路的接口测试用例生成与自动执行系统

描述：使用 Python、FastAPI、pytest 实现智能测试助手，支持输入 Markdown 接口需求文档，自动提取接口信息和测试点，生成正向/异常测试用例及可执行 pytest 脚本，并调用测试执行器生成 Markdown/HTML 报告。项目提供 CLI、FastAPI 接口、示例后端服务、单元/集成测试和 GitHub Actions CI，默认支持无 API Key 离线运行，并预留 OpenAI 兼容 LLM/LangChain 扩展。

## Suggested Demo Flow

1. 展示 `examples/sample_api_requirements.md`。
2. 运行 `ai-test-agent run -i examples/sample_api_requirements.md -o runs/demo`。
3. 打开生成的 `test_generated_api.py`。
4. 打开 `reports/report.md` 或 `reports/report.html`。
5. 展示 `python -m pytest` 和 GitHub Actions。
