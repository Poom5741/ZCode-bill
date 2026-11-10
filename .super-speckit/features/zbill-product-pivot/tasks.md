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
- [x] T2 (shell layer, 2026-11-10) automations surface removed: WorkspaceMainView narrowed to
      "chat" (types.ts), App.tsx states/handlers/props for automations+plugin-store deleted,
      WorkspaceShellLayout automations/plugin-store main-view branches (mobile + desktop) cut,
      useWorkspaceTaskNavigation producers removed (stale nav entries skip-and-continue),
      useWorkspaceMainViewSettingsExit.ts deleted (plugin-store-era exit compensation),
      saved-workflow hub openWorkflow removed (chip degrades to static saved marker;
      navigateToRun kept), composer palette plugin preview passes no-op.
      Remaining for T2: v4 onOpenAutomationsMain plumbing (SessionPane/V4ChatPane/
      V4WorkspaceChatArea/WorkbenchPane — inert, button hidden) + AutomationsSection.tsx +
      AutomationsMainBreadcrumbFrame.tsx + AutomationsPageTitleSwitch.tsx file deletions.
- [x] T3 (protocol+services+CLI layer, 2026-11-10) marketplace RPC chain removed end-to-end:
      shared protocol method constants pluginsMarketplaceAdd/Remove/Update + params schemas +
      ZCodePluginsMarketplaceMutationResult deleted (zcode-protocol/index.ts); zcodeAgentService
      client methods deleted; zcodeAgent.ts interface members deleted; pluginManagementService
      wrapper entries + mutation allowlist (pluginManagement.ts) trimmed; CLI bootstrap server
      switch cases + zcode-protocol/plugins.ts functions deleted; plugins-protocol.test.ts now
      asserts the methods are ABSENT. Core implementations (addZCodePluginMarketplace etc. in
      bootstrap/src/plugins.ts) KEPT — installPlugin/updatePlugin + plugin-reference-catalog
      resolve marketplace sources through them internally.
      Remaining for T3 (UI layer): PluginStorePage.tsx + pluginStoreNavigation.ts deletions
      blocked on extra consumers discovered 2026-11-10 — AnimatedSidePanePanel renders
      PluginStorePage in a side-pane branch (:46/:1420); pluginStoreNavigation consumers:
      WorkspacePluginPreview (:19), MarketingTouchProvider (:15), SettingsPage (:134);
      e2e specs packages/desktop/test/e2e/plugins/plugin-store-*.test.ts. Handle with T4
      (marketing touch is purchase-stack surface) + T6 (e2e).
- [x] T3 (UI layer, 2026-11-10) plugin-store UI removed: PluginStorePage.tsx deleted
      (incl. AnimatedSidePanePanel side-pane branch + plugin-market side-pane tab type
      across workspaceSidePane/useAppPanels/SidePaneTabTrigger/sidePaneTabPresentation +
      new-tab launcher entry + handleOpenPluginMarket thread through App/types/layout),
      pluginStore.ts + pluginManagementStore.ts marketplace-mutation actions removed
      (overview/list data kept for composer mentions), IPluginsService marketplace methods
      removed (retired pluginsService stubs trimmed), marketplacePluginSync prepareSource
      removed (install fails honestly when target marketplace unregistered; syncOptions kept).
      pluginStoreNavigation.ts KEPT — frozen consumer MarketingTouchProvider (PINNED, no
      historical record) imports requestPluginStoreOpen; request/event is a no-op broadcast
      after shell-cut listener removal.
- [x] T4 (entry neutralization, 2026-11-10) purchase surface unreachable: provider neutered
      (openCodingPlanUpgrade = documented no-op returning false; frozen MarketingTouchProvider
      keeps compiling), CodingPlanUpgradeDialog.tsx + codingPlanUpgradeLoginRecovery.ts deleted,
      CodingPlanEntryButton gate neutered to always-ready (quota banners/sidebar degrade to
      plain buttons), SettingsPage automations branch removed, automations orphans deleted
      (AutomationsSection/AutomationsMainBreadcrumbFrame/AutomationsPageTitleSwitch/
      automationsPageTabMemory). Root typecheck EXIT=0; lint 0 errors; architecture 0.
      Remaining T4-deep (orphaned upstream files, unreachable at runtime): CodingPlanEmbeddedWebviewDialog.tsx,
      codingPlanPurchaseAuth.ts, CodingPlanPurchaseChoiceBanners + purchase-token plumbing in
      ModelProviderSection/Detail — removal requires editing upstream-pinned settings files
      (historical-exempt so editable, but large surgery) — schedule with W2 module adoption.
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
