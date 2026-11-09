# Requirements-to-verification matrix — zbill-product-pivot

Overgoal (confirmed by repo owner, ADE chat 2026-11-09): transform ZCode into ZBill — a
Windows-first desktop app for creating bill reports. Keep the agent-chat core (3-panel shell:
file tree / AI chat / document panel), expand bill features beyond the current EV-charging
pipeline, and hard-delete most non-billing ZCode design and features from the code.
Supersedes rdux15-project-device-separation (its domain is being cut, not polished) and
absorbs ZBILL-M1 (macOS-first build-proof; Windows-first replaces it; see decision trail).

| Requirement ID | Acceptance criterion | Verification method | Automated asset | Runtime/API/DB assertion | Owner | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-101 | Ported ZBill product mode builds and launches on Windows: app presents as ZBill, Automations + Plugin Marketplace entries hidden | Real-app journey (ADE computer-use) with screenshot | `ZBILL_PRODUCT=1` dev task in mise.toml | Running app window title/menu "ZBill"; sidebar entries absent | maker | planned | — |
| REQ-102 | Agent chat core works in ZBill mode: a new chat task round-trips with the local agent (prompt in, response + tool activity out) | Real-app journey with transcript evidence | existing session runtime | agent response observed in running app | maker | planned | — |
| REQ-103 | `zbill-billing` pipeline still produces xlsx+PDF from the proven EV fixtures on this Windows host (regression guard) | CLI run of the documented venv pipeline | `zbill-billing/scripts/build_report.py` + `fixtures/inbox` | output files exist with parsed totals matching items.json | maker | planned | — |
| REQ-104 | At least one non-EV bill class ingests end-to-end (parse → items → report) without fabricating amounts; unknown formats stay flagged | CLI run with a new fixture + items.json overrides | `zbill-billing/scripts/*` | report contains only user-confirmed amounts; unknown-format warning recorded | maker | planned | — |
| REQ-105 | Extracted items are reviewable and editable before generation; edits are reflected in the generated report | In-app journey (edit item → regenerate) + file diff evidence | items.json override path | report amounts equal edited values, not raw extraction | maker | planned | — |
| REQ-106 | Generated reports are archived and browsable in-app (document panel) and re-exportable | Real-app journey | output dir under workspace | past report opens in document panel; re-export produces files | maker | planned | — |
| REQ-107 | Cut wave 1: coding-plan purchase/billing panels, plugin marketplace, and automations surfaces are removed from product code and routes; no dead imports remain | grep/dep evidence + `pnpm typecheck`/`pnpm lint`/`pnpm architecture:check --changed` | repo checks | removed route ids absent from bundle; checks exit 0 | maker | planned | — |
| REQ-108 | Cut wave 2: remote-connection device management (SSH/WSL/Docker), web/mobile remote-control surfaces, and unused provider/store modules are deleted per the investigation's keep-list; local Windows workspace + chat flow unaffected | Real-app journey + repo checks | repo checks | app opens local workspace, chat works, removed surfaces absent from UI and code | maker | planned | — |
| REQ-109 | Docs match the product: AGENTS.md/DESIGN.md/CONTEXT.md and issue docs updated for deleted modules; superseded plans recorded | doc review + git evidence | — | docs reference only surviving commands/modules | maker | planned | — |

## Explicit exclusions

| Requirement ID | Status | Reason | Approval |
| --- | --- | --- | --- |
| REQ-910 | Google OAuth plugins (gmail/gdrive/gcalendar/gsheets) | Later milestone per zbill-billing/GOOGLE-PLUGINS-M2.md (auth decision recorded 2026-11-07) | Poom 2026-11-09 |
| REQ-911 | macOS/Linux packaging | Windows-first per owner 2026-11-09; original macOS M1 scope absorbed | Poom 2026-11-09 |
| REQ-912 | Multi-tenant billing, new auth/payment systems | Non-goal of the pivot | Poom 2026-11-09 |
| REQ-913 | RDUX15 project/device-selection connection UX | Superseded: its domain (remote connections) is being cut, not polished | Poom 2026-11-09 |

No row becomes `verified` from code inspection alone; REQ-101/102/105/106/108 require
real-running-app journey evidence (ADE computer-use executor per DT-RDUX15-01).
