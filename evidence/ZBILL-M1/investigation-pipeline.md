# Investigation — reusable pipeline (2026-11-07)

Source: ~/hq/ev-charging-report (proven in production for ต.ค./พ.ย. 2569 reports)
- fetch_receipts.py: Gmail IMAP full-text search (X-GM-RAW UTF-8 literal), keyword+sender classifier, attachment download
- build_report.py: pdftotext -layout parsing (SPARK/EGAT-elexa/PTG/igreen+ formats), xlsx via openpyxl (+xdr anchor fix), PDF via fpdf2+HarfBuzz Thai shaping
- Python 3.14 venv deps: openpyxl, Pillow, fpdf2, uharfbuzz; system deps: pdftotext (poppler)
- M1 packaging: bundle scripts as a project skill in the fork repo (skills dir / MCP server); M2 adds OAuth
