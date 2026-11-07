# Requirements Matrix — rdux15-project-device-separation

Authoritative requirement source: docs/issues/remote-connection-ux/15-project-device-selection-and-connection-management.md
(confirmed Q1–Q12 product decisions + RDUX15-01..25 acceptance scenarios) and #21 chat-entry contract
(RDUX21-01..24). Purpose confirmed by repo owner's "continue work on" instruction (ADE chat
cc7b7010, 2026-11-07) following the lane's evidence-based proposal of ticket 15.

Completion predicate (falsifiable): every REQ below maps to implemented code + executable evidence
(E2E/UI-integration per the ticket's Testing Decisions) or an explicit environment-blocked
not-verified rationale recorded in the feature handoff; native Spec Kit spec/plan/tasks exist and
converge with the implementation.

| ID | Requirement | Ticket anchor | Verification seam | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| REQ-01 | Project + opens direct-create form (name, device, source folder), no local/remote pre-screen | Q1, RDUX15-01 | Desktop E2E from local task / remote task / no task | E2E run record | pending |
| REQ-02 | Device defaults: current task's device, else "此电脑"; offline device kept with visible status, no silent local switch | Q3, RDUX15-02/03 | Desktop E2E + UI timing | E2E + integration record | pending |
| REQ-03 | Device dropdown lists only added devices (online+offline); discovery candidates and unrecognized profiles excluded | Q4, RDUX15-03 | UI integration + E2E | integration record | pending |
| REQ-04 | All add-connection entries (project form, chat menu, settings) open Settings→Remote devices categorized add window, SSH default | Q5, RDUX15-04/05 | Three-entry Desktop E2E | E2E records | pending |
| REQ-05 | Add window: SSH config-host discovery + manual, WSL distros (supported platforms), Docker containers + manual; discovery failure doesn't block manual entries | Q5, RDUX15-05 | UI integration + supported-platform E2E | integration + E2E records | pending |
| REQ-06 | Selecting an existing device never connects; online → Add folder opens directory browser; offline → explicit Connect-and-choose-folder with progress/confirmations inside the project flow | Q6, RDUX15-06/07 | Desktop E2E incl. real remote | E2E records | pending |
| REQ-07 | Device switch after folders selected requires Q7 confirmation (clears folders, keeps name); cancel keeps all values | Q7, RDUX15-08/09 | Desktop E2E + UI timing | E2E + integration records | pending |
| REQ-08 | Settings-sourced add completes in device management (locate device card), no folder/project continuation | Q8, RDUX15-10 | Real remote Desktop E2E | E2E record | pending |
| REQ-09 | Project-draft device-add round trip returns to the same draft with Q7 confirmation on return when folders exist; cancel restores draft | Q10, RDUX15-11/12/13 | Desktop E2E | E2E records | pending |
| REQ-10 | Chat-source add: after every connection choose remote folder, resolve per #21 (RDUX21-01..24), enter project before send; cancel restores original target | Q11, RDUX15-14 | Desktop E2E + UI/service timing | E2E records | pending |
| REQ-11 | Existing-project secondary entry: attach original project identity, list in same dialog, draft retained on return, duplicate-add makes no duplicate entry; read-only legacy remote supported | Q9, RDUX15-15/16 | Desktop E2E + project-service contract | E2E + contract records | pending |
| REQ-12 | Local project capabilities preserved (zero/multi roots); remote = exactly one fixed root; failures create no ghost projects | Out-of-scope guards, RDUX15-17 | Desktop E2E + project-service contract | records | pending |
| REQ-13 | Credential/install/upgrade confirmations preserved and retryable; original completion intent survives; unused new credentials don't overwrite stored ones | Q12, RDUX15-18/21/22 | Real remote E2E + credential/Host contracts | records | pending |
| REQ-14 | Background continue: progress owned by settings device card / pending item; completion notifies without hijacking navigation; failure keeps config+reason with retry | Q12, RDUX15-19 | Desktop E2E + UI timing | records | pending |
| REQ-15 | Cancel/close/Esc semantics: cancel only the unfinished attempt, keep saved records and shared connections; close-after-success never disconnects; Esc follows top-layer-first rule | Q12, RDUX15-13/20/21 | Desktop E2E + UI timing | records | pending |
| REQ-16 | Late/cancelled results are inert: stale requests never reopen dialogs, navigate, create projects, or overwrite new drafts | 决策 19/20, RDUX15-20 | UI integration + existing handoff E2E | records | pending |
| REQ-17 | Keyboard/a11y: device dropdown, confirmations, focus restoration, Esc layering; status not color-only; long names/paths don't cover primary actions | 决策 22/23, RDUX15-23 | Desktop E2E + a11y assertions | records | pending |
| REQ-18 | Visual/theme coverage: light/dark, zh-CN/en-US, normal/narrow windows; WSL only on supported platforms; Docker unavailable vs no-candidates distinguishable | 决策 23/24, RDUX15-24 | Visual evidence + platform E2E | records | pending |
| REQ-19 | Web/mobile regression: shared UI respects Host capabilities, no nonexistent settings entries, no separate remote session, replayable recovery unaffected | 决策 25, RDUX15-25 | Web/mobile regression + Host contracts | records | pending |
| REQ-20 | Native Spec Kit artifacts (spec/plan/tasks) exist, match this matrix, and converge with implementation; draft/cancel timing tests added where E2E is unstable | Testing Decisions | Artifact review + converge receipt | artifacts + receipts | pending |
