# Playbook — doc-retriage-2026-11

Selected PStack playbook: `investigation` (vendor/pstack/skills/poteto-mode/playbooks/investigation.md,
pinned revision e5a8186d7b43be8d6ac4452440fbead5f1a51c70), applied through the adapter override
contract. The upstream playbook is read-only; this delivery extends it with doc-status writes after
investigation completes (per its own "investigation precedes a change → route to Feature" rule).

Falsifiable completion predicate: all 12 matrix rows REQ-01–REQ-12 have evidence-backed verdicts and the
consolidated report exists; `super_speckit.py status --strict` shows all matrix rows resolved.

## Ordered source steps (all pending → completed/skipped with evidence)

1. **Route through the `how` skill** (and `why` for motivation questions) — status: completed (evidence: docs/issues/RETRIAGE-2026-11.md, scan-2026-11-07.md)
   - Application: for each doc, trace its claims to concrete current-code entry points (how);
     record why-status where the doc states motivation.
2. **Throughput checkpoint: `throughput checkpoint: n/a, read-only investigation`** — status: completed (recorded at phase start; evidence: this playbook)
   - Application: kept verbatim; the phase is read-only until the final status-write pass.
3. **Produce how-shaped output / recommendation with tradeoffs** — status: completed (evidence: docs/issues/RETRIAGE-2026-11.md verdict table)
   - Application: per-doc verdict table (done / still-open / obsolete) with a tradeoffs note on
     what re-opening vs closing each doc costs.
4. **Apply the unslop skill to the reply** — status: completed (evidence: docs/issues/RETRIAGE-2026-11.md — plain declarative sentences, no filler)
   - Application: plain declarative sentences in the report and reply; no AI-isms, no filler.

## Delivery-only steps (from playbook-delivery contract, not upstream)

5. Write per-doc verdict evidence into triage report `docs/issues/RETRIAGE-2026-11.md` — completed
6. Update each triaged doc's status line only where evidence supports it — skipped (reason: all 11 in-progress markers verified accurate; no evidence supports a flip; report records per-doc remaining tails instead)
7. Independent checker re-verifies a sample of verdicts against code in a QA clone — pending (checker phase)

## Skips

- Delivery step 6 (doc status-line edits): all 11 in-progress markers verified accurate; no evidence
  supports a flip, so per matrix rules the docs stay untouched and the report carries the verdicts.
