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
