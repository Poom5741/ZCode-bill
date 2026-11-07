# Purpose Map — rdux15-project-device-separation

## Intended outcome
Desktop users create/add projects directly from one form (name, device, source folder) without a local/remote pre-screen; all add-connection entries route to Settings > Remote devices with a categorized SSH/WSL/Docker add window and an explicit Add-and-connect completion point; completion intent dispatches by origin so drafts survive device round trips.

## People affected
Desktop users (primary); repo owner (confirmed Q1-Q12 on 2026-10-12/14 in ticket 15/#21); ADE agent lane a5862aba (implementer); future agents (consumers of the updated connection UX contract)

## Success signal
All RDUX15-01..25 scenarios carry executable evidence or an explicit environment-blocked not-verified rationale; preserved capabilities hold (local multi-root, existing-project attach, credential/install confirmations); Web/mobile regression shows no capability leakage.

## Non-goals
No transport/auth/install/reconnect state machine changes; no save-only mode; no remote multi-root; no cross-restart draft persistence; no mobile remote-management expansion; no ssh-agent work; no task protocol or workspace identity changes.

## Human purpose gate
This map is a draft. A human confirms that this is the intended purpose, or corrects it. Technical implementation choices are deliberately outside this gate.
