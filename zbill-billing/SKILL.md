---
name: zbill-billing
description: Generate the monthly EV-charging reimbursement report (xlsx+PDF) from a folder of receipt PDFs/images. Use when the user asks for "รายงานค่าชาร์จ", "สร้างรายงานเดือน X", monthly reimbursement report, or to process new receipts in zbill-billing/fixtures/inbox.
---

# ZBill Billing — monthly EV-charging reimbursement report

You generate a company-ready reimbursement report from receipt files using the
proven pipeline in `zbill-billing/scripts/`. Thai output (fpdf2 + HarfBuzz
shaping) — never use LibreOffice headless for Thai PDFs on this machine.

## Steps

1. **Setup (once per machine)**: create the Python venv and system deps:
   ```bash
   cd zbill-billing
   python3 -m venv .venv
   .venv/bin/pip install openpyxl Pillow fpdf2 uharfbuzz
   # system: pdftotext comes with poppler (brew install poppler)
   ```

2. **(Optional) fetch from Gmail**: `scripts/fetch_receipts.py --month 2569-XX`
   needs `~/.gmail-imap/credentials.json` (IMAP app password). Skip if the user
   already placed receipts in the inbox folder.

3. **Build the report**: receipts live in `zbill-billing/fixtures/inbox/`
   (or any folder the user names):
   ```bash
   zbill-billing/.venv/bin/python zbill-billing/scripts/build_report.py \
     --month 2569-XX --dir <receipts-folder> --budget 5000 \
     --title "ค่าใช้จ่ายชาร์จ EV ประจำเดือน"
   ```
   Outputs land in `output/` as `ค่าใช้จ่ายชาร์จEV_<month>.xlsx` and `.pdf`.

4. **Verify and report back**: check both files exist; if the script warns
   about missing amounts, list the files and ask the user to fill
   `items.json` (file → amount/date/detail overrides), then rebuild.
   Present the output file paths so the user can open them in the document panel.

## Supported receipt formats

SPARK EV (charging record / topup tax invoice), EGAT/elexa receipts, PTG/PTC
E-Tax invoices, igreen+ app exports (`OrderDetails_*.pdf`, no email exists for
this app — user exports from the app). Unknown formats: extraction may miss
amounts; the script flags them via items.json warnings.

## Rules

- Never edit legacy ZCode modules; all changes stay inside `zbill-billing/`
- Credentials never go into the repo (`~/.gmail-imap/` only)
- If a month folder is empty, tell the user — do not fabricate data
