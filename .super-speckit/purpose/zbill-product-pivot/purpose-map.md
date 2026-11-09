# Purpose Map — zbill-product-pivot

## Intended outcome
ZCode is transformed into **ZBill**: a Windows-first desktop app for creating bill/reimbursement
reports. The agent-chat core stays as the product's interaction model (3-panel shell: file tree /
AI chat / document panel). Bill capability expands beyond today's EV-charging monthly pipeline:
any bill type (not only EV charging), review and editing of extracted items before generation,
in-app report history and archive with re-export, and more output/delivery options beyond the
current xlsx+PDF pair. Most non-billing ZCode design and features are hard-deleted from the
codebase — coding-plan purchase/billing panels, plugin marketplace, automations, remote-connection
device management (SSH/WSL/Docker), web/mobile remote-control surfaces — keeping only what the
bill product and its agent core need.

## People affected
Thai small companies claiming EV/expense allowances (buyers and their finance staff, primary
users); Poom (repo owner/maker); future agents (consumers of the ZBill product contract and
zbill-billing pipeline); upstream ZCode users are no longer a target audience of this fork.

## Success signal
The app builds and launches on Windows presenting as ZBill with a working agent-chat core
(R-101/102); the proven EV pipeline still produces xlsx+PDF (R-103); at least one additional
bill class ingests end-to-end without fabricated amounts (R-104); edited items appear in the
generated report (R-105); past reports are archived, browsable and re-exportable in-app (R-106);
the deleted surfaces are absent from both the running app and the product code with repo checks
green (R-107/108); docs match the surviving product (R-109).

## Non-goals
Google OAuth plugins gmail/gdrive/gcalendar/gsheets (recorded M2 scope, later milestone);
macOS/Linux packaging (Windows-first per owner 2026-11-09); multi-tenant billing; new auth or
payment systems; mobile/web remote control (deleted, not rebuilt); polishing remote-connection
UX (RDUX15 superseded — that domain is being cut).

## Supersession record
- `rdux15-project-device-separation` (state maker_running) is superseded and paused to `blocked`
  with a durable handoff; its artifacts and journey evidence are preserved as history.
- `ZBILL-M1` (branch `zbill/m1-scaffold`, macOS build-proof) is absorbed: its product bits are
  ported onto main; Windows-first replaces macOS-first; the branch remains the historical record.

## Human purpose gate
Confirmed by the repo owner in ADE chat on 2026-11-09 via four scope answers: bill features =
all four axes (any bill type, item review/edit, history/archive, more outputs/delivery);
app shell = keep agent chat core; cut depth = hard-delete modules; platform = Windows first.
Origin quote: "the overgoal i want to transform zcode to not be zcode at all. it should be app
for create bill report as i want but it need more than what feature is now. it also need to cut
down most of design and feature of zcode". Technical implementation choices are deliberately
outside this gate.
