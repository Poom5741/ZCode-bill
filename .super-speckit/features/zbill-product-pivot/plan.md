# Plan — zbill-product-pivot

Technical approach for the ZBill pivot in three maker waves; investigation findings in
./investigation-notes.md (wave-1 module map, evidence-linked). This plan is the phase
contract for the milestone.

## Reused seams (verified in code)

- ZBill product mode: `__ZBILL_PRODUCT__` vite define (packages/desktop/vite.config.ts) →
  `ZBILL_PRODUCT` const (packages/shared/src/env.ts) → sidebar entry hiding
  (packages/ui/src/project-sidebar/ProjectSidebarNavigation.tsx); dev task env in mise.toml.
- Bill pipeline: `zbill-billing/scripts/` (build_report.py / fetch_receipts.py /
  pdf_export.py), fixtures + items.json overrides; output = xlsx+PDF (fpdf2 + HarfBuzz).
- Skill discovery: packages/services/src/skills/skillsService.ts `discoverSkills` —
  independent of marketplace UI; stays.
- Shared shells: workspaceMainView routing in App.tsx + WorkspaceShellLayout.tsx;
  settings provider UI in ModelProviderSection.tsx + model-provider-section/Detail.tsx.

## Architecture contract (delta; product code follows repo AGENTS.md)

- Single owner: report archive index owned by one store module (via hooks) once REQ-106
  lands; pipeline remains the only writer of report files (UI never hand-edits outputs).
- Purchase-token auth, marketplace management RPCs, and automations run-history
  navigation are wave-1 deletions; no compatibility shims, no flag-kept dead code —
  hard delete per owner decision.
- Provider connection (ModelProviderSection base + host provider config RPCs) is
  protected: wave-1 edits must not remove provider add/edit/connect paths.
- skillsService discovery contract protected: deleting marketplace must keep local/repo
  skill loading green (zbill-billing skill invocable — REQ-103 regression covers it).
- ZBILL_PRODUCT flag retires in wave 2, not wave 1 (grill Q4).

## Testing approach

Repo checks per slice: pnpm typecheck, pnpm lint, pnpm architecture:check --changed,
knip for dead exports after each deletion batch. Journey evidence (REQ-101/102/105/106)
via ADE computer-use on the real dev instance (view/cancel-only on user data), recorded
as receipts with screenshots. Pipeline evidence (REQ-103/104) via CLI runs on fixtures
with output-file assertions. chromedriver is Application-Control-blocked on this host;
wdio E2E specs referencing deleted surfaces are removed/rewritten in the same slice and
recorded as coverage changes in matrix evidence.

## Milestone slices (ordered)

- W1 cut (REQ-101, 103, 107): remove automations + plugin-store routes/components/RPCs;
  remove coding-plan purchase dialogs/banners/token-auth; delete or rewrite affected e2e
  specs; remove dead i18n keys; checks green; real-app journey (ZBill launch + chat).
- W2 cut (REQ-102, 108, 109): remove remote-connection-flow + data-sync device management,
  web/mobile remote-control surfaces, unused provider/store modules per keep-list
  investigation; retire ZBILL_PRODUCT flag; update docs (AGENTS.md/DESIGN.md/CONTEXT.md);
  journey: local workspace open + chat round trip.
- W3 bill features (REQ-104, 105, 106): second bill-class parser + fixture; item review
  flow (items.json overrides at minimum, purpose-built review surface if tractable);
  report archive dir + document panel browsing + re-export; journey: edit item →
  regenerate → open archived report.

Slice reassessment after each wave per unified pipeline.
