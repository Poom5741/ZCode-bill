# Requirements Matrix — doc-retriage-2026-11

Purpose (user-confirmed via ADE chat, 2026-11-07): evidence-first pass over all docs marked
"in-progress" against the current v3.17.2 code; close what's done; surface what is genuinely open.

Completion predicate (falsifiable): every in-progress-marked doc listed below has a triage verdict
with cited code evidence, and `docs/issues/RETRIAGE-2026-11.md` records all verdicts.

| # | Requirement | Doc | Verification seam | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| REQ-01 | Verdict for remote-connection-ux/01 with cited code evidence | docs/issues/remote-connection-ux/01-remote-connection-ux-optimization.md | Cross-check claimed features against current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-02 | Verdict for remote-performance-3-16/01 | docs/issues/remote-performance-3-16/01-remote-session-lag-analysis.md | Cross-check analysis claims against current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-03 | Verdict for remote-startup-failures-3-16/01 | docs/issues/remote-startup-failures-3-16/01-source-server-startup-failure-triage.md | Cross-check triage claims against current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-04 | Verdict for ttft-stage-telemetry/01 | docs/issues/ttft-stage-telemetry/01-local-send-stage-observability.md | Check whether instrumented stages exist in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-05 | Verdict for ttft-stage-telemetry/02 | docs/issues/ttft-stage-telemetry/02-queued-retry-and-failure-diagnostics.md | Check whether retry/failure diagnostics exist in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-06 | Verdict for web-remote-control-relay-v2/02 | docs/issues/web-remote-control-relay-v2/02-shared-v2-contract-and-fake-relay.md | Check contract/fake-relay artifacts in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-07 | Verdict for web-remote-control-relay-v2/03 | docs/issues/web-remote-control-relay-v2/03-desktop-v2-register-token-pair.md | Check register/token-pair implementation in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-08 | Verdict for web-remote-control-relay-v2/04 | docs/issues/web-remote-control-relay-v2/04-desktop-auth-gate-and-lifecycle.md | Check auth gate/lifecycle implementation in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-09 | Verdict for web-remote-control-relay-v2/05 | docs/issues/web-remote-control-relay-v2/05-mobile-login-and-qr-direct-connect.md | Check mobile login/QR implementation in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-10 | Verdict for web-remote-control-relay-v2/06 | docs/issues/web-remote-control-relay-v2/06-mobile-device-list-and-last-device.md | Check device-list implementation in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-11 | Verdict for web-remote-control-relay-v2/07 | docs/issues/web-remote-control-relay-v2/07-contract-v1-removal-and-docs.md | Check V1 contract removal status in current source | triage report row | resolved (docs/issues/RETRIAGE-2026-11.md) |
| REQ-12 | Consolidated triage report exists, cites evidence per row, no status flipped without evidence | docs/issues/RETRIAGE-2026-11.md | Report review | triage report | resolved (docs/issues/RETRIAGE-2026-11.md) |

Rules: verdicts are `done (evidence)` / `still-open (evidence + next action)` / `obsolete (reason)`.
No product code changes. Doc status lines are updated only when the evidence supports the flip.
