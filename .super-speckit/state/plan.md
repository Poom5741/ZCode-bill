# Implementation Plan: ZBill M1

**Branch**: `zbill/m1-scaffold` · **Spec**: `.super-speckit/state/spec.md` · **Created**: 2026-11-07

## Architecture summary

Reuse upstream ZCode desktop (Electron, packages/desktop) unchanged in M1. ZBill additions are locally contained (architecture-policy: no edits inside legacy modules):

```
zbill-billing/            # NEW top-level: skill definition + pipeline port
  skill.json / SKILL.md   #   agent-facing definition ("สร้างรายงานเดือน X")
  scripts/                #   port of ~/hq/ev-charging-report scripts (fetch/build/pdf)
  fixtures/inbox/         #   sample receipts for journey QA
evidence/                 # delivery evidence (already started)
```

## Tech stack & decisions

| Decision | Choice | Rationale |
|---|---|---|
| Toolchain | mise (pinned node 24.14/pnpm 10.33) | mise.toml is authoritative (C1) |
| Report generation | Existing Python pipeline via venv | Proven in production; port unchanged |
| PDF engine | fpdf2 + uharfbuzz (Thai shaping) | LibreOffice broken for Thai here; reportlab floats Thai vowels |
| Skill form | Project skill the agent can invoke (M1); MCP wrapper deferred | Fastest path to Story 3; skill system already ships with ZCode |
| Electron mirror | Override ELECTRON_MIRROR to official if npmmirror slow | Investigation unknown U1 |

## Phases

1. **Toolchain** (R-001): install mise + pinned node/pnpm → `pnpm install`
2. **Build** (R-002): `pnpm build`; resolve native/ build issues as they surface
3. **Billing skill** (R-004 prep): port pipeline scripts + fixtures into zbill-billing/
4. **Launch & journey** (R-003, R-004): `pnpm dev:desktop:test` (isolated data dir), run skill in app, verify output panel
5. **Provenance** (R-005): document upstream base SHA + fork diff

## Risks

- Electron binary download latency/failure from TH network (mitigate: ELECTRON_MIRROR override, retry)
- native/ modules may need Xcode CLT specifics
- dev:desktop:test may require provider/model config — use isolated config with a reachable endpoint

## Verification

Matrix `.super-speckit/state/ZBILL-M1-matrix.md` rows R-001..R-005; runtime journeys required for R-003/R-004 (screenshots + produced files), static review never suffices.
