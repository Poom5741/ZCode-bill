import WebSocket from "ws";
const page = (await (await fetch("http://127.0.0.1:9229/json/list")).json()).find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl, { maxPayload: 64 * 1024 * 1024 });
await new Promise((r) => ws.once("open", r));
let seq = 0; const pending = new Map();
ws.on("message", (raw) => { const m = JSON.parse(raw); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((res) => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const r = await new Promise((res) => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method: "Runtime.evaluate", params: { returnByValue: true, expression: `(() => {
  const page = document.querySelector('[data-testid="settings-page"]');
  const root = page ?? document;
  return Array.from(root.querySelectorAll("button")).filter((b) => b.getClientRects().length).slice(0, 40)
    .map((b) => ({ tid: b.dataset.testid ?? null, label: (b.getAttribute("aria-label") ?? b.textContent ?? "").trim().replace(/\s+/g," ").slice(0, 36) }));
})()` } })); });
console.log(JSON.stringify(r.result?.result?.value ?? r, null, 1));
ws.close();
