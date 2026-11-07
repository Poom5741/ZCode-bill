# Google service plugins — ZBill M2 scope (recorded 2026-11-07)

User request: "add more plugin for google thing like gmail and etc." — recorded as
M2 product scope; intentionally deferred out of M1 (build-prove milestone) so the
current candidate stays contained (Super-SpecKit: changed candidates invalidate proof).

## Plugin set (each = one MCP server + skill, per ZCode plugin architecture)

| Plugin | Transport | Purpose |
|---|---|---|
| gmail | IMAP app-password (works today) + optional Gmail API OAuth in M2 | Fetch receipt emails + attachments; manage labels |
| gdrive | Google Drive API v3 (OAuth, org account) | Pull receipt files from company Drive folders into pipeline |
| gcalendar | Calendar API v3 (OAuth read-only) | Match charging sessions to trips/meetings (business-purpose proof) |
| gsheets | Sheets API v4 (OAuth read-only) | Employee/vehicle registry → per-person allowance limits |

## Auth strategy (customer-facing, differs from our dev shortcut)

- Product default: Google OAuth per org account (customers won't share app passwords).
- Our own dev machines may keep the IMAP app-password path (user preference).
- OAuth client per deployment; tokens stored client-side in app data dir, never in repo.

## Entry point in M2

- New milestone ZBILL-M2 registered in Super-SpecKit with its own purpose/matrix;
  plugins land under `zbill-billing/plugins/<service>/` (contained per architecture policy).

## Current status

- Gmail: working via IMAP (fetch_receipts.py) — promoted to the gmail plugin in M2.
- Drive/Calendar/Sheets: not implemented; no OAuth credentials exist yet.
