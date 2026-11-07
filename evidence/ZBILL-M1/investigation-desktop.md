# Investigation — desktop app structure (2026-11-07)

- packages/desktop: src/, native/, build/, scripts/, electron-builder.config.js — Electron main + renderer app
- The shipped ZCode Desktop app (this session's host) already renders: left file tree, center agent chat, right document panels (PDF/Spreadsheets/Presentations via MCP viewer plugins) — confirms 3-panel shell exists upstream; M1 does not need to build panels from scratch
- Coding-specific surfaces to hide later (M3): terminal, git panel, plugin marketplace
- architecture-policy.yaml defines module boundaries (rpc, shared, provider, services, session...) — ZBill additions must stay locally contained (billing skill + MCP server), no edits across legacy modules in M1
