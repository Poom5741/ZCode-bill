# Durable handoff — rdux15-project-device-separation (paused to blocked, 2026-11-09)

## Why paused
The repo owner declared an overgoal pivot (ADE chat 10e5b846, 2026-11-09): ZCode becomes
ZBill, a Windows-first bill-report app, with most non-billing ZCode design and features
hard-deleted. The remote-connection domain this feature improves is scheduled for deletion
(wave 2), not polish. Continuing maker work here would invest in code being removed.
Successor feature: `zbill-product-pivot` (purpose confirmed, route milestone, decision
trail DT-ZPIVOT-01 records the supersession).

## State at pause
- State was `maker_running`; no code candidate existed (candidate_sha null, runs empty).
  All committed work on main is docs/pipeline state + journey evidence (T1 gap analysis,
  RDUX15-01/02/03/04/05/09 real-app journeys via ADE computer-use, Windows scope PASS).
- Completed receipts: investigation (registered), personas, shared-design, baseline-feedback,
  phase contract (plan.md), research notes, architecture; grill complete; purpose confirmed.
- Working tree at pause: clean before the pivot port; the pivot ported zbill/m1-scaffold
  product bits onto main in the same session (see zbill-product-pivot decision trail).

## What a future resumer needs
1. Read `zbill-product-pivot` purpose map and matrix first — if the cut waves proceed,
   this feature never resumes; its domain disappears.
2. If the pivot is ever reversed by the owner, resume from this feature's registered
   receipts (all digest-frozen under .super-speckit/features/rdux15-project-device-separation/),
   re-run the T1 re-execution plan per investigation-notes.md (tests exist; Windows scope
   verified for RDUX15-04/05; SSH-dependent scenarios remain not-verified per DT-RDUX15-02).
3. Journey UX executor contract (DT-RDUX15-01) and SSH-host decision (DT-RDUX15-02) remain
   recorded in this feature's decision trail as history.

## Transfer
same-environment (ADE lane a5862aba), stage: pivot-supersession, attempt: handoff-pivot-1.
