# Tasks: ZBill M1

**Input**: `.super-speckit/state/spec.md`, `plan.md` · Matrix: `ZBILL-M1-matrix.md`

## Phase 1 — Toolchain (R-001)

- [x] T1.1 mise present; pinned node 24.14.0 + pnpm 10.33.2 available via `mise exec`
- [ ] T1.2 `mise exec -- pnpm install` exit 0 (running, background)
- [ ] T1.3 `mise exec -- pnpm bootstrap` exit 0

## Phase 2 — Build (R-002)

- [ ] T2.1 `mise exec -- pnpm build` exit 0
- [ ] T2.2 Desktop artifact exists (packages/desktop build output / electron-builder dist)

## Phase 3 — Billing skill (R-004 prep)

- [x] T3.1 Create `zbill-billing/` layout decision (see plan.md) — contained, no legacy module edits
- [ ] T3.2 Port pipeline scripts (fetch_receipts/build_report/pdf_export) into zbill-billing/scripts with venv bootstrap script
- [ ] T3.3 Add SKILL.md (agent-invokable: "สร้างรายงานเดือน X" reads receipts dir, runs build, reports output paths)
- [ ] T3.4 Fixtures: copy 4 sample receipts (SPARK/EGAT/PTG/igreen+) into zbill-billing/fixtures/inbox/ with expected outputs

## Phase 4 — Launch & journey QA (R-003, R-004)

- [ ] T4.1 Launch app via `pnpm dev:desktop:test` (isolated data dir); screenshot 3 panels
- [ ] T4.2 Journey: open workspace with fixtures → invoke billing skill → xlsx+PDF produced
- [ ] T4.3 Journey: open produced PDF/xlsx in output panel; Thai correct, images visible

## Phase 5 — Provenance (R-005)

- [ ] T5.1 evidence/upstream-base.md: base SHA a9fe401e, fork additions list, no legacy module edits

## Phase 6 — Convergence & merge

- [ ] T6.1 Independent QA clone + lenses (PStack + Lude) + convergence receipt
- [ ] T6.2 Release checks + merge (authority: repo owner)
