# Tasks — zbill-product-pivot

Ordered by wave; each task names its REQ binding. [x] = done with evidence linked in the
matrix; every REQ row needs its verification before the slice closes.

## W1 cut (REQ-101, REQ-103, REQ-107)

- [x] T1 Trace host-side handlers for addPluginMarketplace/updatePluginMarketplace and
      purchase-token RPCs; list every caller (App.tsx, host, shared protocol).
      Finding 2026-11-10: marketplace management is a services-layer chain, no desktop-main
      handlers — zcodeAgentService.ts:5496/5524 → zcodeAgent.ts:815/821 →
      pluginManagementService.ts:23/25/:181/:187 → pluginManagement.ts:64/:70/:101/:103
      (operation allowlist). Purchase e2e helpers confirmed under
      packages/desktop/test/e2e/helpers/coding-plan-upgrade-*.ts (+ codingPlanUpgradeMockServer.test.ts).
- [ ] T2 Delete automations surface: workspaceMainView "automations" route branches,
      AutomationsPage component graph, run-history navigation (WorkspaceShellLayout
      :1527-1536), onOpenAutomations wiring end to end.
- [ ] T3 Delete plugin-store surface: PluginStorePage, pluginStoreNavigation lib,
      plugin-store route branches, marketplace management RPCs (T1 list).
- [ ] T4 Delete coding-plan purchase surface: CodingPlanUpgradeDialog,
      CodingPlanEmbeddedWebviewDialog, CodingPlanPurchaseChoiceBanners,
      codingPlanPurchaseAuth.js, purchase-token refresh state; keep provider base CRUD.
- [ ] T5 Audit packages/services/src/coding-plan-subscription/* and usage-stats purchase
      providers: delete members with no remaining callers (knip-verified).
- [ ] T6 Delete/rewrite e2e specs covering deleted surfaces (marketing-touch-*,
      coding-plan entitlement); record coverage change in matrix evidence.
- [ ] T7 Remove dead i18n keys (plugin-store.*, automations.*, purchase strings) after
      last reference dies.
- [ ] T8 Checks: typecheck, lint, architecture:check --changed, knip; fix fallout.
- [ ] T9 Regression: zbill-billing EV fixtures still produce xlsx+PDF (REQ-103).
- [ ] T10 Journey: ZBILL_PRODUCT=1 launch — app is ZBill, deleted entries absent,
      chat round trip works (REQ-101; chat evidence also seeds REQ-102).

## W2 cut (REQ-102, REQ-108, REQ-109)

- [ ] T11 Investigate remote-control keep-list: import graph of remote-connection-flow,
      data-sync device management, web/server relay, mobile attachment.
- [ ] T12 Delete remote-connection-flow + data-sync device management per keep-list.
- [ ] T13 Delete web/mobile remote-control surfaces (packages/web, packages/server,
      relay attachment paths) unless blocked by a shared runtime dependency.
- [ ] T14 Delete unused provider/store modules found in T11; retire ZBILL_PRODUCT flag.
- [ ] T15 Update AGENTS.md/DESIGN.md/CONTEXT.md + issue docs (REQ-109).
- [ ] T16 Checks + journey: local workspace open, chat round trip (REQ-102), deleted
      surfaces absent (REQ-108).

## W3 bill features (REQ-104, REQ-105, REQ-106)

- [ ] T17 Add second bill-class parser + fixture + items.json (REQ-104); flag-and-ask
      behavior for unknown formats preserved.
- [ ] T18 Item review/edit flow: purpose-built review surface (or items.json editor)
      wired through hooks; edits flow into build_report.py (REQ-105).
- [ ] T19 Report archive: workspace-local reports dir, document-panel browsing,
      re-export action (REQ-106); archive index single-owner store.
- [ ] T20 Checks + journey: edit item → regenerate → open archived report.
