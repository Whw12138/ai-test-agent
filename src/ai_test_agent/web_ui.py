"""Browser UI for AI Test Agent."""

WEB_UI_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Test Agent</title>
  <style>
    :root {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #5f6b7a;
      --line: #d9e0ea;
      --blue: #2563eb;
      --green: #15803d;
      --red: #b91c1c;
      --amber: #b45309;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, sans-serif;
      font-size: 14px;
      letter-spacing: 0;
    }
    header {
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 0 24px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }
    h1 { margin: 0; font-size: 20px; line-height: 1.2; }
    h2 { margin: 0 0 12px; font-size: 15px; line-height: 1.3; }
    p { margin: 0; color: var(--muted); line-height: 1.5; }
    a { color: var(--blue); text-decoration: none; }
    button, select, input, textarea {
      font: inherit;
    }
    button {
      border: 1px solid var(--line);
      background: #ffffff;
      color: var(--ink);
      border-radius: 6px;
      padding: 9px 12px;
      cursor: pointer;
      min-height: 38px;
    }
    button.primary {
      border-color: var(--blue);
      background: var(--blue);
      color: #ffffff;
      font-weight: 700;
    }
    button:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }
    input, select, textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #ffffff;
      color: var(--ink);
      padding: 9px 10px;
    }
    textarea {
      min-height: 420px;
      resize: vertical;
      font-family: Consolas, Monaco, monospace;
      font-size: 13px;
      line-height: 1.5;
    }
    label {
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }
    main {
      display: grid;
      grid-template-columns: minmax(360px, 0.9fr) minmax(480px, 1.1fr);
      gap: 18px;
      padding: 18px;
      max-width: 1440px;
      margin: 0 auto;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      min-width: 0;
    }
    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-bottom: 14px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }
    .checkline {
      display: flex;
      gap: 8px;
      align-items: center;
      min-height: 38px;
    }
    .checkline input {
      width: 16px;
      height: 16px;
    }
    .status {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 86px;
      min-height: 32px;
      border-radius: 6px;
      padding: 6px 10px;
      background: #eef2f7;
      color: var(--muted);
      font-weight: 700;
    }
    .status.pass { background: #dcfce7; color: var(--green); }
    .status.fail { background: #fee2e2; color: var(--red); }
    .status.work { background: #fef3c7; color: var(--amber); }
    .metrics {
      display: grid;
      grid-template-columns: repeat(5, minmax(92px, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    .metric {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #ffffff;
    }
    .metric span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 6px;
    }
    .metric strong {
      display: block;
      font-size: 22px;
      line-height: 1.1;
    }
    .split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }
    th, td {
      border-bottom: 1px solid #edf0f5;
      padding: 9px 8px;
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }
    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }
    iframe {
      width: 100%;
      height: 360px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #ffffff;
    }
    .report-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin: 10px 0;
    }
    .empty {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 220px;
      border: 1px dashed var(--line);
      border-radius: 8px;
      color: var(--muted);
      text-align: center;
      padding: 18px;
    }
    .error {
      color: var(--red);
      white-space: pre-wrap;
    }
    @media (max-width: 980px) {
      main { grid-template-columns: 1fr; }
      .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .grid, .split { grid-template-columns: 1fr; }
      textarea { min-height: 300px; }
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>AI Test Agent</h1>
      <p>Requirement to test cases, pytest code, and execution report.</p>
    </div>
    <nav>
      <a href="/docs">Swagger</a>
    </nav>
  </header>

  <main>
    <section class="panel">
      <div class="toolbar">
        <button id="sampleText">Markdown Sample</button>
        <button id="sampleOpenApi">OpenAPI Sample</button>
        <button id="clearInput">Clear</button>
      </div>

      <div class="grid">
        <div>
          <label for="projectName">Project</label>
          <input id="projectName" value="Demo API">
        </div>
        <div>
          <label for="inputFormat">Input Format</label>
          <select id="inputFormat">
            <option value="auto">Auto</option>
            <option value="text">Text</option>
            <option value="openapi">OpenAPI</option>
          </select>
        </div>
        <div>
          <label for="outputDir">Output</label>
          <input id="outputDir" value="runs/web">
        </div>
      </div>

      <label for="requirementText">Requirement</label>
      <textarea id="requirementText"></textarea>

      <div class="toolbar" style="margin-top: 14px; margin-bottom: 0;">
        <button id="runButton" class="primary">Run Agent</button>
        <span class="checkline"><input id="executeTests" type="checkbox" checked><span>Execute tests</span></span>
      </div>
    </section>

    <section class="panel">
      <div class="report-actions">
        <div>
          <h2>Run Result</h2>
          <p id="summary">Ready</p>
        </div>
        <span id="status" class="status">IDLE</span>
      </div>

      <div class="metrics">
        <div class="metric"><span>Total</span><strong id="mTotal">0</strong></div>
        <div class="metric"><span>Passed</span><strong id="mPassed">0</strong></div>
        <div class="metric"><span>Failed</span><strong id="mFailed">0</strong></div>
        <div class="metric"><span>Errors</span><strong id="mErrors">0</strong></div>
        <div class="metric"><span>Duration</span><strong id="mDuration">-</strong></div>
      </div>

      <div class="split">
        <div>
          <h2>Endpoints</h2>
          <div id="endpointsEmpty" class="empty">No result yet.</div>
          <table id="endpointsTable" hidden>
            <thead><tr><th>Method</th><th>Path</th><th>Status</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
        <div>
          <h2>Test Cases</h2>
          <div id="casesEmpty" class="empty">No result yet.</div>
          <table id="casesTable" hidden>
            <thead><tr><th>ID</th><th>Request</th><th>Expected</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <div class="report-actions">
        <h2>Report Preview</h2>
        <a id="reportLink" href="#" target="_blank" hidden>Open report</a>
      </div>
      <div id="reportEmpty" class="empty">Run the agent to generate a report.</div>
      <iframe id="reportFrame" title="Generated test report" hidden></iframe>
      <p id="errorBox" class="error"></p>
    </section>
  </main>

  <script>
    const markdownSample = `# Sample Shop API Requirements

## GET /health
Description: Check whether the service is alive.
Success: 200
Response Keys: status

## POST /login
Description: Login with demo credentials and receive an access token.
Request JSON:
\\`\\`\\`json
{"username": "demo", "password": "secret"}
\\`\\`\\`
Success: 200
Response Keys: token, user_id

## GET /products
Description: Query all available products.
Success: 200
Response Keys: items, total

## POST /orders
Description: Create an order for an existing product.
Request JSON:
\\`\\`\\`json
{"product_id": 1, "quantity": 2}
\\`\\`\\`
Success: 201
Response Keys: order_id, status
`;

    const openApiSample = JSON.stringify({
      openapi: "3.1.0",
      info: { title: "Sample Shop API", version: "0.1.0" },
      paths: {
        "/health": {
          get: {
            summary: "Check service health",
            responses: {
              "200": {
                description: "Service is healthy",
                content: { "application/json": { schema: { type: "object", properties: { status: { type: "string", example: "ok" } } } } }
              }
            }
          }
        },
        "/login": {
          post: {
            summary: "Login with demo credentials",
            requestBody: {
              required: true,
              content: { "application/json": { schema: { type: "object", required: ["username", "password"], properties: { username: { type: "string", example: "demo" }, password: { type: "string", example: "secret" } } } } }
            },
            responses: {
              "200": {
                description: "Login succeeded",
                content: { "application/json": { schema: { type: "object", properties: { token: { type: "string" }, user_id: { type: "integer" } } } } }
              }
            }
          }
        },
        "/products": {
          get: {
            summary: "List products",
            responses: {
              "200": {
                description: "Products returned",
                content: { "application/json": { schema: { type: "object", properties: { items: { type: "array" }, total: { type: "integer" } } } } }
              }
            }
          }
        },
        "/orders": {
          post: {
            summary: "Create an order",
            requestBody: {
              required: true,
              content: { "application/json": { schema: { type: "object", required: ["product_id", "quantity"], properties: { product_id: { type: "integer", example: 1 }, quantity: { type: "integer", example: 2 } } } } }
            },
            responses: {
              "201": {
                description: "Order created",
                content: { "application/json": { schema: { type: "object", properties: { order_id: { type: "string" }, status: { type: "string" } } } } }
              }
            }
          }
        }
      }
    }, null, 2);

    const $ = (id) => document.getElementById(id);

    function setStatus(label, kind) {
      const status = $("status");
      status.textContent = label;
      status.className = "status" + (kind ? " " + kind : "");
    }

    function resetTables() {
      $("endpointsTable").hidden = true;
      $("casesTable").hidden = true;
      $("endpointsEmpty").hidden = false;
      $("casesEmpty").hidden = false;
      $("endpointsTable").querySelector("tbody").innerHTML = "";
      $("casesTable").querySelector("tbody").innerHTML = "";
    }

    function rows(tableId, emptyId, values, renderer) {
      const table = $(tableId);
      const body = table.querySelector("tbody");
      body.innerHTML = values.map(renderer).join("");
      table.hidden = values.length === 0;
      $(emptyId).hidden = values.length !== 0;
    }

    function artifactUrl(path) {
      const normalized = path.replaceAll("\\\\", "/");
      const marker = "/runs/";
      const index = normalized.indexOf(marker);
      if (index >= 0) {
        return normalized.slice(index);
      }
      if (normalized.startsWith("runs/")) {
        return "/" + normalized;
      }
      return "";
    }

    async function runAgent() {
      $("errorBox").textContent = "";
      $("runButton").disabled = true;
      setStatus("RUNNING", "work");
      $("summary").textContent = "Running pipeline";

      try {
        const response = await fetch("/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: $("requirementText").value,
            source_name: "web-ui",
            project_name: $("projectName").value || "Demo API",
            output_dir: $("outputDir").value || "runs/web",
            execute: $("executeTests").checked,
            input_format: $("inputFormat").value
          })
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "Request failed");
        }

        const execution = data.execution;
        const statusKind = execution && execution.success ? "pass" : execution ? "fail" : "";
        setStatus(execution ? (execution.success ? "PASS" : "FAIL") : "GENERATED", statusKind);
        $("summary").textContent = data.suite.analysis.summary;
        $("mTotal").textContent = execution ? execution.total : data.suite.test_cases.length;
        $("mPassed").textContent = execution ? execution.passed : 0;
        $("mFailed").textContent = execution ? execution.failed : 0;
        $("mErrors").textContent = execution ? execution.errors : 0;
        $("mDuration").textContent = execution ? execution.duration_seconds.toFixed(2) + "s" : "-";

        rows("endpointsTable", "endpointsEmpty", data.suite.analysis.endpoints, (item) =>
          `<tr><td>${item.method}</td><td>${item.path}</td><td>${item.success_status}</td></tr>`
        );
        rows("casesTable", "casesEmpty", data.suite.test_cases, (item) =>
          `<tr><td>${item.id}</td><td>${item.method} ${item.path}</td><td>${item.expected_status}</td></tr>`
        );

        const url = artifactUrl(data.html_report);
        if (url) {
          const cacheBustUrl = url + "?t=" + Date.now();
          $("reportFrame").src = cacheBustUrl;
          $("reportFrame").hidden = false;
          $("reportEmpty").hidden = true;
          $("reportLink").href = cacheBustUrl;
          $("reportLink").hidden = false;
        }
      } catch (error) {
        setStatus("ERROR", "fail");
        $("summary").textContent = "Run failed";
        $("errorBox").textContent = error.message;
      } finally {
        $("runButton").disabled = false;
      }
    }

    $("sampleText").addEventListener("click", () => {
      $("requirementText").value = markdownSample;
      $("inputFormat").value = "text";
    });
    $("sampleOpenApi").addEventListener("click", () => {
      $("requirementText").value = openApiSample;
      $("inputFormat").value = "openapi";
    });
    $("clearInput").addEventListener("click", () => {
      $("requirementText").value = "";
      resetTables();
      $("reportFrame").hidden = true;
      $("reportEmpty").hidden = false;
      $("reportLink").hidden = true;
      $("summary").textContent = "Ready";
      $("errorBox").textContent = "";
      setStatus("IDLE", "");
    });
    $("runButton").addEventListener("click", runAgent);

    $("requirementText").value = markdownSample;
  </script>
</body>
</html>
"""
