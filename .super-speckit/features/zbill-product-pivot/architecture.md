# Architecture — zbill-product-pivot

Delta on top of the repo architecture policy (root AGENTS.md; docs-only extension —
product code follows the repo rules unchanged). Atlas: .super-speckit/atlas/README.md.
Change story: .super-speckit/atlas/changes/zbill-product-pivot/change-story.md.

## State owners after the pivot

| State | Owner | Notes |
| --- | --- | --- |
| Chat/session runtime | existing host + session runtime (kept) | untouched by wave 1 |
| Provider connection config | ModelProviderSection base + host provider RPCs (kept) | wave 1 deletes only purchase-specific state (purchase-token auth, upgrade dialogs) |
| Bill pipeline inputs | zbill-billing pipeline (Python) | single writer of report outputs |
| Item overrides | items.json contract | UI edits persist here; pipeline reads at generation |
| Report archive index | ONE new store module (wave 3, via hooks) | no per-panel copies; UI never writes report files |
| Skill discovery | skillsService (kept) | marketplace install UI deleted, discovery contract untouched |

## Allowed relationships

- UI components → services via packages/ui/src/hooks; no direct Repo/service calls.
- Purchase/marketplace/automations deletions remove their exclusive service methods and
  host handlers in the same slice; shared methods with the kept agent core stay.
- No new task-protocol fields for the archive index in wave 3; it is renderer-local
  state over workspace files, same layering as existing workspace UI state.

## Deleted boundaries (end state)

- Wave 1: workspaceMainView routes "automations"/"plugin-store", PluginStorePage,
  pluginStoreNavigation, CodingPlanUpgradeDialog, CodingPlanEmbeddedWebviewDialog,
  CodingPlanPurchaseChoiceBanners, codingPlanPurchaseAuth, marketplace management RPCs,
  automations run-history navigation, their i18n keys and e2e specs.
- Wave 2: remote-connection-flow, data-sync device management, web/mobile remote-control
  surfaces, unused provider/store modules, ZBILL_PRODUCT flag itself.
- Deletion rule: hard delete (no shims, no dead exports); knip + typecheck enforce.

## Invariants (verified how)

1. Provider connect path survives (typecheck + journey REQ-102).
2. Skill discovery survives (REQ-103 pipeline regression + skill invocation).
3. Pipeline sole writer of reports (code review + REQ-105/106 journeys).
4. Every wave closes green: typecheck, lint, architecture:check --changed, knip.
