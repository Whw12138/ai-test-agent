"""Browser UI for AI Test Agent."""

WEB_UI_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Test Agent 智能测试助手</title>
  <style>
    :root {
      --sky: #dff6f0;
      --grass: #9edc8a;
      --leaf: #39aa70;
      --deep-leaf: #1f795b;
      --pond: #86d5da;
      --shell: #fff8dc;
      --paper: #fff8e7;
      --paper-2: #fff2c7;
      --wood: #b97845;
      --wood-dark: #6f472c;
      --ink: #2d3528;
      --muted: #6d765f;
      --line: rgba(111, 71, 44, 0.22);
      --aqua: #43c8bf;
      --blue: #4c8ed9;
      --amber: #e2a744;
      --rose: #d65d64;
      --violet: #9071d8;
      --shadow: 0 18px 0 rgba(111, 71, 44, 0.1), 0 28px 60px rgba(82, 102, 70, 0.18);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 12% 8%, rgba(255, 248, 220, 0.88), transparent 18%),
        radial-gradient(circle at 86% 10%, rgba(134, 213, 218, 0.46), transparent 22%),
        radial-gradient(circle at 18% 92%, rgba(57, 170, 112, 0.26), transparent 26%),
        linear-gradient(180deg, var(--sky) 0%, #edf9e9 44%, #c9e9ab 100%);
      color: var(--ink);
      font-family: Inter, "Microsoft YaHei", "PingFang SC", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
      overflow-x: hidden;
    }
    body::before,
    body::after {
      content: "";
      position: fixed;
      left: -8vw;
      right: -8vw;
      pointer-events: none;
      z-index: 0;
    }
    body::before {
      top: 0;
      height: 180px;
      background:
        radial-gradient(circle at 12% 64%, rgba(255,255,255,0.9) 0 24px, transparent 25px),
        radial-gradient(circle at 17% 58%, rgba(255,255,255,0.86) 0 34px, transparent 35px),
        radial-gradient(circle at 72% 72%, rgba(255,255,255,0.72) 0 28px, transparent 29px),
        radial-gradient(circle at 78% 66%, rgba(255,255,255,0.74) 0 40px, transparent 41px);
      opacity: 0.78;
    }
    body::after {
      bottom: -90px;
      height: 270px;
      background:
        radial-gradient(60% 90% at 14% 0%, rgba(68, 167, 112, 0.38), transparent 64%),
        radial-gradient(68% 100% at 72% 8%, rgba(255, 230, 126, 0.36), transparent 62%),
        radial-gradient(54% 80% at 46% 12%, rgba(134, 213, 218, 0.34), transparent 66%);
      filter: blur(0.2px);
    }
    a { color: inherit; text-decoration: none; }
    button, input, select, textarea { font: inherit; }
    button {
      border: 0;
      cursor: pointer;
      min-height: 40px;
    }
    button:disabled {
      opacity: 0.58;
      cursor: wait;
    }
    .dot-field {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
      opacity: 0.5;
    }
    .app-shell {
      position: relative;
      z-index: 1;
      width: min(1480px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 20px 0 36px;
    }
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 16px;
      padding: 10px 12px;
      border: 2px solid rgba(111, 71, 44, 0.18);
      border-radius: 24px 30px 22px 28px;
      background:
        linear-gradient(90deg, rgba(255,248,220,0.82), rgba(255,255,255,0.64)),
        repeating-linear-gradient(90deg, rgba(185,120,69,0.08) 0 8px, rgba(255,255,255,0) 8px 18px);
      box-shadow: 0 10px 0 rgba(111, 71, 44, 0.08);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .mark {
      display: grid;
      place-items: center;
      width: 46px;
      height: 42px;
      border: 2px solid rgba(20, 91, 66, 0.24);
      border-radius: 55% 45% 58% 42% / 44% 55% 45% 56%;
      background:
        radial-gradient(circle at 32% 24%, rgba(255,255,255,0.55), transparent 32%),
        linear-gradient(145deg, #58c987, #1f8a5f);
      color: #fffbe8;
      font-weight: 900;
      box-shadow: 0 8px 0 rgba(31, 121, 91, 0.18);
      transform: rotate(-4deg);
    }
    .brand h1 {
      margin: 0;
      font-size: 18px;
      line-height: 1.1;
      color: #253226;
    }
    .brand p {
      margin: 4px 0 0;
      color: #65735a;
      font-size: 13px;
    }
    .nav {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .nav a, .ghost-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      min-height: 40px;
      padding: 0 14px;
      border: 2px solid rgba(111, 71, 44, 0.18);
      border-radius: 999px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,248,220,0.9));
      color: #31412e;
      font-size: 13px;
      box-shadow: 0 5px 0 rgba(111, 71, 44, 0.12);
    }
    .nav a:hover, .ghost-button:hover {
      transform: translateY(-1px);
      box-shadow: 0 7px 0 rgba(111, 71, 44, 0.12);
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.08fr) minmax(330px, 0.72fr);
      gap: 18px;
      margin-bottom: 18px;
    }
    .hero-main {
      min-height: 228px;
      padding: 28px;
      border: 3px solid rgba(111, 71, 44, 0.18);
      border-radius: 34px 42px 30px 38px;
      background:
        radial-gradient(circle at 88% 12%, rgba(255, 231, 112, 0.5), transparent 26%),
        radial-gradient(circle at 78% 76%, rgba(134, 213, 218, 0.45), transparent 30%),
        linear-gradient(135deg, rgba(255, 252, 227, 0.96), rgba(240, 255, 233, 0.9));
      box-shadow: var(--shadow);
      overflow: hidden;
      position: relative;
    }
    .hero-main::before {
      content: "";
      position: absolute;
      width: 220px;
      height: 96px;
      right: 28px;
      bottom: 18px;
      border-radius: 48% 52% 45% 55% / 56% 46% 54% 44%;
      background:
        radial-gradient(circle at 24% 44%, rgba(255,255,255,0.42) 0 16px, transparent 17px),
        linear-gradient(150deg, rgba(95, 191, 128, 0.34), rgba(134, 213, 218, 0.38));
      border: 2px dashed rgba(31, 121, 91, 0.18);
    }
    .hero-main::after {
      content: "";
      position: absolute;
      width: 300px;
      height: 300px;
      right: -120px;
      top: -128px;
      background:
        conic-gradient(from 130deg, rgba(255, 231, 112, 0), rgba(255, 231, 112, 0.4), rgba(76, 142, 217, 0.18), rgba(57, 170, 112, 0.22), rgba(255, 231, 112, 0));
      filter: blur(16px);
      opacity: 0.85;
    }
    .kicker {
      margin: 0 0 12px;
      color: var(--deep-leaf);
      font-size: 12px;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .hero-title {
      position: relative;
      z-index: 1;
      max-width: 780px;
      margin: 0;
      font-size: clamp(32px, 5vw, 64px);
      line-height: 1.02;
      letter-spacing: 0;
      color: #223226;
      text-shadow: 0 3px 0 rgba(255, 248, 220, 0.86);
    }
    .shiny-text {
      color: transparent;
      background:
        linear-gradient(110deg, #1f795b 0%, #1f795b 32%, #fff8dc 46%, #e2a744 50%, #1f795b 66%, #1f795b 100%);
      background-size: 280% 100%;
      background-clip: text;
      -webkit-background-clip: text;
      animation: shine 4.2s linear infinite;
    }
    @keyframes shine {
      0% { background-position: 140% 0; }
      100% { background-position: -140% 0; }
    }
    .hero-copy {
      position: relative;
      z-index: 1;
      margin: 18px 0 0;
      max-width: 720px;
      color: #52625e;
      font-size: 15px;
      line-height: 1.8;
    }
    .hero-actions {
      position: relative;
      z-index: 1;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 22px;
    }
    .primary-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 0 16px;
      border: 2px solid rgba(111, 71, 44, 0.16);
      border-radius: 999px;
      background:
        linear-gradient(180deg, #2e9165, #1f795b);
      color: #fffbe8;
      font-weight: 900;
      box-shadow: 0 6px 0 rgba(31, 121, 91, 0.28), 0 16px 26px rgba(31, 121, 91, 0.18);
    }
    .primary-button:hover {
      transform: translateY(-1px);
      box-shadow: 0 8px 0 rgba(31, 121, 91, 0.24), 0 18px 28px rgba(31, 121, 91, 0.16);
    }
    .spotlight {
      position: relative;
      overflow: hidden;
      border: 3px solid rgba(111, 71, 44, 0.16);
      border-radius: 30px 36px 28px 34px;
      background:
        radial-gradient(360px circle at var(--x, 50%) var(--y, 50%), rgba(255, 231, 112, 0.32), transparent 44%),
        linear-gradient(180deg, rgba(255, 252, 231, 0.92), rgba(247, 255, 238, 0.9));
      box-shadow: var(--shadow);
    }
    .insight-panel {
      padding: 20px;
      display: grid;
      align-content: space-between;
      gap: 18px;
      min-height: 228px;
    }
    .insight-panel h2 {
      margin: 0;
      font-size: 18px;
      color: #2c3a2b;
    }
    .insight-panel p {
      margin: 8px 0 0;
      color: var(--muted);
      line-height: 1.6;
    }
    .signal-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 9px;
    }
    .signal {
      padding: 12px;
      border-radius: 20px 18px 22px 16px;
      background:
        radial-gradient(circle at 82% 18%, rgba(255,255,255,0.74), transparent 34%),
        rgba(255, 248, 220, 0.82);
      border: 2px solid rgba(111,71,44,0.12);
      box-shadow: inset 0 -3px 0 rgba(111,71,44,0.05);
    }
    .signal strong {
      display: block;
      font-size: 20px;
      line-height: 1;
    }
    .signal span {
      display: block;
      margin-top: 7px;
      color: var(--muted);
      font-size: 12px;
    }
    .workspace {
      display: grid;
      grid-template-columns: minmax(420px, 0.94fr) minmax(520px, 1.06fr);
      gap: 18px;
      align-items: start;
    }
    .panel {
      border: 3px solid rgba(111, 71, 44, 0.16);
      border-radius: 30px 36px 28px 34px;
      background:
        linear-gradient(180deg, rgba(255, 252, 231, 0.96), rgba(255, 248, 220, 0.9));
      box-shadow: var(--shadow);
      min-width: 0;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      padding: 18px 18px 13px;
      border-bottom: 2px dashed rgba(111, 71, 44, 0.18);
      background:
        radial-gradient(circle at 92% 22%, rgba(134, 213, 218, 0.28), transparent 20%),
        linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0));
    }
    .panel-header h2 {
      margin: 0;
      font-size: 16px;
      color: #253226;
    }
    .panel-header p {
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .panel-body {
      padding: 18px;
    }
    .control-row {
      display: grid;
      grid-template-columns: 1fr 150px 1fr;
      gap: 10px;
      margin-bottom: 12px;
    }
    label {
      display: block;
      margin: 0 0 6px;
      color: #617058;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    input, select, textarea {
      width: 100%;
      border: 2px solid rgba(111, 71, 44, 0.16);
      border-radius: 18px 16px 20px 15px;
      background: rgba(255,255,255,0.78);
      color: var(--ink);
      outline: none;
      box-shadow: inset 0 2px 0 rgba(255,255,255,0.72);
    }
    input, select {
      min-height: 42px;
      padding: 0 12px;
    }
    textarea {
      min-height: 420px;
      padding: 14px;
      resize: vertical;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 13px;
      line-height: 1.62;
      background:
        linear-gradient(rgba(255,255,255,0.82), rgba(255,255,255,0.82)),
        repeating-linear-gradient(180deg, transparent 0 27px, rgba(67, 200, 191, 0.14) 28px 29px);
    }
    input:focus, select:focus, textarea:focus {
      border-color: rgba(57, 170, 112, 0.72);
      box-shadow: 0 0 0 4px rgba(255, 231, 112, 0.28), inset 0 2px 0 rgba(255,255,255,0.72);
    }
    .tabs, .run-row {
      display: flex;
      flex-wrap: wrap;
      gap: 9px;
      align-items: center;
    }
    .tabs {
      margin-bottom: 12px;
    }
    .tab-button {
      padding: 0 13px;
      border-radius: 999px;
      border: 2px solid rgba(111, 71, 44, 0.14);
      background: rgba(255,255,255,0.66);
      color: #273a35;
      font-size: 13px;
      box-shadow: 0 4px 0 rgba(111, 71, 44, 0.08);
    }
    .tab-button.active {
      background: #d7f5bd;
      color: #1f795b;
      border-color: rgba(57,170,112,0.28);
      font-weight: 900;
    }
    .run-row {
      justify-content: space-between;
      margin-top: 14px;
    }
    .toggle {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      color: #465641;
      font-size: 13px;
      font-weight: 800;
    }
    .toggle input {
      width: 17px;
      height: 17px;
      accent-color: var(--aqua);
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 96px;
      min-height: 36px;
      padding: 0 12px;
      border-radius: 999px;
      border: 2px solid rgba(111, 71, 44, 0.12);
      background: #fff8dc;
      color: #56644b;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: 0.04em;
      box-shadow: 0 5px 0 rgba(111, 71, 44, 0.1);
    }
    .status-pill.pass { background: #c9f4d0; color: #1d6b45; }
    .status-pill.fail { background: #ffd8d8; color: #9f1d2c; }
    .status-pill.work { background: #ffe790; color: #765011; }
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }
    .metric {
      min-height: 82px;
      padding: 13px;
      border-radius: 22px 18px 20px 16px;
      background:
        radial-gradient(circle at 85% 12%, rgba(255,255,255,0.7), transparent 34%),
        rgba(255, 248, 220, 0.78);
      border: 2px solid rgba(111,52,47,0.1);
      box-shadow: inset 0 -4px 0 rgba(111, 71, 44, 0.05);
    }
    .metric span {
      display: block;
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .metric strong {
      display: block;
      margin-top: 10px;
      font-size: 24px;
      line-height: 1;
    }
    .result-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }
    .mini-panel {
      min-width: 0;
      border: 2px solid rgba(111,71,44,0.14);
      border-radius: 22px 18px 22px 18px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.78), rgba(255,252,231,0.68));
      overflow: hidden;
    }
    .mini-panel h3 {
      margin: 0;
      padding: 13px 14px;
      border-bottom: 2px dashed rgba(111,71,44,0.12);
      font-size: 13px;
      color: #2c3a2b;
    }
    .empty {
      display: grid;
      place-items: center;
      min-height: 180px;
      padding: 20px;
      color: var(--muted);
      text-align: center;
      line-height: 1.5;
      background:
        radial-gradient(circle at 50% 40%, rgba(134, 213, 218, 0.12), transparent 36%);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }
    th, td {
      padding: 10px 12px;
      border-bottom: 1px dashed rgba(111,71,44,0.12);
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
      font-size: 12px;
    }
    th {
      color: var(--muted);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      background: rgba(255, 248, 220, 0.48);
    }
    .method {
      display: inline-flex;
      min-width: 48px;
      justify-content: center;
      border-radius: 8px;
      padding: 4px 7px;
      background: #d9f4ff;
      color: #27638f;
      font-weight: 900;
    }
    .method.post {
      background: #d7f5bd;
      color: #1f795b;
    }
    .report-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }
    .report-bar h3 {
      margin: 0;
      font-size: 14px;
    }
    iframe {
      width: 100%;
      height: 390px;
      border: 2px solid rgba(111,71,44,0.14);
      border-radius: 22px 18px 22px 18px;
      background: #fffdf2;
    }
    .error {
      margin: 12px 0 0;
      color: var(--rose);
      white-space: pre-wrap;
      line-height: 1.5;
    }
    @media (max-width: 1080px) {
      .hero, .workspace { grid-template-columns: 1fr; }
      .control-row, .result-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .app-shell { width: min(100vw - 20px, 1480px); padding-top: 12px; }
      .topbar { align-items: flex-start; flex-direction: column; }
      .hero-main { padding: 20px; }
      .metric-grid, .signal-grid { grid-template-columns: 1fr 1fr; }
      textarea { min-height: 320px; }
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script type="text/babel">
    const { useEffect, useRef, useState } = React;

    const markdownSample = `# 示例商城 API 需求

## GET /health
Description: 检查服务是否存活。
Success: 200
Response Keys: status

## POST /login
Description: 使用演示账号登录并获取访问令牌。
Request JSON:
\`\`\`json
{"username": "demo", "password": "secret"}
\`\`\`
Success: 200
Response Keys: token, user_id

## GET /products
Description: 查询可售商品列表。
Success: 200
Response Keys: items, total

## POST /orders
Description: 为已有商品创建订单。
Request JSON:
\`\`\`json
{"product_id": 1, "quantity": 2}
\`\`\`
Success: 201
Response Keys: order_id, status
`;

    const openApiSample = JSON.stringify({
      openapi: "3.1.0",
      info: { title: "示例商城 API", version: "0.1.0" },
      paths: {
        "/health": {
          get: {
            summary: "检查服务健康状态",
            responses: {
              "200": {
                description: "服务正常",
                content: { "application/json": { schema: { type: "object", properties: { status: { type: "string", example: "ok" } } } } }
              }
            }
          }
        },
        "/login": {
          post: {
            summary: "使用演示账号登录",
            requestBody: {
              required: true,
              content: { "application/json": { schema: { type: "object", required: ["username", "password"], properties: { username: { type: "string", example: "demo" }, password: { type: "string", example: "secret" } } } } }
            },
            responses: {
              "200": {
                description: "登录成功",
                content: { "application/json": { schema: { type: "object", properties: { token: { type: "string" }, user_id: { type: "integer" } } } } }
              }
            }
          }
        },
        "/products": {
          get: {
            summary: "查询商品列表",
            responses: {
              "200": {
                description: "返回商品列表",
                content: { "application/json": { schema: { type: "object", properties: { items: { type: "array" }, total: { type: "integer" } } } } }
              }
            }
          }
        },
        "/orders": {
          post: {
            summary: "创建订单",
            requestBody: {
              required: true,
              content: { "application/json": { schema: { type: "object", required: ["product_id", "quantity"], properties: { product_id: { type: "integer", example: 1 }, quantity: { type: "integer", example: 2 } } } } }
            },
            responses: {
              "201": {
                description: "订单创建成功",
                content: { "application/json": { schema: { type: "object", properties: { order_id: { type: "string" }, status: { type: "string" } } } } }
              }
            }
          }
        }
      }
    }, null, 2);

    function DotField() {
      const canvasRef = useRef(null);

      useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        const pointer = { x: -9999, y: -9999 };
        let width = 0;
        let height = 0;
        let raf = 0;
        let dots = [];

        const resize = () => {
          width = canvas.width = window.innerWidth * window.devicePixelRatio;
          height = canvas.height = window.innerHeight * window.devicePixelRatio;
          canvas.style.width = window.innerWidth + "px";
          canvas.style.height = window.innerHeight + "px";
          const gap = 34 * window.devicePixelRatio;
          dots = [];
          for (let y = gap; y < height; y += gap) {
            for (let x = gap; x < width; x += gap) {
              dots.push({ x, y, base: 0.9 + Math.random() * 1.4 });
            }
          }
        };

        const move = (event) => {
          pointer.x = event.clientX * window.devicePixelRatio;
          pointer.y = event.clientY * window.devicePixelRatio;
        };

        const draw = () => {
          ctx.clearRect(0, 0, width, height);
          for (const dot of dots) {
            const dx = dot.x - pointer.x;
            const dy = dot.y - pointer.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const heat = Math.max(0, 1 - dist / (180 * window.devicePixelRatio));
            const leafTilt = Math.sin((dot.x + dot.y) * 0.002);
            ctx.beginPath();
            ctx.ellipse(dot.x, dot.y, dot.base + heat * 2.7, dot.base * 0.72 + heat * 1.4, leafTilt, 0, Math.PI * 2);
            ctx.fillStyle = heat > 0 ? `rgba(57, 170, 112, ${0.14 + heat * 0.38})` : "rgba(111, 71, 44, 0.08)";
            ctx.fill();
          }
          raf = requestAnimationFrame(draw);
        };

        resize();
        draw();
        window.addEventListener("resize", resize);
        window.addEventListener("pointermove", move);
        return () => {
          cancelAnimationFrame(raf);
          window.removeEventListener("resize", resize);
          window.removeEventListener("pointermove", move);
        };
      }, []);

      return <canvas ref={canvasRef} className="dot-field" aria-hidden="true" />;
    }

    function ShinyText({ children }) {
      return <span className="shiny-text">{children}</span>;
    }

    function SpotlightCard({ className = "", children }) {
      const ref = useRef(null);
      const onMove = (event) => {
        const rect = ref.current.getBoundingClientRect();
        ref.current.style.setProperty("--x", `${event.clientX - rect.left}px`);
        ref.current.style.setProperty("--y", `${event.clientY - rect.top}px`);
      };
      return (
        <div ref={ref} className={`spotlight ${className}`} onMouseMove={onMove}>
          {children}
        </div>
      );
    }

    function artifactUrl(path) {
      const normalized = path.replaceAll("\\", "/");
      const marker = "/runs/";
      const index = normalized.indexOf(marker);
      if (index >= 0) return normalized.slice(index);
      if (normalized.startsWith("runs/")) return "/" + normalized;
      return "";
    }

    function Metric({ label, value }) {
      return (
        <div className="metric">
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      );
    }

    function App() {
      const [text, setText] = useState(markdownSample);
      const [inputFormat, setInputFormat] = useState("text");
      const [projectName, setProjectName] = useState("演示 API");
      const [outputDir, setOutputDir] = useState("runs/web");
      const [execute, setExecute] = useState(true);
      const [result, setResult] = useState(null);
      const [status, setStatus] = useState("IDLE");
      const [error, setError] = useState("");
      const [running, setRunning] = useState(false);

      const statusLabels = {
        IDLE: "待运行",
        RUNNING: "运行中",
        PASS: "通过",
        FAIL: "失败",
        ERROR: "异常",
        GENERATED: "已生成"
      };
      const localizeSummary = (value) => {
        if (!value) return "准备就绪";
        const endpointMatch = value.match(/^Parsed (\d+) API endpoints covering methods: (.+)\.$/);
        if (endpointMatch) return `已解析 ${endpointMatch[1]} 个接口，覆盖方法：${endpointMatch[2]}。`;
        const textMatch = value.match(/^Parsed free-form requirement text with (\d+) characters\.$/);
        if (textMatch) return `已解析 ${textMatch[1]} 个字符的自由格式需求文本。`;
        return value;
      };

      const execution = result?.execution;
      const summary = localizeSummary(result?.suite?.analysis?.summary);
      const reportUrl = result?.html_report ? artifactUrl(result.html_report) : "";
      const reportPreview = reportUrl ? `${reportUrl}?t=${Date.now()}` : "";
      const statusClass = status === "PASS" ? "pass" : status === "FAIL" || status === "ERROR" ? "fail" : status === "RUNNING" ? "work" : "";

      const loadMarkdown = () => {
        setText(markdownSample);
        setInputFormat("text");
      };

      const loadOpenApi = () => {
        setText(openApiSample);
        setInputFormat("openapi");
      };

      const clearAll = () => {
        setText("");
        setResult(null);
        setError("");
        setStatus("IDLE");
      };

      const runAgent = async () => {
        setError("");
        setRunning(true);
        setStatus("RUNNING");
        try {
          const response = await fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text,
              source_name: "web-ui",
              project_name: projectName || "演示 API",
              output_dir: outputDir || "runs/web",
              execute,
              input_format: inputFormat
            })
          });
          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.detail || "请求失败");
          }
          setResult(data);
          setStatus(data.execution ? (data.execution.success ? "PASS" : "FAIL") : "GENERATED");
        } catch (err) {
          setError(err.message);
          setStatus("ERROR");
        } finally {
          setRunning(false);
        }
      };

      const endpoints = result?.suite?.analysis?.endpoints || [];
      const cases = result?.suite?.test_cases || [];

      return (
        <>
          <DotField />
          <div className="app-shell">
            <header className="topbar">
              <div className="brand">
                <div className="mark">AT</div>
                <div>
                  <h1>AI Test Agent</h1>
                  <p>测试开发作品集系统</p>
                </div>
              </div>
              <nav className="nav">
                <a href="/docs">接口文档</a>
                <a href="https://github.com/Whw12138/ai-test-agent" target="_blank" rel="noreferrer">GitHub</a>
              </nav>
            </header>

            <section className="hero">
              <div className="hero-main">
                <p className="kicker">岛屿手账风界面</p>
                <h2 className="hero-title">
                  把接口需求变成<ShinyText>可执行测试</ShinyText>
                </h2>
                <p className="hero-copy">
                  粘贴 Markdown 需求或 OpenAPI JSON，Agent 会自动提取接口契约、
                  设计测试用例、生成 pytest 代码、执行测试，并在页面内预览测试报告。
                </p>
                <div className="hero-actions">
                  <button className="primary-button" onClick={runAgent} disabled={running}>
                    {running ? "运行中..." : "运行 Agent"}
                  </button>
                  <button className="ghost-button" onClick={loadOpenApi}>载入 OpenAPI 示例</button>
                </div>
              </div>

              <SpotlightCard className="insight-panel">
                <div>
                  <h2>测试岛公告板</h2>
                  <p>一条适合放进作品集的闭环流程：输入需求、解析接口、生成用例、执行状态和最终报告。</p>
                </div>
                <div className="signal-grid">
                  <div className="signal"><strong>API</strong><span>接口解析</span></div>
                  <div className="signal"><strong>8+</strong><span>自动用例</span></div>
                  <div className="signal"><strong>CI</strong><span>pytest 就绪</span></div>
                </div>
              </SpotlightCard>
            </section>

            <section className="workspace">
              <SpotlightCard className="panel">
                <div className="panel-header">
                  <div>
                    <h2>需求输入区</h2>
                    <p>选择示例，或粘贴你自己的接口需求文档。</p>
                  </div>
                  <div className="tabs">
                    <button className={`tab-button ${inputFormat === "text" ? "active" : ""}`} onClick={loadMarkdown}>Markdown</button>
                    <button className={`tab-button ${inputFormat === "openapi" ? "active" : ""}`} onClick={loadOpenApi}>OpenAPI</button>
                    <button className="tab-button" onClick={clearAll}>清空</button>
                  </div>
                </div>
                <div className="panel-body">
                  <div className="control-row">
                    <div>
                      <label>项目名称</label>
                      <input value={projectName} onChange={(e) => setProjectName(e.target.value)} />
                    </div>
                    <div>
                      <label>输入格式</label>
                      <select value={inputFormat} onChange={(e) => setInputFormat(e.target.value)}>
                        <option value="auto">自动识别</option>
                        <option value="text">文本需求</option>
                        <option value="openapi">OpenAPI</option>
                      </select>
                    </div>
                    <div>
                      <label>输出目录</label>
                      <input value={outputDir} onChange={(e) => setOutputDir(e.target.value)} />
                    </div>
                  </div>
                  <label>需求内容</label>
                  <textarea value={text} onChange={(e) => setText(e.target.value)} spellCheck="false" />
                  <div className="run-row">
                    <label className="toggle">
                      <input type="checkbox" checked={execute} onChange={(e) => setExecute(e.target.checked)} />
                      执行生成的 pytest
                    </label>
                    <button className="primary-button" onClick={runAgent} disabled={running || text.trim().length === 0}>
                      {running ? "运行中..." : "生成报告"}
                    </button>
                  </div>
                </div>
              </SpotlightCard>

              <SpotlightCard className="panel">
                <div className="panel-header">
                  <div>
                    <h2>执行控制台</h2>
                    <p>{summary}</p>
                  </div>
                  <span className={`status-pill ${statusClass}`}>{statusLabels[status] || status}</span>
                </div>
                <div className="panel-body">
                  <div className="metric-grid">
                    <Metric label="用例总数" value={execution ? execution.total : cases.length} />
                    <Metric label="通过" value={execution ? execution.passed : 0} />
                    <Metric label="失败" value={execution ? execution.failed : 0} />
                    <Metric label="错误" value={execution ? execution.errors : 0} />
                    <Metric label="耗时" value={execution ? `${execution.duration_seconds.toFixed(2)}s` : "-"} />
                  </div>

                  <div className="result-grid">
                    <div className="mini-panel">
                      <h3>接口列表</h3>
                      {endpoints.length === 0 ? (
                        <div className="empty">运行 Agent 后，这里会展示解析出的 API 契约。</div>
                      ) : (
                        <table>
                          <thead><tr><th>方法</th><th>路径</th><th>成功状态码</th></tr></thead>
                          <tbody>
                            {endpoints.map((item, index) => (
                              <tr key={`${item.method}-${item.path}-${index}`}>
                                <td><span className={`method ${item.method.toLowerCase()}`}>{item.method}</span></td>
                                <td>{item.path}</td>
                                <td>{item.success_status}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      )}
                    </div>

                    <div className="mini-panel">
                      <h3>测试用例</h3>
                      {cases.length === 0 ? (
                        <div className="empty">生成的正向、异常和边界类用例会显示在这里。</div>
                      ) : (
                        <table>
                          <thead><tr><th>ID</th><th>请求</th><th>预期状态</th></tr></thead>
                          <tbody>
                            {cases.map((item) => (
                              <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.method} {item.path}</td>
                                <td>{item.expected_status}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      )}
                    </div>
                  </div>

                  <div className="report-bar">
                    <h3>报告预览</h3>
                    {reportUrl && <a className="ghost-button" href={reportPreview} target="_blank" rel="noreferrer">打开报告</a>}
                  </div>
                  {reportUrl ? (
                    <iframe src={reportPreview} title="生成的测试报告" />
                  ) : (
                    <div className="empty">运行完成后，这里会预览生成的 HTML 测试报告。</div>
                  )}
                  {error && <p className="error">{error}</p>}
                </div>
              </SpotlightCard>
            </section>
          </div>
        </>
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(<App />);
  </script>
</body>
</html>
"""
