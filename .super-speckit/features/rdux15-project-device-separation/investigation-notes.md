# Investigation notes — rdux15-project-device-separation (2026-11-07)

`throughput checkpoint: n/a, read-only investigation`

## Verified seams (first mapping pass, HEAD 776437ca)

- **Completion-intent contract exists** — `packages/ui/src/remote-connection-flow/contract.ts`:
  `onDeviceConnected` (line 12-16, "设备管理连接成功；导航由发起入口负责，不创建项目"),
  `onConnectionReady` (line 26-27, "项目向导在连接完成后接管目录选择"),
  `completion` option (line 11), `RemoteConnectionCompletionIntent.directToDirectory` (line 53-60),
  `requestRemoteProjectConnection` re-export (line 5), `RemoteConnectionProgress` projection
  (line 117-135, wizard chrome + background-safe fields). This is the seam ticket 15 wiring item 4-5
  says to reuse: "现有流程已支持连接成功后由调用方接管。优先复用该接缝".
- **Chat composer project menu** — `packages/ui/src/project-sidebar/ProjectComposerMenu.tsx`
  (onCreateTask implementations at lines 111/435/571-580).
- **Sidebar remote default-device rule** — `packages/ui/src/project-sidebar/index.tsx:98`
  ("当前任务只影响远端'创建项目'的默认设备；分组继承在点击时读") — matches Q3's intended default rule.
- **Settings device management + wizard** — `packages/ui/src/data-sync/ui/DataSyncSection.tsx`
  (Root-injected global wizard: line 34 "打开已有的全局连接向导（Root 注入）", line 125 returnTarget
  "完成后 Root 回到发起时的设置 tab", busy-rejection at 143, reconnect at 365).
- **Entry provenance note** — `packages/ui/src/data-sync/ui/DataSyncEntry.tsx:29`
  ("只有带项目上下文的入口传入（连接向导、Header、侧栏项目菜单）").

## Open component questions (to resolve during spec/plan authoring)

1. Component hosting the local/remote pre-screen + host list inside project creation (the screen
   ticket 15 removes).
2. Current categorized SSH/WSL/Docker add-window shape after the 10-14 batch.
3. Chat menu remote-entry i18n key ("新建远程连接…" wording per ticket).
4. `packages/ui/src/app-shell/types.ts:82` draft handoff type (创建项目后的当前草稿交接) — read fully
   when designing draft ownership (ticket decision 9: single draft owner).
