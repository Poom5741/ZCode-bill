// RDUX15-04/05 journey: settings → 远程设备 → add window SSH/WSL/Docker
// categorization (default SSH) + WSL section on Windows. View/cancel only.
import WebSocket from "ws";
import { mkdir, writeFile } from "node:fs/promises";

const CDP = "http://127.0.0.1:9229";
const OUT = ".super-speckit/qa/rdux15-journey";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const page = (await (await fetch(`${CDP}/json/list`)).json()).find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl, { maxPayload: 256 * 1024 * 1024 });
await new Promise((r) => ws.once("open", r));
let seq = 0; const pending = new Map();
ws.on("message", (raw) => { const m = JSON.parse(raw); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((res) => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const evalJs = async (expression) => {
  const r = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) return { error: (r.result.exceptionDetails.exception?.description ?? "exception").slice(0, 140) };
  return r.result?.result?.value;
};
const shot = async (name) => { const r = await send("Page.captureScreenshot", { format: "png" }); await mkdir(OUT, { recursive: true }); await writeFile(`${OUT}/${name}.png`, Buffer.from(r.result.data, "base64")); return `${OUT}/${name}.png`; };

const results = {};
await send("Page.enable");

// 0. dismiss leftovers
await evalJs(`document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", keyCode: 27, bubbles: true, cancelable: true })); true`);
await sleep(400);

// 1. open settings from the task bar button
results.settingsOpened = await evalJs(`(() => {
  const b = document.querySelector('[data-testid="task-settings-button"]');
  if (!b) return "missing:task-settings-button";
  b.click(); return true;
})()`);
await sleep(1500);
results.settingsVisible = await evalJs(`({ settings: Boolean(document.querySelector('[data-testid="settings-page"]')) })`);

// 2. navigate to 远程设备 section
results.navClicked = await evalJs(`(() => {
  const nav = document.querySelector('[data-settings-section-nav="remoteDevices"]');
  if (!nav) return "missing:nav-remoteDevices";
  nav.click(); return true;
})()`);
await sleep(1500);
results.proofDevices = await shot("06-remote-devices");

// 3. discover add controls in the panel
results.addCandidates = await evalJs(`(() => {
  const page = document.querySelector('[data-testid="settings-page"]');
  const root = page ?? document;
  return Array.from(root.querySelectorAll("button"))
    .filter((b) => /Add|添加|remote device|远程设备/i.test(b.textContent ?? "") && b.getClientRects().length)
    .slice(0, 6)
    .map((b) => ({ tid: b.dataset.testid ?? null, text: (b.textContent ?? "").trim().slice(0, 40) }));
})()`);

// 4. open the add window (first matching enabled button)
results.addOpened = await evalJs(`(() => {
  const page = document.querySelector('[data-testid="settings-page"]');
  const root = page ?? document;
  const b = Array.from(root.querySelectorAll("button")).find((x) =>
    /New connection|新建连接/i.test((x.getAttribute("aria-label") ?? "") + (x.textContent ?? "")) && !x.disabled && x.getClientRects().length);
  if (!b) return "no-add-button";
  b.click(); return true;
})()`);
await sleep(1500);

// 5. assert kind categorization + default SSH
results.kindTabs = await evalJs(`(() => {
  const kinds = Array.from(document.querySelectorAll('[data-testid^="remote-kind-"]'))
    .filter((el) => el.getClientRects().length)
    .map((el) => ({ tid: el.dataset.testid, active: el.getAttribute("aria-checked") ?? el.getAttribute("data-state") ?? el.getAttribute("aria-pressed") ?? "?" }));
  const sshDialog = Boolean(document.querySelector('[data-testid="ssh-dialog"]'));
  return { kinds, sshDialog };
})()`);
results.proofAddSsh = await shot("07-add-default-ssh");

// 6. switch to WSL section
results.wslClicked = await evalJs(`(() => {
  const wsl = document.querySelector('[data-testid="remote-kind-wsl"]');
  if (!wsl) return "missing:remote-kind-wsl";
  wsl.click(); return true;
})()`);
await sleep(1200);
results.wslSection = await evalJs(`(() => {
  const dlg = document.querySelector('[data-testid="ssh-dialog"]') ?? document.querySelector('[role="dialog"]');
  if (!dlg) return { error: "no add dialog" };
  const text = (dlg.textContent ?? "").replace(/\s+/g, " ");
  return {
    wslActive: (document.querySelector('[data-testid="remote-kind-wsl"]')?.getAttribute("aria-checked") ?? document.querySelector('[data-testid="remote-kind-wsl"]')?.getAttribute("data-state")) ?? "?",
    mentionsDistro: /distro|发行版/i.test(text),
    mentionsWsl: /WSL/i.test(text),
    snippet: text.slice(0, 160),
  };
})()`);
results.proofAddWsl = await shot("08-add-wsl");

// 7. cancel — Esc
await evalJs(`document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", keyCode: 27, bubbles: true, cancelable: true })); true`);
await sleep(600);
results.cancelled = await evalJs(`({ dialogGone: !document.querySelector('[data-testid="ssh-dialog"]') })`);
results.proofAfter = await shot("09-after-cancel");

console.log(JSON.stringify(results, null, 1));
ws.close();
