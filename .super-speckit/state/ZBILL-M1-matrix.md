# Requirements-to-verification matrix — ZBILL-M1

Milestone M1: prove the ZCode fork builds and runs as the ZBill product shell on macOS.

| Requirement ID | Acceptance criterion | Verification method | Automated asset | Runtime/API/DB assertion | Owner | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | Monorepo dependencies install cleanly (`pnpm install` exits 0 on Node ≥22) | CLI exit code in fresh shell | `scripts/verify-m1.sh` | exit code 0 | QA | planned | — |
| R-002 | Desktop app builds from fork source (`pnpm build` relevant packages exit 0) | Build log + produced .app artifact | `scripts/verify-m1.sh` | artifact exists on disk | QA | planned | — |
| R-003 | Built app launches on macOS and shows the 3-panel shell (file tree left, agent center, document panel right) | Manual journey + screenshot from running app | — | screenshot evidence in evidence/ | QA | planned | — |
| R-004 | A billing skill/MCP can be invoked in the running app and produces a monthly report file (xlsx+pdf) visible in the output panel | Journey test with sample receipts from ev-charging-report fixture data | fixture inbox | output files exist + open in viewer | QA | planned | — |
| R-005 | Upstream sync point documented (commit SHA of zai-org/ZCode base, fork diff limited to ZBill additions) | Git evidence | `git log/diff --stat` | documented in evidence/upstream-base.md | maker | planned | — |

## Explicit exclusions

| Requirement ID | Status | Reason | Approval |
| --- | --- | --- | --- |
| R-900 | Windows/Linux packaging | M1 is macOS-only per product decision | Poom 2026-11-07 |
| R-901 | Gmail OAuth wizard | Deferred to M2 (current M1 uses local inbox folder) | Poom 2026-11-07 |
| R-902 | Re-branding/theming (ZBill name, logo) | Deferred to M3 | Poom 2026-11-07 |

No row becomes `verified` from code inspection or OCR alone.
