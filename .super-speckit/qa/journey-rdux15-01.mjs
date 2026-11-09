// RDUX15-01 journey v2: real-app CDP assertions. View/cancel only.
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
  if (r.result?.exceptionDetails) return { error: (r.result.exceptionDetails.exception?.description ?? "exception").slice(0, 120) };
  return r.result?.result?.value;
};
const shot = async (name) => { const r = await send("Page.captureScreenshot", { format: "png" }); await mkdir(OUT, { recursive: true }); await writeFile(`${OUT}/${name}.png`, Buffer.from(r.result.data, "base64")); return `${OUT}/${name}.png`; };
const esc = `(() => {
  const el = document.activeElement ?? document.body;
  for (const t of [document, el]) {
    t.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", keyCode: 27, which: 27, bubbles: true, cancelable: true }));
  }
  return true;
})()`;

const results = {};
await send("Page.enable");

// clean slate: dismiss anything left from v1
await evalJs(esc); await sleep(500); await evalJs(esc); await sleep(500);
results.clean = await evalJs(`({ gone: !document.querySelector('[role="dialog"] [data-testid="virtual-project-name"]') })`);

// 1. open create form
results.addClicked = await evalJs(`(() => { const b = document.querySelector('[data-testid="virtual-project-add"]'); if (!b) return "missing:add"; b.click(); return true; })()`);
await sleep(1200);

// 2. combined form assertions (REQ-01/02: name+device+folders one surface)
results.form = await evalJs(`(() => {
  const dlg = document.querySelector('[role="dialog"]');
  if (!dlg) return { error: "no dialog" };
  const q = (s) => Boolean(dlg.querySelector(s));
  return {
    name: q('[data-testid="virtual-project-name"]'),
    device: q('[data-testid="virtual-project-device"]'),
    browse: q('[data-testid="virtual-project-browse"]'),
    existing: q('[data-testid="virtual-project-existing"]'),
    title: (dlg.querySelector("h2, h1, [data-slot=\\"dialog-title\\"]")?.textContent ?? "").trim().slice(0, 40),
  };
})()`);
results.proofForm = await shot("03-form-v2");

// 3. dropdown contents
await evalJs(`(() => { const t = document.querySelector('[role="dialog"] [data-testid="virtual-project-device"]'); if (!t) return "missing"; t.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true })); t.dispatchEvent(new PointerEvent("pointerup", { bubbles: true })); return true; })()`);
await sleep(900);
results.dropdown = await evalJs(`(() => {
  const items = Array.from(document.querySelectorAll('[role="listbox"] [role="option"]'));
  return {
    count: items.length,
    texts: items.map((i) => i.textContent.trim().replace(/\s+/g, " ").slice(0, 45)),
    localAttrOnOption: items.some((i) => i.getAttribute("data-device-id") === "local" || i.querySelector('[data-device-id="local"]') !== null),
    localByText: items.some((i) => /This computer|此电脑/.test(i.textContent)),
    addRemoteByText: items.some((i) => /Add remote device|添加远程设备/.test(i.textContent)),
  };
})()`);
results.proofDropdown = await shot("04-dropdown-v2");

// 4. cancel without saving: Esc closes dropdown, Esc closes dialog
await evalJs(esc); await sleep(400); await evalJs(esc); await sleep(700);
results.cancel = await evalJs(`({ dialogGone: !document.querySelector('[role="dialog"] [data-testid="virtual-project-name"]') })`);
results.proofAfter = await shot("05-after-cancel");

console.log(JSON.stringify(results, null, 1));
ws.close();
