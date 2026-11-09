# Spec — zbill-product-pivot

ZBill: transform the ZCode fork into a Windows-first desktop app for creating bill reports.
The agent-chat core stays as the interaction model (3-panel shell: file tree / AI chat /
document panel). Non-billing ZCode features are hard-deleted from the product and codebase;
bill capability expands beyond today's EV-charging pipeline. Authority: purpose map
(.super-speckit/purpose/zbill-product-pivot/purpose-map.md, confirmed 2026-11-09) and the
owner's four scope answers recorded in decision trail DT-ZPIVOT-01.

## User stories

1. As a finance-staff user, I want the app to open as ZBill with chat as the core surface, so that I can drive report creation conversationally without agent-development clutter.
2. As a finance-staff user, I want receipts of any bill type (EV, utility, phone, internet, general expense) to flow into a monthly report, so that one app covers all reimbursements.
3. As a finance-staff user, I want to review and edit extracted items (amounts, dates, business purpose) before generating, so that the submitted report is correct without hand-editing files.
4. As a finance-staff user, I want past reports stored and browsable in-app, so that I can re-open or re-export any previous month.
5. As a finance-staff user, I want outputs beyond xlsx+PDF (per-person sheets, CSV), so that the report fits each submission channel.
6. As the app owner, I want purchase/marketplace/automations and remote-connection surfaces gone from code, so that the product is honest, smaller, and maintainable.

## Requirements

- REQ-101 ZBill product mode builds and launches on Windows presenting as ZBill; Automations and Plugin Marketplace entries absent (real-app journey evidence).
- REQ-102 A new chat task round-trips with the local agent in ZBill mode (real-app journey with transcript evidence).
- REQ-103 The zbill-billing pipeline produces xlsx+PDF from the proven EV fixtures on this Windows host (regression guard; CLI evidence).
- REQ-104 At least one non-EV bill class ingests end-to-end (parse → items → report) without fabricating amounts; unknown formats stay flagged, never guessed.
- REQ-105 Extracted items are reviewable and editable before generation; edits are reflected in the generated report.
- REQ-106 Generated reports are archived and browsable in-app (document panel) and re-exportable.
- REQ-107 Wave 1: coding-plan purchase panels, plugin marketplace, and automations surfaces are removed from product code and routes; no dead exports remain; typecheck/lint/architecture checks exit 0.
- REQ-108 Wave 2: remote-connection device management (SSH/WSL/Docker), web/mobile remote-control surfaces, and unused provider/store modules are deleted per the investigation keep-list; local Windows workspace + chat flow unaffected.
- REQ-109 Docs (AGENTS.md/DESIGN.md/CONTEXT.md, issue docs) match the surviving product; superseded plans recorded.

## Acceptance criteria and verification

Each REQ row binds to the matrix (.super-speckit/features/zbill-product-pivot/matrix.md):
CLI/repo-check evidence for REQ-103/104/107/108/109; real-running-app journey evidence
(ADE computer-use executor) for REQ-101/102/105/106/108. No row becomes verified from code
inspection alone.

## Non-goals

Google OAuth plugins (gmail/gdrive/gcalendar/gsheets — later milestone, auth decision
recorded in zbill-billing/GOOGLE-PLUGINS-M2.md); macOS/Linux packaging; multi-tenant
billing; new auth/payment systems; mobile/web remote control (deleted, not rebuilt);
RDUX15 connection UX (superseded).
