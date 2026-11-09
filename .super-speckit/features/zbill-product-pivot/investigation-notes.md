# Investigation notes — zbill-product-pivot (2026-11-09)

throughput checkpoint: n/a, read-only investigation

Scope: overgoal pivot from ZCode (coding agent desktop app) to ZBill (bill-report app,
Windows-first, agent-chat core kept, non-billing features hard-deleted). This pass maps
what exists, what is already ported, and what the cut/extend waves must cover. Deeper
per-wave import-graph mapping happens before each maker wave and updates this receipt.

## Observed facts (verified today)

1. Prior ZBill work exists on branch `origin/zbill/m1-scaffold` (8 commits, fork point
   a9fe401e). Its product bits are now PORTED onto main (38 files): ZBill product mode
   (`__ZBILL_PRODUCT__` vite define, `ZBILL_PRODUCT` const in packages/shared/src/env.ts,
   sidebar entry hiding in ProjectSidebarNavigation.tsx, `mise.toml` dev task env), the
   proven `zbill-billing/` pipeline (build_report.py / fetch_receipts.py / pdf_export.py +
   EV fixtures, smoke-tested 941.15 THB report per branch evidence), GOOGLE-PLUGINS-M2
   scope record, and ZBILL-M1 purpose/matrix/evidence as historical artifacts.
   Vendored `.super-speckit` kit content from the branch was NOT ported (main's is newer);
   `super-speckit.yml` stays main's richer version; skill-registration dirs are gitignored
   machine-local state on main.
2. Port verification: `pnpm typecheck` clean, `pnpm lint` 0 errors (89 pre-existing warnings).
3. Cut candidates identified at product level (exact import graphs pending wave investigations):
   - Wave 1 (UI entry removal + route deletion): coding-plan purchase panels
     (packages/ui CodingPlan* / purchase flow), plugin marketplace entry + surface,
     automations entry + surface (see ProjectSidebarNavigation.tsx hiding today).
     Wave-1 investigation must separate "purchase UI" (delete) from "provider
     connection config" the agent core still needs for model access (keep).
   - Wave 2 (module deletion): remote-connection-flow + data-sync device management
     (SSH/WSL/Docker), web/mobile remote-control link (packages/web, packages/server,
     remote relay), provider/store purchase modules not needed by the agent core.
   - Keep: agent core (session runtime, protocol, CLI runtime, host), 3-panel shell,
     document panel (report viewing), settings skeleton, workspace folder open.
4. Bill extension points (wave-3 detail pending): zbill-billing pipeline is a Python venv
   CLI; in-app review/edit can ride items.json overrides now and a purpose-built review
   surface later; report archive can live under the workspace output dir browsable via
   the document panel; output formats already xlsx+PDF (fpdf2 + HarfBuzz Thai shaping).

## Decisions carried from owner (2026-11-09 chat)

- Features: any bill type; item review/edit; report history/archive; more outputs/delivery.
- Shell: keep agent chat core (3-panel), strip everything non-billing around it.
- Cut: hard-delete modules (not flag-hiding).
- Platform: Windows first (macOS packaging later).

## Unknowns (bounded, none decision-critical for routing)

- Full import graph per cut wave (the per-wave investigations produce the exact keep-list).
- Which provider/store modules the local agent runtime still requires for model access
  (wave-1 investigation must distinguish "purchase UI" from "provider connection config").
- Document-panel archive UX shape (bill-feature wave; product decision within confirmed purpose).

## Conventions applied (from repo AGENTS.md / packages/ui/AGENTS.md)

- UI accesses services via hooks; no direct Repo/service access from components.
- Zustand state in src/store; single owner per state; no duplicate write paths.
- Deletions must keep typecheck/lint/architecture checks green; no dead exports (knip).
- Docs (AGENTS.md/DESIGN.md/CONTEXT.md) updated in the same change as behavior removal.

## Wave-1 module map (added 2026-11-10, evidence-linked)

### Marketplace (delete surface, keep discovery)
- Main view route: workspaceMainView === "plugin-store" in packages/ui/src/App.tsx (lines ~884-998:
  handleNavigateToPluginStoreMain, pluginStoreOpenVersion, onNavigateToPluginStore wiring).
- Page component: packages/ui/src/settings/PluginStorePage.tsx (imported by
  packages/ui/src/app-shell/WorkspaceShellLayout.tsx:63).
- Exclusive service RPCs: zcodeAgentService.addPluginMarketplace / updatePluginMarketplace
  (App.tsx:844-846) - marketplace INSTALL/management calls; host side to be traced in maker work.
- KEEP: packages/services/src/skills/skillsService.ts discoverSkills - reads workspace/repo skill
  dirs and installed plugin roots independently of the marketplace UI (skillsService.ts:840,
  1036, 1061); zbill-billing skill discovery must not regress.
- Navigation lib: packages/ui/src/lib/pluginStoreNavigation.ts (addPluginStoreOpenListener).

### Automations (delete surface)
- Main view route: workspaceMainView === "automations" (App.tsx:881; WorkspaceShellLayout.tsx:
  1454, 2159, 2338-2358, 2779-2799 render automations main + run-history navigation).
- Entry: ProjectSidebarNavigation Automations button (already hidden under ZBILL_PRODUCT).
- Run-history cross-workspace navigation logic in WorkspaceShellLayout.tsx:1527-1536 goes with it.

### Coding-plan purchase (delete surface; KEEP provider connection)
- Surfaces: packages/ui/src/settings/CodingPlanUpgradeDialog.tsx,
  CodingPlanEmbeddedWebviewDialog.tsx (purchase webview + CodingPlanPurchaseCompletePayload),
  model-provider-section Detail.tsx CodingPlanPurchaseChoiceBanners (:594,:878) and
  onCodingPlanPurchaseComplete plumbing (:254,:303,:638,:755), ModelProviderSection.tsx
  purchase-token refresh state (:380-609,:849,:1206).
- KEEP: ModelProviderSection base provider add/edit/connection + API key management - the agent
  runtime needs a configured provider for model access. Purchase-token auth
  (codingPlanPurchaseAuth.js) and upgrade/discount UI go; connection/refresh of provider
  credentials stays.
- Services packages/services/src/coding-plan-subscription/* + usage-stats purchase providers:
  audit in maker work; delete only members with no remaining UI/runtime callers.

### Known blast radius (maker work refines)
- i18n keys (workspace.openScheduledSettings, plugin-store.*, automations.*, coding plan
  purchase strings) - remove keys only after last reference dies (knip will flag).
- E2E: packages/desktop/test/e2e references purchase/marketplace/automations flows
  (marketing-touch-*, coding-plan entitlement tests) - delete or rewrite with the surfaces.
- App.tsx / WorkspaceShellLayout.tsx are shared shells; every removal must keep chat/task
  main views, settings, and web-remote-control shell conditionals compiling.
