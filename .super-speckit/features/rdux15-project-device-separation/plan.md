# Plan — RDUX15 项目创建与远程连接管理分离

Technical approach per ticket 模块与接线 1–6, 数据与状态归属 7–13, 异步/取消/目录边界 14–21,
investigation findings in ./investigation-notes.md (HEAD 776437ca mapping).

## Reused seams (verified in code)
- Completion intent: `packages/ui/src/remote-connection-flow/contract.ts` — `onDeviceConnected`
  (device-management completion, no project creation), `onConnectionReady` (project wizard takes
  over directory selection), `completion` + `directToDirectory`, `requestRemoteProjectConnection`.
- Root-injected global wizard + `returnTarget` precedent: `data-sync/ui/DataSyncSection.tsx:125-143`.
- Sidebar default-device rule precedent: `project-sidebar/index.tsx:98`.
- Existing directory browser + remote existing-project picker: reuse as-is (wiring item 1).

## Architecture contract (docs-only extension of delivery rules; product code follows repo AGENTS.md)
- Draft ownership: project name/device/folders held by ONE owner (store via hooks, no per-entry
  copies; decision 9). Return-intent is renderer-memory only (app-shell types.ts draft handoff),
  never a task-protocol owner (decision 13).
- Device identity: Source/Profile model untouched; dropdown reads existing device-management facts
  (decision 7-8); no new management API (wiring item 5).
- Late-result inertia: existing request-identity/invalidation mechanisms reused; no timers/polling
  compensation (decision 19). Esc layering follows shared component top-layer rules (decision 21).
- Forbidden: new auth/install/connect chains, second wizard instance, per-path device dedup,
  password in return intent (reject-if-touched; validated in review).

## Testing approach
E2E-first per ticket Testing Decisions: map RDUX15 scenarios into existing case catalog + coverage
matrix, add red interaction tests at real entries before code (feedback loop), update helpers that
assume the old three-screen navigation. UI-integration tests only for unstable timing (late results,
cancel, draft restore). Real SSH/WSL/Docker chains per harness capabilities (WSL2/Docker local OK;
SSH host pending → honest not-verified).

## Milestone slices (ordered)
M1 project direct-create form + device dropdown (REQ-01..03, 06, 07)
M2 settings add window consolidation + three entries (REQ-04, 05, 08)
M3 completion-intent dispatch + draft round trips (REQ-09, 10, 14)
M4 existing-project entry + local capability guards (REQ-11, 12)
M5 credential/install/cancel/late-result hardening (REQ-13, 15, 16)
M6 a11y/visual/web-mobile regression pass (REQ-17..19)
