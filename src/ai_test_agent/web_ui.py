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
      --sand: #f6e3af;
      --sea: #7cc9d8;
      --mint: #a7d9bd;
      --leaf-pattern: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%233c9f86' stroke-opacity='.18' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M18 24c16 2 25 10 27 27-15-2-25-11-27-27Z'/%3E%3Cpath d='M23 28c8 8 13 14 18 23M30 31c-1 7-1 13 0 18M37 37c-1 6-1 10 0 15'/%3E%3Cpath d='M78 78c14 1 23 9 25 24-14-1-23-9-25-24Z'/%3E%3Cpath d='M82 82c7 7 12 13 17 20M90 85c-1 6-1 11 0 16'/%3E%3Cpath d='M78 18c8 4 12 10 12 20-9-3-14-10-12-20Z'/%3E%3Cpath d='M19 86c6-3 13-1 18 5-7 4-14 3-18-5Z'/%3E%3C/g%3E%3Cg fill='%23e9cf72' fill-opacity='.16'%3E%3Ccircle cx='58' cy='24' r='3'/%3E%3Ccircle cx='105' cy='48' r='2'/%3E%3Ccircle cx='53' cy='92' r='2.5'/%3E%3C/g%3E%3C/svg%3E");
      --shadow: 0 18px 0 rgba(111, 71, 44, 0.1), 0 28px 60px rgba(82, 102, 70, 0.18);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        var(--leaf-pattern),
        radial-gradient(circle at 12% 8%, rgba(255, 248, 220, 0.88), transparent 18%),
        radial-gradient(circle at 86% 10%, rgba(134, 213, 218, 0.46), transparent 22%),
        radial-gradient(circle at 18% 92%, rgba(57, 170, 112, 0.26), transparent 26%),
        linear-gradient(180deg, var(--sky) 0%, #edf9e9 44%, #c9e9ab 100%);
      background-size: 120px 120px, auto, auto, auto, auto;
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
      height: 210px;
      background:
        radial-gradient(110px 34px at 52% 72%, rgba(255,255,255,0.76) 0 58%, transparent 60%),
        radial-gradient(circle at 12% 64%, rgba(255,255,255,0.9) 0 24px, transparent 25px),
        radial-gradient(circle at 17% 58%, rgba(255,255,255,0.86) 0 34px, transparent 35px),
        radial-gradient(circle at 72% 72%, rgba(255,255,255,0.72) 0 28px, transparent 29px),
        radial-gradient(circle at 78% 66%, rgba(255,255,255,0.74) 0 40px, transparent 41px);
      opacity: 0.78;
    }
    body::after {
      bottom: -72px;
      height: 320px;
      background:
        radial-gradient(54% 58% at 74% 28%, rgba(255, 233, 167, 0.52), transparent 64%),
        radial-gradient(60% 90% at 14% 0%, rgba(68, 167, 112, 0.42), transparent 64%),
        linear-gradient(180deg, transparent 0 18%, rgba(246, 227, 175, 0.58) 19% 35%, rgba(124, 201, 216, 0.34) 36% 100%);
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
    .mimo-shell {
      width: min(1680px, calc(100vw - 24px));
      padding: 10px 0 28px;
    }
    .desktop-topbar {
      display: grid;
      grid-template-columns: auto minmax(220px, 1fr) auto auto auto;
      align-items: center;
      gap: 10px;
      min-height: 56px;
      margin-bottom: 10px;
      padding: 8px 12px;
      border: 1px solid rgba(119, 100, 72, 0.16);
      border-radius: 22px 22px 10px 10px;
      background:
        linear-gradient(180deg, rgba(255, 253, 241, 0.94), rgba(255, 249, 229, 0.82)),
        repeating-linear-gradient(90deg, rgba(82, 179, 165, 0.055) 0 12px, transparent 12px 28px);
      box-shadow: 0 10px 28px rgba(73, 84, 66, 0.12);
      backdrop-filter: blur(18px);
    }
    .traffic {
      display: flex;
      gap: 8px;
      padding: 0 8px;
    }
    .traffic span {
      width: 13px;
      height: 13px;
      border-radius: 999px;
      box-shadow: inset 0 -2px 0 rgba(0,0,0,0.08);
    }
    .traffic span:nth-child(1) { background: #ff6f62; }
    .traffic span:nth-child(2) { background: #f6c64b; }
    .traffic span:nth-child(3) { background: #55c86f; }
    .top-chip,
    .desktop-nav a,
    .desktop-nav button {
      min-height: 38px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 999px;
      background: rgba(255, 253, 245, 0.88);
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.08);
    }
    .top-chip {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      width: fit-content;
      padding: 0 13px 0 8px;
      color: #4d4a3d;
      font-size: 13px;
      font-weight: 800;
    }
    .top-chip em {
      color: #7d7a69;
      font-style: normal;
      font-weight: 700;
    }
    .tiny-avatar {
      display: grid;
      place-items: center;
      width: 26px;
      height: 26px;
      border-radius: 48% 52% 46% 54%;
      background: linear-gradient(145deg, #6bd38f, #1aa892);
      color: #fff8df;
      font-size: 12px;
      font-weight: 900;
    }
    .model-stack {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .model-stack .top-chip {
      padding: 0 14px;
    }
    .clock {
      min-width: 148px;
      text-align: center;
      color: #9b947e;
      font-size: 13px;
      font-weight: 800;
    }
    .desktop-nav {
      display: inline-flex;
      justify-content: flex-end;
      gap: 8px;
    }
    .desktop-nav a {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 13px;
      color: #574f3f;
      font-size: 13px;
      font-weight: 800;
    }
    .desktop-frame {
      position: relative;
      display: grid;
      grid-template-columns: 320px minmax(520px, 1fr) 330px;
      gap: 12px;
      min-height: calc(100vh - 92px);
      padding: 12px;
      border: 1px solid rgba(119, 100, 72, 0.16);
      border-radius: 10px 10px 26px 26px;
      background:
        linear-gradient(90deg, rgba(236, 250, 241, 0.72), rgba(255, 253, 242, 0.96) 22%, rgba(255, 250, 232, 0.96) 74%, rgba(245, 250, 236, 0.8)),
        radial-gradient(circle at 52% 24%, rgba(255, 234, 122, 0.18), transparent 24%);
      box-shadow: 0 24px 70px rgba(88, 94, 72, 0.16);
      backdrop-filter: blur(20px);
      overflow: hidden;
    }
    .desktop-frame::before {
      content: "";
      position: absolute;
      left: 24px;
      right: 24px;
      bottom: -28px;
      height: 150px;
      border-radius: 48% 52% 0 0 / 38% 36% 0 0;
      background:
        radial-gradient(20px 10px at 18% 58%, rgba(255,255,255,0.58) 0 70%, transparent 72%),
        radial-gradient(24px 12px at 64% 52%, rgba(255,255,255,0.5) 0 70%, transparent 72%),
        linear-gradient(180deg, rgba(246, 227, 175, 0.48) 0 28%, rgba(120, 198, 214, 0.2) 29% 44%, rgba(61, 163, 139, 0.18) 45% 100%);
      pointer-events: none;
      opacity: 0.7;
    }
    .desktop-frame > * {
      position: relative;
      z-index: 1;
    }
    .side-dock,
    .workbench,
    .asset-dock {
      min-width: 0;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 22px;
      background: rgba(255, 251, 233, 0.74);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.72), 0 10px 24px rgba(93, 95, 72, 0.1);
    }
    .side-dock,
    .asset-dock {
      padding: 14px;
    }
    .dock-search {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      min-height: 42px;
      margin-bottom: 14px;
      padding: 0 12px;
      border: 1px solid rgba(119, 100, 72, 0.18);
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.86);
      color: #8c846d;
      font-size: 13px;
      box-shadow: inset 0 2px 8px rgba(119, 100, 72, 0.05);
    }
    .dock-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin: 14px 0 8px;
      color: #645d4b;
      font-size: 13px;
      font-weight: 900;
    }
    .dock-title span {
      color: #8a836d;
      font-size: 12px;
      font-weight: 800;
    }
    .ability-tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 12px;
    }
    .ability-tabs button,
    .mimo-tab,
    .mini-action {
      min-height: 40px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.84);
      color: #5c5544;
      font-weight: 900;
      box-shadow: 0 4px 0 rgba(119, 100, 72, 0.08);
    }
    .ability-tabs button.active,
    .mimo-tab.active,
    .mini-action.active {
      background: linear-gradient(180deg, #46cbbd, #25b9aa);
      color: #ffffff;
      border-color: rgba(37, 185, 170, 0.34);
      box-shadow: 0 5px 0 rgba(32, 139, 127, 0.18);
    }
    .side-card {
      position: relative;
      display: grid;
      grid-template-columns: 46px 1fr;
      gap: 10px;
      align-items: center;
      min-height: 70px;
      margin-bottom: 10px;
      padding: 12px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-left: 5px solid rgba(67, 200, 191, 0.75);
      border-radius: 18px;
      background: rgba(255, 253, 244, 0.82);
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.08);
    }
    .side-card strong {
      display: block;
      color: #3a382e;
      font-size: 14px;
    }
    .side-card span {
      display: block;
      margin-top: 3px;
      color: #7a725f;
      font-size: 12px;
      line-height: 1.35;
    }
    .asset-icon,
    .work-avatar {
      display: grid;
      place-items: center;
      border-radius: 18px;
      background:
        radial-gradient(circle at 30% 24%, rgba(255,255,255,0.72), transparent 35%),
        linear-gradient(145deg, #c9f4d8, #7bdacb);
      color: #2a7f72;
      font-weight: 900;
    }
    .island-icon {
      position: relative;
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      overflow: hidden;
      border: 2px solid rgba(255, 253, 244, 0.78);
      border-radius: 17px 19px 15px 18px;
      background:
        radial-gradient(circle at 30% 22%, rgba(255,255,255,0.74), transparent 34%),
        linear-gradient(145deg, #c9f4d8, #74d9ca);
      box-shadow: 0 5px 0 rgba(119, 100, 72, 0.12), inset 0 -4px 0 rgba(36, 139, 124, 0.08);
    }
    .island-icon.large {
      width: 54px;
      height: 54px;
      border-radius: 21px 24px 19px 23px;
    }
    .island-icon::before,
    .island-icon::after,
    .island-icon span {
      content: "";
      position: absolute;
      display: block;
    }
    .island-icon.api::before {
      width: 28px;
      height: 20px;
      border-radius: 7px 8px 6px 9px;
      background:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.12) 0 4px, rgba(88,48,24,0.1) 4px 7px),
        linear-gradient(180deg, #bd8150, #8d5b36);
      box-shadow: 0 3px 0 rgba(107, 66, 38, 0.24);
      transform: rotate(-6deg);
    }
    .island-icon.api::after {
      width: 20px;
      height: 2px;
      border-radius: 999px;
      background: rgba(255, 247, 209, 0.95);
      box-shadow: 0 6px 0 rgba(255, 247, 209, 0.95);
      transform: rotate(-6deg);
    }
    .island-icon.api span {
      width: 5px;
      height: 5px;
      right: 8px;
      bottom: 8px;
      border-radius: 999px;
      background: #f4d76a;
      box-shadow: -8px -8px 0 #f4d76a, -16px -2px 0 #f4d76a;
    }
    .island-icon.ci {
      background:
        radial-gradient(circle at 30% 22%, rgba(255,255,255,0.74), transparent 34%),
        linear-gradient(145deg, #f8df7d, #53c6a6);
    }
    .island-icon.ci::before {
      width: 23px;
      height: 23px;
      border: 4px solid #fff8dc;
      border-radius: 50%;
      box-shadow: inset 0 0 0 4px rgba(43, 134, 116, 0.78);
    }
    .island-icon.ci::after {
      width: 30px;
      height: 5px;
      border-radius: 999px;
      background: #2f8c7b;
      transform: rotate(-35deg);
    }
    .island-icon.asset::before {
      width: 29px;
      height: 25px;
      border-radius: 50% 50% 45% 45%;
      background:
        radial-gradient(circle at 20% 18%, rgba(255,255,255,0.84) 0 8px, transparent 9px),
        repeating-radial-gradient(circle at 50% 84%, rgba(255,255,255,0.58) 0 2px, transparent 2px 5px),
        linear-gradient(145deg, #f7d88a, #eaa06f);
      transform: rotate(8deg);
    }
    .island-icon.asset::after {
      width: 26px;
      height: 7px;
      bottom: 10px;
      border-radius: 999px;
      background: rgba(121, 83, 45, 0.18);
    }
    .island-icon.context::before {
      width: 30px;
      height: 24px;
      border-radius: 7px;
      background:
        linear-gradient(90deg, rgba(255,255,255,0.34) 0 33%, transparent 33% 36%, rgba(255,255,255,0.24) 36% 66%, transparent 66% 69%, rgba(255,255,255,0.18) 69%),
        linear-gradient(145deg, #fff5be, #8fd9c0);
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.12);
      transform: rotate(-4deg);
    }
    .island-icon.context::after {
      width: 9px;
      height: 9px;
      top: 10px;
      left: 20px;
      border-radius: 50% 50% 50% 0;
      background: #e46f62;
      transform: rotate(-45deg);
    }
    .island-icon.task::before {
      width: 3px;
      height: 28px;
      left: 15px;
      top: 8px;
      border-radius: 999px;
      background: #7b5b3b;
    }
    .island-icon.task::after {
      width: 22px;
      height: 16px;
      left: 17px;
      top: 9px;
      border-radius: 5px 9px 8px 4px;
      background:
        radial-gradient(circle at 70% 40%, rgba(255,255,255,0.44), transparent 30%),
        linear-gradient(145deg, #ff8f63, #f1c85b);
      transform: rotate(3deg);
    }
    .island-icon.agent::before {
      width: 32px;
      height: 26px;
      border-radius: 45% 55% 50% 50%;
      background:
        radial-gradient(circle at 32% 42%, #2d7d72 0 3px, transparent 4px),
        radial-gradient(circle at 66% 42%, #2d7d72 0 3px, transparent 4px),
        linear-gradient(145deg, #fff5c8 0 45%, #8edbd1 46% 100%);
      box-shadow: 0 4px 0 rgba(43, 121, 109, 0.16);
    }
    .island-icon.agent::after {
      width: 24px;
      height: 7px;
      bottom: 8px;
      border-radius: 999px;
      background: rgba(45, 125, 114, 0.22);
    }
    .island-icon.agent span {
      width: 18px;
      height: 10px;
      top: 8px;
      left: 10px;
      border-radius: 9px 9px 5px 5px;
      background:
        radial-gradient(circle at 72% 38%, #f4d76a 0 3px, transparent 4px),
        linear-gradient(145deg, #47c7b6, #2c9183);
      transform: rotate(-8deg);
    }
    .island-icon.run::before {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: linear-gradient(145deg, #62c8ff, #4dc7a0);
      box-shadow: inset 0 -3px 0 rgba(20, 99, 95, 0.14);
    }
    .island-icon.run::after {
      width: 0;
      height: 0;
      border-top: 7px solid transparent;
      border-bottom: 7px solid transparent;
      border-left: 12px solid #fff8dc;
      left: 18px;
      top: 14px;
    }
    .work-heading .island-icon.large {
      justify-self: center;
    }
    .asset-card.feature .island-icon {
      margin: 0 auto 12px;
    }
    .side-card.muted {
      border-left-color: rgba(142, 126, 218, 0.6);
      opacity: 0.86;
    }
    .workbench {
      display: flex;
      flex-direction: column;
      gap: 14px;
      padding: 18px;
      background:
        linear-gradient(180deg, rgba(255, 253, 242, 0.88), rgba(255, 250, 232, 0.66));
    }
    .work-heading {
      display: grid;
      grid-template-columns: 54px 1fr auto;
      gap: 12px;
      align-items: center;
      padding: 12px;
      border-radius: 22px;
      background: rgba(255, 253, 244, 0.72);
    }
    .work-avatar {
      width: 52px;
      height: 52px;
      border-radius: 20px;
      font-size: 18px;
    }
    .work-heading p,
    .work-heading h1 {
      margin: 0;
    }
    .work-heading p {
      color: #27a799;
      font-size: 13px;
      font-weight: 900;
    }
    .work-heading h1 {
      margin-top: 3px;
      color: #433927;
      font-size: 26px;
      line-height: 1.1;
    }
    .work-heading small {
      display: block;
      margin-top: 5px;
      color: #827a66;
      line-height: 1.4;
    }
    .flow-strip {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      padding: 8px;
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.75);
      border: 1px solid rgba(119, 100, 72, 0.12);
    }
    .flow-strip span {
      min-width: 0;
      padding: 8px 10px;
      border-radius: 999px;
      color: #726b58;
      font-size: 12px;
      font-weight: 900;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .flow-strip .active {
      background: #d7f6ef;
      color: #158a7e;
    }
    .mimo-tabs {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }
    .task-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .task-card {
      min-height: 88px;
      padding: 14px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 20px;
      background: rgba(255, 253, 244, 0.78);
      color: #463d2f;
      text-align: left;
      box-shadow: 0 4px 0 rgba(119, 100, 72, 0.08);
    }
    .task-card strong {
      display: block;
      margin-bottom: 5px;
      color: #2d8f80;
      font-size: 15px;
    }
    .task-card span {
      color: #7b735f;
      font-size: 12px;
      line-height: 1.45;
    }
    .task-card.primary-task {
      background: linear-gradient(160deg, #38c4b4, #2fc5a4);
      color: #fff;
    }
    .task-card.primary-task strong,
    .task-card.primary-task span {
      color: #fff;
    }
    .draft-card,
    .console-card {
      border: 1px solid rgba(119, 100, 72, 0.15);
      border-radius: 22px;
      background: rgba(255, 253, 244, 0.8);
      box-shadow: 0 4px 0 rgba(119, 100, 72, 0.08);
      overflow: hidden;
    }
    .draft-head,
    .console-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 13px 14px;
      border-bottom: 1px dashed rgba(119, 100, 72, 0.16);
    }
    .draft-head strong,
    .console-head strong {
      color: #3f382d;
      font-size: 15px;
    }
    .draft-head span,
    .console-head span {
      color: #8a826d;
      font-size: 12px;
    }
    .draft-body,
    .console-body {
      padding: 14px;
    }
    .asset-tabs {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-bottom: 12px;
    }
    .asset-tabs span {
      display: grid;
      place-items: center;
      min-height: 34px;
      border-radius: 999px;
      background: rgba(255,253,244,0.74);
      color: #716955;
      font-size: 12px;
      font-weight: 900;
    }
    .asset-tabs .active {
      background: #d8f6ed;
      color: #1c8a7c;
    }
    .asset-card {
      margin-bottom: 12px;
      padding: 14px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 20px;
      background: rgba(255, 253, 244, 0.78);
      box-shadow: 0 4px 0 rgba(119, 100, 72, 0.07);
    }
    .asset-card h3 {
      margin: 0 0 6px;
      color: #41392d;
      font-size: 15px;
    }
    .asset-card p {
      margin: 0;
      color: #807762;
      font-size: 13px;
      line-height: 1.55;
    }
    .island-postcard {
      position: relative;
      min-height: 150px;
      margin-bottom: 12px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 22px;
      overflow: hidden;
      background:
        radial-gradient(80px 34px at 76% 28%, rgba(255,255,255,0.82) 0 42%, transparent 44%),
        radial-gradient(54px 24px at 64% 30%, rgba(255,255,255,0.72) 0 44%, transparent 46%),
        linear-gradient(180deg, #90d4ec 0 44%, #f8e6b8 45% 62%, #71cbd6 63% 100%);
      box-shadow: 0 4px 0 rgba(119, 100, 72, 0.08);
    }
    .island-postcard::before {
      content: "";
      position: absolute;
      left: -18px;
      right: -18px;
      bottom: 36px;
      height: 42px;
      border-radius: 50%;
      background:
        radial-gradient(16px 8px at 24% 48%, rgba(255,255,255,0.82) 0 70%, transparent 72%),
        radial-gradient(24px 10px at 62% 54%, rgba(255,255,255,0.74) 0 70%, transparent 72%),
        rgba(255,255,255,0.52);
    }
    .island-postcard::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 40px;
      background:
        var(--leaf-pattern),
        linear-gradient(180deg, #7ccf80, #5ebf74);
      background-size: 86px 86px, auto;
    }
    .wood-sign {
      position: absolute;
      left: 16px;
      top: 18px;
      z-index: 1;
      padding: 8px 12px;
      border-radius: 10px 12px 9px 13px;
      background:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.08) 0 5px, rgba(95, 54, 28, 0.08) 5px 9px),
        linear-gradient(180deg, #bd8150, #8c5b37);
      color: #fff5ce;
      font-size: 14px;
      font-weight: 900;
      box-shadow: 0 5px 0 rgba(95, 54, 28, 0.22);
    }
    .postcard-chip {
      position: absolute;
      right: 14px;
      bottom: 12px;
      z-index: 1;
      min-height: 30px;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.88);
      color: #267b70;
      font-size: 12px;
      font-weight: 900;
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.12);
    }
    .island-stamp {
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border-radius: 16px 18px 15px 19px;
      background:
        radial-gradient(circle at 32% 24%, rgba(255,255,255,0.72), transparent 36%),
        linear-gradient(145deg, #f7d86b, #35bda7);
      color: #fffaf0;
      font-size: 18px;
      font-weight: 900;
      box-shadow: 0 5px 0 rgba(119, 100, 72, 0.12);
    }
    .asset-card.feature {
      min-height: 210px;
      display: grid;
      place-items: center;
      text-align: center;
      border-left: 5px solid #8e86e8;
      background:
        radial-gradient(circle at 50% 22%, rgba(67,200,191,0.22), transparent 28%),
        rgba(255, 253, 244, 0.78);
    }
    .asset-icon {
      width: 54px;
      height: 54px;
      margin: 0 auto 12px;
      font-size: 18px;
    }
    .asset-metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }
    .asset-metrics div {
      min-height: 58px;
      padding: 10px;
      border-radius: 14px;
      background: rgba(255, 253, 244, 0.78);
      border: 1px solid rgba(119, 100, 72, 0.1);
      color: #453e32;
      font-weight: 900;
    }
    .asset-metrics span {
      display: block;
      margin-top: 4px;
      color: #807762;
      font-size: 12px;
      font-weight: 800;
    }
    .console-card .result-grid {
      margin-bottom: 14px;
    }
    .console-toolbar,
    .artifact-actions,
    .record-meta {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
    .console-toolbar {
      justify-content: flex-end;
    }
    .artifact-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 34px;
      padding: 0 11px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.86);
      color: #537162;
      font-size: 12px;
      font-weight: 900;
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.08);
    }
    .artifact-link.primary {
      background: #d8f6ed;
      color: #168a7d;
      border-color: rgba(37, 185, 170, 0.28);
    }
    .platform-tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 14px;
      padding-bottom: 4px;
      overflow-x: auto;
    }
    .platform-tab {
      min-width: max-content;
      min-height: 38px;
      padding: 0 13px;
      border: 1px solid rgba(119, 100, 72, 0.14);
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.78);
      color: #756c59;
      font-size: 12px;
      font-weight: 900;
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.07);
    }
    .platform-tab.active {
      background: linear-gradient(180deg, #46cbbd, #25b9aa);
      color: #ffffff;
      border-color: rgba(37, 185, 170, 0.34);
      box-shadow: 0 4px 0 rgba(32, 139, 127, 0.18);
    }
    .tab-pane {
      min-height: 260px;
    }
    .pane-heading {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }
    .pane-heading h3 {
      margin: 0;
      color: #3f382d;
      font-size: 15px;
    }
    .pane-heading p {
      margin: 4px 0 0;
      color: #847b66;
      font-size: 12px;
      line-height: 1.55;
    }
    .table-wrap {
      overflow-x: auto;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-radius: 16px;
      background: rgba(255, 253, 244, 0.6);
    }
    .table-wrap table {
      min-width: 620px;
    }
    .test-point-list {
      display: grid;
      gap: 8px;
    }
    .test-point {
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
      padding: 11px;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-radius: 16px;
      background: rgba(255, 253, 244, 0.72);
    }
    .point-index {
      display: grid;
      place-items: center;
      width: 32px;
      height: 32px;
      border-radius: 13px;
      background: #d8f6ed;
      color: #1c8a7c;
      font-size: 12px;
      font-weight: 900;
    }
    .test-point strong {
      display: block;
      color: #4a4134;
      font-size: 13px;
    }
    .test-point p {
      margin: 4px 0 0;
      color: #817762;
      font-size: 12px;
      line-height: 1.5;
    }
    .risk-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 52px;
      min-height: 28px;
      padding: 0 9px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 900;
    }
    .risk-badge.low { background: #d8f6ed; color: #168a7d; }
    .risk-badge.medium { background: #fff0ba; color: #9a6a0c; }
    .risk-badge.high { background: #ffe1dc; color: #b0493c; }
    .insight-box {
      margin-bottom: 12px;
      padding: 13px;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-left: 5px solid #e8bf4f;
      border-radius: 16px;
      background: rgba(255, 248, 214, 0.62);
    }
    .insight-box.pass {
      border-left-color: #43c8bf;
      background: rgba(216, 246, 237, 0.58);
    }
    .insight-box h3 {
      margin: 0;
      color: #4c4334;
      font-size: 14px;
    }
    .insight-box p {
      margin: 6px 0 0;
      color: #796e59;
      font-size: 12px;
      line-height: 1.6;
    }
    .failure-list {
      display: grid;
      gap: 8px;
      margin-bottom: 12px;
    }
    .failure-item {
      padding: 11px;
      border: 1px solid rgba(214, 93, 100, 0.2);
      border-radius: 14px;
      background: rgba(255, 225, 220, 0.56);
    }
    .failure-item strong {
      display: block;
      color: #a44148;
      font-size: 12px;
    }
    .failure-item p {
      margin: 5px 0 0;
      color: #7f5c59;
      font-size: 12px;
      line-height: 1.5;
      white-space: pre-wrap;
    }
    .bug-summary-list {
      display: grid;
      gap: 10px;
    }
    .bug-summary-card {
      padding: 12px;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-left: 5px solid #e8bf4f;
      border-radius: 16px;
      background: rgba(255, 253, 244, 0.74);
      box-shadow: 0 3px 0 rgba(119, 100, 72, 0.06);
    }
    .bug-summary-card.high {
      border-left-color: #ef7770;
      background: rgba(255, 225, 220, 0.48);
    }
    .bug-summary-card.medium {
      border-left-color: #e8bf4f;
      background: rgba(255, 248, 214, 0.5);
    }
    .bug-summary-card.low {
      border-left-color: #43c8bf;
      background: rgba(216, 246, 237, 0.48);
    }
    .bug-summary-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }
    .bug-summary-head strong {
      display: block;
      color: #4b4031;
      font-size: 13px;
      line-height: 1.35;
    }
    .bug-summary-card p {
      margin: 6px 0 0;
      color: #7b715d;
      font-size: 12px;
      line-height: 1.55;
    }
    .bug-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }
    .bug-meta span {
      min-height: 26px;
      padding: 5px 8px;
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.78);
      color: #786c59;
      font-size: 11px;
      font-weight: 900;
    }
    .bug-severity {
      min-width: 54px;
      min-height: 27px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 900;
      white-space: nowrap;
    }
    .bug-severity.high { background: #ffe1dc; color: #b0493c; }
    .bug-severity.medium { background: #fff0ba; color: #9a6a0c; }
    .bug-severity.low { background: #d8f6ed; color: #168a7d; }
    .mindmap-preview {
      min-height: 300px;
      padding: 16px;
      overflow: auto;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-radius: 18px;
      background:
        linear-gradient(90deg, rgba(67, 200, 191, 0.13) 1px, transparent 1px),
        linear-gradient(180deg, rgba(67, 200, 191, 0.11) 1px, transparent 1px),
        rgba(255, 253, 244, 0.72);
      background-size: 34px 34px;
    }
    .mindmap-tree {
      display: grid;
      gap: 12px;
    }
    .mindmap-root {
      width: max-content;
      max-width: 100%;
      padding: 10px 14px;
      border: 3px solid rgba(255,253,244,0.98);
      border-radius: 999px;
      background: linear-gradient(135deg, #28164f, #5c2d8b 62%, #ffd24a);
      color: #fff8dc;
      font-weight: 900;
      box-shadow: 0 5px 0 rgba(66, 35, 106, 0.22);
    }
    .mindmap-branches {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .mindmap-branch {
      padding: 12px;
      border: 1px solid rgba(119, 100, 72, 0.12);
      border-radius: 16px;
      background: rgba(255, 253, 244, 0.82);
    }
    .mindmap-branch strong {
      color: #2d8f80;
      font-size: 13px;
    }
    .mindmap-branch ul {
      margin: 8px 0 0;
      padding-left: 18px;
      color: #756b58;
      font-size: 12px;
      line-height: 1.65;
    }
    .execution-log {
      max-height: 280px;
      margin: 0;
      padding: 13px;
      overflow: auto;
      border-radius: 15px;
      background: #31423a;
      color: #f6f3dd;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 12px;
      line-height: 1.55;
      white-space: pre-wrap;
    }
    .record-meta {
      margin-bottom: 12px;
    }
    .record-meta span {
      min-height: 32px;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(255, 253, 244, 0.8);
      color: #766d5b;
      font-size: 12px;
      font-weight: 800;
    }
    .artifact-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }
    .artifact-grid .artifact-link {
      min-height: 44px;
      border-radius: 14px;
    }
    /* Sticker button layer inspired by island UI, without using copyrighted assets. */
    .ability-tabs button,
    .mimo-tab,
    .mini-action,
    .platform-tab,
    .artifact-link,
    .task-card,
    .ghost-button {
      position: relative;
      overflow: hidden;
      border-width: 2px;
      border-style: solid;
      border-color: rgba(255, 253, 244, 0.94);
      outline: 1px solid rgba(107, 78, 55, 0.11);
      background:
        radial-gradient(circle at 22% 20%, rgba(255, 255, 255, 0.78), transparent 23%),
        linear-gradient(180deg, rgba(255, 253, 244, 0.98), rgba(255, 246, 221, 0.9));
      box-shadow:
        0 4px 0 rgba(110, 87, 55, 0.14),
        0 10px 18px rgba(79, 58, 38, 0.06);
    }
    .ability-tabs button,
    .mimo-tab,
    .mini-action,
    .platform-tab,
    .artifact-link {
      padding-left: 28px;
    }
    .artifact-link {
      white-space: nowrap;
    }
    .ability-tabs button::before,
    .mimo-tab::before,
    .mini-action:not(.active)::before,
    .platform-tab::before,
    .artifact-link:not(.primary)::before {
      content: "";
      position: absolute;
      left: 10px;
      top: 50%;
      width: 9px;
      height: 9px;
      pointer-events: none;
      transform: translateY(-50%) rotate(18deg);
      background: #43c8bf;
      clip-path: polygon(50% 0, 62% 34%, 98% 34%, 68% 55%, 80% 91%, 50% 70%, 20% 91%, 32% 55%, 2% 34%, 38% 34%);
      opacity: 0.62;
      filter: drop-shadow(0 1px 0 rgba(37, 133, 121, 0.16));
    }
    .primary-button,
    .task-card.primary-task,
    .mini-action.active,
    .artifact-link.primary {
      position: relative;
      isolation: isolate;
      overflow: hidden;
      border: 3px solid rgba(255, 253, 244, 0.98);
      outline: 2px solid rgba(74, 35, 103, 0.12);
      background:
        radial-gradient(circle at 16% 17%, rgba(255, 255, 255, 0.42), transparent 24%),
        linear-gradient(135deg, #28164f 0%, #3a1d67 40%, #5c2d8b 64%, #f1a13d 65%, #ffd24a 100%);
      color: #fff8dc;
      text-shadow: 0 1px 0 rgba(49, 24, 83, 0.2);
      box-shadow:
        0 5px 0 rgba(66, 35, 106, 0.28),
        0 15px 24px rgba(75, 48, 112, 0.18);
    }
    .primary-button,
    .mini-action.active,
    .artifact-link.primary {
      min-height: 40px;
      padding-right: 40px;
    }
    .artifact-link.primary {
      padding-left: 16px;
      padding-right: 34px;
    }
    .artifact-grid .artifact-link.primary {
      padding-left: 10px;
      padding-right: 28px;
      font-size: 11px;
    }
    .primary-button::before,
    .mini-action.active::before,
    .artifact-link.primary::before {
      content: "";
      position: absolute;
      right: 15px;
      top: 50%;
      width: 15px;
      height: 15px;
      pointer-events: none;
      transform: translateY(-50%) rotate(10deg);
      background: #ffd53f;
      clip-path: polygon(50% 0, 62% 34%, 98% 34%, 68% 55%, 80% 91%, 50% 70%, 20% 91%, 32% 55%, 2% 34%, 38% 34%);
      filter: drop-shadow(0 1px 0 rgba(93, 47, 18, 0.24));
    }
    .artifact-link.primary::before {
      right: 10px;
      width: 13px;
      height: 13px;
    }
    .task-card.primary-task {
      padding-right: 58px;
    }
    .task-card.primary-task::before {
      content: "";
      position: absolute;
      right: 14px;
      top: 13px;
      width: 20px;
      height: 20px;
      pointer-events: none;
      transform: rotate(14deg);
      background: #ffd53f;
      clip-path: polygon(50% 0, 62% 34%, 98% 34%, 68% 55%, 80% 91%, 50% 70%, 20% 91%, 32% 55%, 2% 34%, 38% 34%);
      filter: drop-shadow(0 1px 0 rgba(93, 47, 18, 0.22));
    }
    .task-card.primary-task::after {
      content: "";
      position: absolute;
      right: 14px;
      bottom: 14px;
      width: 23px;
      height: 23px;
      pointer-events: none;
      border: 3px solid rgba(255, 184, 33, 0.94);
      border-radius: 999px;
      background:
        radial-gradient(circle, #ffe477 0 34%, #ffb230 36% 58%, #e87828 61% 100%);
      box-shadow: inset 0 0 0 2px rgba(255, 249, 215, 0.72);
    }
    .task-card strong,
    .task-card span {
      position: relative;
      z-index: 1;
    }
    .ability-tabs button.active,
    .mimo-tab.active,
    .platform-tab.active {
      padding-right: 28px;
      border-color: rgba(255, 253, 244, 0.98);
      outline: 2px solid rgba(37, 185, 170, 0.13);
      background:
        radial-gradient(circle at 20% 18%, rgba(255, 255, 255, 0.64), transparent 24%),
        linear-gradient(145deg, #65dfd0, #28bdaa);
      box-shadow:
        0 5px 0 rgba(32, 139, 127, 0.18),
        0 14px 20px rgba(45, 165, 151, 0.12);
    }
    .ability-tabs button.active::after,
    .mimo-tab.active::after,
    .platform-tab.active::after {
      content: "";
      position: absolute;
      right: 10px;
      top: 50%;
      width: 10px;
      height: 10px;
      pointer-events: none;
      border: 2px solid rgba(255, 246, 219, 0.9);
      border-radius: 999px;
      background: #ffd14b;
      transform: translateY(-50%);
      box-shadow: inset 0 0 0 1px rgba(232, 144, 34, 0.46);
    }
    .task-card:not(.primary-task):hover,
    .ability-tabs button:hover,
    .mimo-tab:hover,
    .mini-action:hover,
    .platform-tab:hover,
    .artifact-link:hover,
    .ghost-button:hover,
    .primary-button:hover {
      transform: translateY(-1px) rotate(-0.2deg);
      box-shadow:
        0 6px 0 rgba(110, 87, 55, 0.13),
        0 14px 22px rgba(79, 58, 38, 0.08);
    }
    .primary-button:hover,
    .task-card.primary-task:hover,
    .mini-action.active:hover,
    .artifact-link.primary:hover {
      box-shadow:
        0 7px 0 rgba(66, 35, 106, 0.25),
        0 18px 28px rgba(75, 48, 112, 0.18);
    }
    .primary-button:disabled,
    .task-card:disabled,
    .mini-action:disabled {
      cursor: not-allowed;
      filter: saturate(0.72);
      opacity: 0.62;
      transform: none;
    }
    @media (max-width: 1080px) {
      .desktop-topbar { grid-template-columns: auto 1fr; }
      .model-stack, .clock { display: none; }
      .desktop-nav { justify-content: flex-start; }
      .desktop-frame { grid-template-columns: 1fr; }
      .side-dock, .asset-dock { order: initial; }
      .hero, .workspace { grid-template-columns: 1fr; }
      .control-row, .result-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .mimo-shell { width: min(100vw - 12px, 1480px); padding-top: 8px; }
      .desktop-topbar { border-radius: 20px; }
      .desktop-nav { grid-column: 1 / -1; }
      .desktop-frame { padding: 8px; border-radius: 20px; }
      .workbench, .side-dock, .asset-dock { padding: 12px; border-radius: 20px; }
      .work-heading { grid-template-columns: 46px 1fr; }
      .work-heading .mini-action { grid-column: 1 / -1; }
      .flow-strip, .mimo-tabs, .task-grid, .asset-metrics { grid-template-columns: 1fr 1fr; }
      .hero-main { padding: 20px; }
      .metric-grid, .signal-grid { grid-template-columns: 1fr 1fr; }
      .artifact-grid { grid-template-columns: 1fr; }
      .mindmap-branches { grid-template-columns: 1fr; }
      .test-point { grid-template-columns: 34px minmax(0, 1fr); }
      .test-point .risk-badge { grid-column: 2; justify-self: start; }
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

    function IslandIcon({ type, label, large = false }) {
      return <span className={`island-icon ${type} ${large ? "large" : ""}`} role="img" aria-label={label}><span></span></span>;
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
      const [clockText, setClockText] = useState("");
      const [activeResultTab, setActiveResultTab] = useState("points");

      useEffect(() => {
        const updateClock = () => {
          const now = new Date();
          const weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
          const hours = String(now.getHours()).padStart(2, "0");
          const minutes = String(now.getMinutes()).padStart(2, "0");
          setClockText(`${weekdays[now.getDay()]} ${now.getMonth() + 1}/${now.getDate()} ${hours}:${minutes}`);
        };
        updateClock();
        const timer = setInterval(updateClock, 30000);
        return () => clearInterval(timer);
      }, []);

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
          setActiveResultTab("points");
        } catch (err) {
          setError(err.message);
          setStatus("ERROR");
        } finally {
          setRunning(false);
        }
      };

      const endpoints = result?.suite?.analysis?.endpoints || [];
      const testPoints = result?.suite?.analysis?.test_points || [];
      const cases = result?.suite?.test_cases || [];
      const failures = execution?.failures || [];
      const passRate = execution?.total ? `${Math.round((execution.passed / execution.total) * 100)}%` : "-";
      const suiteUrl = result ? artifactUrl(`${outputDir}/suite.json`) : "";
      const testFileUrl = result?.test_file ? artifactUrl(result.test_file) : "";
      const markdownReportUrl = result?.markdown_report ? artifactUrl(result.markdown_report) : "";
      const junitUrl = execution?.junit_xml ? artifactUrl(execution.junit_xml) : "";
      const bugSummaries = result?.bug_summaries || [];
      const bugSummaryUrl = result?.bug_summary_file ? artifactUrl(result.bug_summary_file) : "";
      const mindmapUrl = result?.mindmap_file ? artifactUrl(result.mindmap_file) : "";
      const xmindUrl = result?.xmind_file ? artifactUrl(result.xmind_file) : "";
      const riskLabels = { low: "低风险", medium: "中风险", high: "高风险" };
      const categoryLabels = { positive: "正向", boundary: "边界", negative: "异常", security: "安全" };
      const highRiskPoints = testPoints.filter((point) => point.risk_level === "high").length;

      return (
        <>
          <DotField />
          <div className="app-shell mimo-shell">
            <header className="desktop-topbar">
              <div className="traffic" aria-hidden="true"><span></span><span></span><span></span></div>
              <div className="top-chip">
                <span className="tiny-avatar">AT</span>
                <strong>AI Test Agent</strong>
                <em>本地项目执行</em>
              </div>
              <div className="model-stack">
                <span className="top-chip">v0.1 Pro</span>
                <span className="top-chip">测试开发</span>
                <span className="top-chip">快速</span>
              </div>
              <div className="clock">{clockText}</div>
              <nav className="desktop-nav">
                <a href="/docs">接口文档</a>
                <a href="https://github.com/Whw12138/ai-test-agent" target="_blank" rel="noreferrer">GitHub</a>
              </nav>
            </header>

            <section className="desktop-frame">
              <aside className="side-dock">
                <div className="dock-search"><span>ai-test-agent</span><span>搜索</span></div>
                <div className="dock-title">能力中心 <span>主区操作</span></div>
                <div className="ability-tabs">
                  <button className="active" onClick={loadMarkdown}>编程</button>
                  <button onClick={loadOpenApi}>联调</button>
                  <button>多模态</button>
                  <button>语音</button>
                </div>
                <div className="side-card">
                  <IslandIcon type="api" label="接口能力" />
                  <div><strong>AI Test Agent</strong><span>接口测试用例生成与自动执行</span></div>
                </div>
                <div className="side-card muted">
                  <IslandIcon type="ci" label="工程展示" />
                  <div><strong>工程展示</strong><span>pytest、报告、GitHub Actions</span></div>
                </div>
                <div className="dock-title">成果与状态</div>
                <div className="side-card">
                  <IslandIcon type="asset" label="测试资产" />
                  <div><strong>测试资产</strong><span>{execution ? execution.total : cases.length} 项用例、Bug 摘要、脑图和报告</span></div>
                </div>
                <div className="side-card muted">
                  <IslandIcon type="context" label="上下文" />
                  <div><strong>上下文</strong><span>{endpoints.length} 个接口契约与需求文档</span></div>
                </div>
                <div className="side-card muted">
                  <IslandIcon type="task" label="任务状态" />
                  <div><strong>任务</strong><span>{statusLabels[status] || status}，运行状态看板</span></div>
                </div>
              </aside>

              <main className="workbench">
                <div className="work-heading">
                  <IslandIcon type="agent" label="AI 测试工作流" large />
                  <div>
                    <p>AI 测试工作流</p>
                    <h1>编程</h1>
                    <small>把需求交给工作台，自动完成接口解析、用例设计、代码生成、测试执行和报告归档。</small>
                  </div>
                  <button className="mini-action" onClick={clearAll}>返回空白任务</button>
                </div>

                <div className="flow-strip">
                  <span className="active">当前：编程</span>
                  <span>填入参数</span>
                  <span>保存成果</span>
                </div>

                <div className="mimo-tabs">
                  <button className={`mimo-tab ${inputFormat === "text" ? "active" : ""}`} onClick={loadMarkdown}>编程</button>
                  <button className={`mimo-tab ${inputFormat === "openapi" ? "active" : ""}`} onClick={loadOpenApi}>联调</button>
                  <button className="mimo-tab" onClick={loadOpenApi}>契约</button>
                  <button className="mimo-tab" onClick={clearAll}>清空</button>
                </div>

                <div className="task-grid">
                  <button className="task-card primary-task" onClick={runAgent} disabled={running || text.trim().length === 0}>
                    <strong>{running ? "运行中..." : "运行 Agent"}</strong>
                    <span>从需求到报告，一次跑完整闭环。</span>
                  </button>
                  <button className="task-card" onClick={loadOpenApi}>
                    <strong>读取接口契约</strong>
                    <span>载入 OpenAPI 示例，检查解析和用例生成。</span>
                  </button>
                  <button className="task-card" onClick={loadMarkdown}>
                    <strong>整理需求</strong>
                    <span>切回 Markdown 示例，适合面试演示。</span>
                  </button>
                  <button className="task-card" onClick={clearAll}>
                    <strong>重置工作台</strong>
                    <span>清空输入和运行结果，重新开始。</span>
                  </button>
                </div>

                <section className="draft-card">
                  <div className="draft-head">
                    <div><strong>任务草稿</strong><span> 在当前项目里实现这个测试任务</span></div>
                    <button className="primary-button" onClick={runAgent} disabled={running || text.trim().length === 0}>
                      {running ? "运行中..." : "生成报告"}
                    </button>
                  </div>
                  <div className="draft-body">
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
                      <span className={`status-pill ${statusClass}`}>{statusLabels[status] || status}</span>
                    </div>
                  </div>
                </section>

                <section className="console-card">
                  <div className="console-head">
                    <div><strong>测试管理台</strong><span> {summary}</span></div>
                    <div className="console-toolbar">
                      {suiteUrl && <a className="artifact-link" href={suiteUrl} download>下载 suite.json</a>}
                      {reportUrl && <a className="artifact-link primary" href={reportPreview} target="_blank" rel="noreferrer">打开 HTML 报告</a>}
                    </div>
                  </div>
                  <div className="console-body">
                    <div className="metric-grid">
                      <Metric label="接口" value={endpoints.length} />
                      <Metric label="测试点" value={testPoints.length} />
                      <Metric label="用例" value={cases.length} />
                      <Metric label="Bug/风险" value={bugSummaries.length} />
                      <Metric label="通过率" value={passRate} />
                    </div>

                    <div className="platform-tabs">
                      <button className={`platform-tab ${activeResultTab === "points" ? "active" : ""}`} onClick={() => setActiveResultTab("points")}>AI 测试点 {testPoints.length}</button>
                      <button className={`platform-tab ${activeResultTab === "cases" ? "active" : ""}`} onClick={() => setActiveResultTab("cases")}>测试用例 {cases.length}</button>
                      <button className={`platform-tab ${activeResultTab === "contracts" ? "active" : ""}`} onClick={() => setActiveResultTab("contracts")}>接口契约 {endpoints.length}</button>
                      <button className={`platform-tab ${activeResultTab === "bugs" ? "active" : ""}`} onClick={() => setActiveResultTab("bugs")}>Bug 摘要 {bugSummaries.length}</button>
                      <button className={`platform-tab ${activeResultTab === "mindmap" ? "active" : ""}`} onClick={() => setActiveResultTab("mindmap")}>测试脑图 {mindmapUrl ? 1 : 0}</button>
                      <button className={`platform-tab ${activeResultTab === "execution" ? "active" : ""}`} onClick={() => setActiveResultTab("execution")}>执行记录 {execution ? 1 : 0}</button>
                      <button className={`platform-tab ${activeResultTab === "report" ? "active" : ""}`} onClick={() => setActiveResultTab("report")}>测试报告 {reportUrl ? 1 : 0}</button>
                    </div>

                    {activeResultTab === "points" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>AI 测试点脑图</h3>
                            <p>从需求文档提取功能、边界和异常关注点，按风险等级整理。</p>
                          </div>
                        </div>
                        {testPoints.length === 0 ? (
                          <div className="empty">运行 Agent 后，这里会生成可解释的测试点树。</div>
                        ) : (
                          <div className="test-point-list">
                            {testPoints.map((point, index) => (
                              <div className="test-point" key={point.id}>
                                <span className="point-index">{index + 1}</span>
                                <div>
                                  <strong>{point.feature}</strong>
                                  <p>{point.description}</p>
                                </div>
                                <span className={`risk-badge ${point.risk_level}`}>{riskLabels[point.risk_level] || point.risk_level}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {activeResultTab === "cases" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>结构化测试用例</h3>
                            <p>覆盖正向、异常和边界场景，可继续生成 pytest 自动化脚本。</p>
                          </div>
                          {testFileUrl && <a className="artifact-link" href={testFileUrl} download>下载 pytest</a>}
                        </div>
                        {cases.length === 0 ? (
                          <div className="empty">运行 Agent 后，这里会展示生成的结构化用例。</div>
                        ) : (
                          <div className="table-wrap">
                            <table>
                              <thead><tr><th>ID</th><th>类别</th><th>优先级</th><th>请求</th><th>预期状态</th></tr></thead>
                              <tbody>
                                {cases.map((item) => (
                                  <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td>{categoryLabels[item.category] || item.category}</td>
                                    <td>{item.priority}</td>
                                    <td>{item.method} {item.path}</td>
                                    <td>{item.expected_status}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}
                      </div>
                    )}

                    {activeResultTab === "contracts" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>接口契约</h3>
                            <p>展示 Agent 从 Markdown 或 OpenAPI 中解析出的接口定义。</p>
                          </div>
                        </div>
                        {endpoints.length === 0 ? (
                          <div className="empty">运行 Agent 后，这里会展示解析出的 API 契约。</div>
                        ) : (
                          <div className="table-wrap">
                          <table>
                            <thead><tr><th>方法</th><th>路径</th><th>名称</th><th>成功状态码</th><th>必填字段</th></tr></thead>
                            <tbody>
                              {endpoints.map((item, index) => (
                                <tr key={`${item.method}-${item.path}-${index}`}>
                                  <td><span className={`method ${item.method.toLowerCase()}`}>{item.method}</span></td>
                                  <td>{item.path}</td>
                                  <td>{item.name}</td>
                                  <td>{item.success_status}</td>
                                  <td>{item.required_fields?.join(", ") || "-"}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                          </div>
                        )}
                      </div>
                    )}

                    {activeResultTab === "bugs" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>疑似 Bug 与风险摘要</h3>
                            <p>执行失败会生成疑似 Bug；全部通过时保留高风险测试关注项，方便复盘和面试展示。</p>
                          </div>
                          <div className="console-toolbar">
                            {bugSummaryUrl && <a className="artifact-link" href={bugSummaryUrl} download>下载 Bug JSON</a>}
                            {xmindUrl && <a className="artifact-link primary" href={xmindUrl} download>下载 XMind</a>}
                          </div>
                        </div>
                        {bugSummaries.length === 0 ? (
                          <div className="empty">运行 Agent 后，这里会生成疑似 Bug 或风险关注列表。</div>
                        ) : (
                          <div className="bug-summary-list">
                            {bugSummaries.map((item) => (
                              <div className={`bug-summary-card ${item.severity}`} key={item.id}>
                                <div className="bug-summary-head">
                                  <strong>{item.id} · {item.title}</strong>
                                  <span className={`bug-severity ${item.severity}`}>{riskLabels[item.severity] || item.severity}</span>
                                </div>
                                <p>{item.actual_result}</p>
                                <p>{item.recommendation}</p>
                                <div className="bug-meta">
                                  <span>状态：{item.status}</span>
                                  <span>来源：{item.source}</span>
                                  <span>关联：{item.related_case || "-"}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {activeResultTab === "mindmap" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>测试脑图导出</h3>
                            <p>把接口契约、测试点、用例、疑似 Bug 和报告状态组织成可下载脑图。</p>
                          </div>
                          <div className="console-toolbar">
                            {mindmapUrl && <a className="artifact-link" href={mindmapUrl} download>下载脑图 MD</a>}
                            {xmindUrl && <a className="artifact-link primary" href={xmindUrl} download>下载 XMind</a>}
                          </div>
                        </div>
                        {!result ? (
                          <div className="empty">运行 Agent 后，这里会展示测试资产脑图。</div>
                        ) : (
                          <div className="mindmap-preview">
                            <div className="mindmap-tree">
                              <div className="mindmap-root">{projectName || "演示 API"} 测试脑图</div>
                              <div className="mindmap-branches">
                                <div className="mindmap-branch">
                                  <strong>接口契约</strong>
                                  <ul>{endpoints.slice(0, 6).map((item, index) => <li key={`${item.path}-${index}`}>{item.method} {item.path}</li>)}</ul>
                                </div>
                                <div className="mindmap-branch">
                                  <strong>测试点</strong>
                                  <ul>{testPoints.slice(0, 6).map((item) => <li key={item.id}>{item.feature} · {riskLabels[item.risk_level] || item.risk_level}</li>)}</ul>
                                </div>
                                <div className="mindmap-branch">
                                  <strong>测试用例</strong>
                                  <ul>{cases.slice(0, 6).map((item) => <li key={item.id}>{item.id} · {categoryLabels[item.category] || item.category}</li>)}</ul>
                                </div>
                                <div className="mindmap-branch">
                                  <strong>Bug 与风险</strong>
                                  <ul>{bugSummaries.slice(0, 6).map((item) => <li key={item.id}>{item.id} · {item.title}</li>)}</ul>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {activeResultTab === "execution" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>执行记录与 AI 风险洞察</h3>
                            <p>根据 pytest 的真实结果整理失败摘要，方便继续定位问题。</p>
                          </div>
                          {junitUrl && <a className="artifact-link" href={junitUrl} download>下载 JUnit XML</a>}
                        </div>
                        {!execution ? (
                          <div className="empty">开启“执行生成的 pytest”后运行 Agent，这里会显示执行日志。</div>
                        ) : (
                          <>
                            <div className={`insight-box ${execution.success ? "pass" : ""}`}>
                              <h3>{execution.success ? "本次执行未发现失败" : `发现 ${failures.length} 个疑似缺陷`}</h3>
                              <p>{execution.success ? `共执行 ${execution.total} 条用例，全部通过。可以继续补充边界需求或导出报告。` : "优先检查失败用例的请求参数、预期状态码和接口实现，再根据日志复现。"}</p>
                            </div>
                            {failures.length > 0 && (
                              <div className="failure-list">
                                {failures.map((failure, index) => (
                                  <div className="failure-item" key={`${failure.name}-${index}`}>
                                    <strong>{failure.name}</strong>
                                    <p>{failure.message}</p>
                                  </div>
                                ))}
                              </div>
                            )}
                            <div className="record-meta">
                              <span>通过 {execution.passed}</span>
                              <span>失败 {execution.failed}</span>
                              <span>错误 {execution.errors}</span>
                              <span>跳过 {execution.skipped}</span>
                              <span>耗时 {execution.duration_seconds.toFixed(2)}s</span>
                            </div>
                            <pre className="execution-log">{execution.stdout || execution.stderr || "无执行输出"}</pre>
                          </>
                        )}
                      </div>
                    )}

                    {activeResultTab === "report" && (
                      <div className="tab-pane">
                        <div className="pane-heading">
                          <div>
                            <h3>测试报告与归档</h3>
                            <p>预览 HTML 报告，也可以下载生成的测试资产用于提交或复盘。</p>
                          </div>
                        </div>
                        {reportUrl ? (
                          <>
                            <iframe src={reportPreview} title="生成的测试报告" />
                            <div className="artifact-grid">
                              <a className="artifact-link primary" href={reportUrl} download>下载 HTML 报告</a>
                              <a className="artifact-link" href={markdownReportUrl} download>下载 Markdown 报告</a>
                              <a className="artifact-link" href={suiteUrl} download>下载 suite.json</a>
                              <a className="artifact-link" href={testFileUrl} download>下载 pytest 脚本</a>
                              {bugSummaryUrl && <a className="artifact-link" href={bugSummaryUrl} download>下载 Bug 摘要</a>}
                              {mindmapUrl && <a className="artifact-link" href={mindmapUrl} download>下载脑图 MD</a>}
                              {xmindUrl && <a className="artifact-link primary" href={xmindUrl} download>下载 XMind</a>}
                            </div>
                          </>
                        ) : (
                          <div className="empty">运行完成后，这里会预览并归档生成的测试报告。</div>
                        )}
                      </div>
                    )}
                    {error && <p className="error">{error}</p>}
                  </div>
                </section>
              </main>

              <aside className="asset-dock">
                <div className="asset-tabs">
                  <span className="active">资产 {cases.length + bugSummaries.length}</span>
                  <span>上下文 {endpoints.length}</span>
                  <span>变更 0</span>
                  <span>任务 {status === "IDLE" ? 0 : 1}</span>
                </div>
                <div className="island-postcard" aria-hidden="true">
                  <div className="wood-sign">测试岛</div>
                  <div className="postcard-chip">AI QA 航线</div>
                </div>
                <div className="asset-card">
                  <h3>资产码头</h3>
                  <p>输出资产会在这里汇总：接口契约、测试用例、Bug 摘要、测试脑图和 HTML 报告。</p>
                </div>
                <div className="asset-metrics">
                  <div>{endpoints.length}<span>接口</span></div>
                  <div>{cases.length}<span>用例</span></div>
                  <div>{reportUrl ? 1 : 0}<span>报告</span></div>
                </div>
                <div className="asset-card feature">
                  <div>
                    <IslandIcon type="asset" label="资产" large />
                    <h3>{reportUrl ? "已有可用资产" : "还没有可用资产"}</h3>
                    <p>{reportUrl ? "报告已生成，可以打开查看或继续修改需求重新运行。" : "先生成测试报告，完成后会自动归档到这里。"}</p>
                    <div className="hero-actions">
                      <button className="mini-action active" onClick={runAgent} disabled={running || text.trim().length === 0}>生成资产</button>
                      <button className="mini-action" onClick={loadOpenApi}>分析契约</button>
                    </div>
                  </div>
                </div>
                <div className="asset-card">
                  <h3>能力状态</h3>
                  <p>入口 {inputFormat === "openapi" ? "OpenAPI" : "Markdown"}，授权可执行，结果回到当前工作台。</p>
                </div>
                <div className={`insight-box ${execution?.success ? "pass" : ""}`}>
                  <h3>AI 风险雷达</h3>
                  <p>{result ? `识别 ${testPoints.length} 个测试点，其中 ${highRiskPoints} 个高风险关注点；生成 ${bugSummaries.length} 条 Bug/风险摘要。` : "运行 Agent 后，这里会汇总需求风险和执行失败。"}</p>
                </div>
                {result && (
                  <div className="asset-card">
                    <h3>下载测试资产</h3>
                    <div className="artifact-grid">
                      <a className="artifact-link" href={suiteUrl} download>suite.json</a>
                      <a className="artifact-link" href={testFileUrl} download>pytest 脚本</a>
                      <a className="artifact-link" href={markdownReportUrl} download>Markdown</a>
                      <a className="artifact-link primary" href={reportUrl} download>HTML 报告</a>
                      {bugSummaryUrl && <a className="artifact-link" href={bugSummaryUrl} download>Bug 摘要</a>}
                      {mindmapUrl && <a className="artifact-link" href={mindmapUrl} download>脑图 MD</a>}
                      {xmindUrl && <a className="artifact-link primary" href={xmindUrl} download>XMind</a>}
                    </div>
                  </div>
                )}
              </aside>
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
