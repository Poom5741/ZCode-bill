# Research — doc-retriage-2026-11

## What was inspected (with commands actually run)

1. `git log --oneline -15` — repo history is upstream syncs: a9fe401e "chore: sync ZCode source
   v3.17.2" is HEAD; no local feature work after "feat: open source".
2. `docs/issues/**` status scan (scan-2026-11-07.md) — 11 docs marked in-progress across 6 series.
3. `docs/todo/wsl-native-support.md` — header states it is historical (implemented, absorbed into
   `docs/architecture/remote-target-abstraction.md`); excluded from re-triage.
4. Typecheck attempt — failed: node_modules absent; `corepack pnpm install` then completed with
   --ignore-scripts (husky prepare cannot run because pnpm is not on PATH in this environment).
5. Repo layout for the affected claims: remote stack lives in `packages/server/src/remote/`
   (incl. `wsl-backend.ts`), desktop host/main in `packages/desktop/src/`, mobile web in
   `packages/web/`, shared protocol in `packages/shared/src/` (per AGENTS.md and README).

## Relevant conventions and applicability

- Doc statuses are claim records, not ground truth; only code is (AGENTS.md: distinguish confirmed
  causes from hypotheses; execute necessary verification and state honestly when not run).
- The relay-v2 series carries progress notes dated 2026-09-19/09-22 — predates the v3.17.2 sync,
  so verdicts must come from current code only.

## Sources and uncertainty

- Current primary guidance: repository AGENTS.md (loaded into session context), README.md layout.
- Uncertainty: whether upstream absorbed the relay-v2/mobile work is exactly what the triage
  determines per doc; recorded as investigation unknowns, not assumed.
