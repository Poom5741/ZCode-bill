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

## Auth strategy (DECIDED 2026-11-07, user feedback)

**User verdict: nobody will do the "create your own Google Cloud project" dance — it's too hard.**
Product rule: the customer never opens Google Cloud Console.

- **ZBill ships its own OAuth client**: we create ONE Google Cloud project + consent screen
  once (vendor-side); customers only click "Sign in with Google" and pick their account.
- OAuth client per deployment is NOT required; vendor-hosted client covers all customers.
- Gmail scope is "restricted" at Google → plan for OAuth verification lead time (or start
  with unverified-test-mode limited to pilot customers while in review).
- **App password stays as fallback** ("advanced connection" option) — power users who
  prefer it, and as a working path if Google verification is still pending.
- Tokens stored client-side in app data dir, never in the repo.

## Entry point in M2

- New milestone ZBILL-M2 registered in Super-SpecKit with its own purpose/matrix;
  plugins land under `zbill-billing/plugins/<service>/` (contained per architecture policy).

## Current status

- Gmail: working via IMAP (fetch_receipts.py) — promoted to the gmail plugin in M2.
- Drive/Calendar/Sheets: not implemented; no OAuth credentials exist yet.
