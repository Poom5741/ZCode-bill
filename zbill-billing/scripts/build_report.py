#!/usr/bin/env python3
"""สร้างรายงานค่าใช้จ่ายชาร์จ EV รายเดือน (.xlsx + .pdf)

ใช้งาน:
    1. วางไฟล์หลักฐาน (PDF/รูป) ใน data/inbox/
    2. (ทางเลือก) แก้ metadata ใน data/inbox/items.json
    3. รัน: .venv/bin/python scripts/build_report.py --month 2569-11 --title "..."
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.drawing.image import Image as XlImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "data" / "inbox"
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"

THAI_FONT = "Thonburi"  # ฟอนต์ไทยที่ LibreOffice/macOS มี

IMG_W_PX = 140  # ความกว้างรูปในเซลล์
IMG_H_PX = 180

HEADERS = ["ลำดับ", "วันที่", "หมวดหมู่", "รายละเอียด", "จำนวนเงิน (บาท)",
           "แหล่งที่มา / หมายเหตุ", "รูปประกอบ"]

HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(color="FFFFFF", bold=True, size=11, name=THAI_FONT)
BODY_FONT = Font(size=11, name=THAI_FONT)
TITLE_FONT = Font(size=14, bold=True, name=THAI_FONT)
THIN = Border(*[Side(style="thin", color="999999")] * 4)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")

# คำสำคัญสำหรับ classifier เบื้องต้น (ใช้กับข้อความจาก PDF)
CATEGORY_HINTS = [
    ("ค่าชาร์จ EV", ["charge", "charging", "ev ", "kwh", "ชาร์จ", "สถานีชาร์จ"]),
    ("ค่าจอด/บริการ", ["parking", "service fee", "จอด", "ค่าบริการ"]),
    ("ค่าเดินทาง", ["grab", "taxi", "เดินทาง"]),
]


def guess_category(text: str) -> str:
    low = (text or "").lower()
    for cat, keys in CATEGORY_HINTS:
        if any(k in low for k in keys):
            return cat
    return "ค่าชาร์จ EV"


def guess_amount(text: str):
    """หายอดเงิน: 1) บรรทัดยอดรวมที่มี keyword ชัด 2) ตัวเลขสูงสุด (ยอดรวมรวม VAT มักสูงสุด)"""
    if not text:
        return None
    # บรรทัดยอดรวมที่รู้จัก (EGAT / ทั่วไป / igreen+: จำนวนเงินที่ชำระ)
    for m in re.finditer(
            r"(?:รวมยอดเงินที่ชาระ|รวมยอดเงินที่ชำระ|ยอดชำระ|จำนวนเงินที่ชำระ|"
            r"จำนวนเงินรวม\s*/?\s*Total Amount|Grand Total|รวมทั้งสิ้น|ยอดรวม|Total Amount)"
            r"\D{0,40}?([0-9][0-9,]*\.\d{2})", text, re.I):
        return float(m.group(1).replace(",", ""))
    # เลขที่ตามหลัง ฿/THB/บาท
    amounts = []
    for m in re.finditer(r"(?:฿|THB|บาท)\s*([0-9][0-9,]*\.\d{2})", text or "", re.I):
        amounts.append(float(m.group(1).replace(",", "")))
    if amounts:
        return max(amounts)
    # fallback: ตัวเลขสูงสุดในใบ (ยอดรวมรวมภาษี)
    for m in re.finditer(r"([0-9][0-9,]*\.\d{2})", text):
        try:
            v = float(m.group(1).replace(",", ""))
            if 0.01 <= v < 1_000_000:
                amounts.append(v)
        except ValueError:
            pass
    return max(amounts) if amounts else None


def guess_kwh(text: str):
    m = re.search(r"([0-9]+\.?[0-9]*)\s*kwh", text or "", re.I)
    return float(m.group(1)) if m else None


def guess_date(text: str):
    # igreen+: "เวลา : 26/11/02 19:59" = YY/MM/DD (ค.ศ.)
    m = re.search(r"เวลา\s*:\s*(\d{2})/(\d{1,2})/(\d{2})\s", text or "")
    if m:
        yy, mo, d = (int(x) for x in m.groups())
        try:
            return date(2000 + yy, mo, d).strftime("%d %b %Y")
        except ValueError:
            pass
    m = re.search(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})", text or "")
    if m:
        d, mo, y = (int(x) for x in m.groups())
        if y < 100:
            y += 2500
        if y > 2400:  # พ.ศ.
            y -= 543
        try:
            return date(y, mo, d).strftime("%d %b %Y")
        except ValueError:
            pass
    return ""


def guess_station(text: str):
    """ชื่อสถานี (igreen+: 'สถานี : ...', SPARK: business place)"""
    m = re.search(r"สถานี\s*:\s*([^\n]+)", text or "")
    return m.group(1).strip() if m else ""


def pdf_text(path: Path) -> str:
    try:
        return subprocess.run(["pdftotext", "-layout", "-q", str(path), "-"],
                              capture_output=True, text=True).stdout
    except FileNotFoundError:
        return ""


def collect_receipts(month: str, scan_dir: Path = None):
    """สแกนโฟลเดอร์: PDF/รูป -> ดึงข้อมูลอัตโนมัติ; items.json override ได้"""
    scan_dir = scan_dir or INBOX
    overrides = {}
    mf = scan_dir / "items.json"
    if mf.exists():
        overrides = {o.get("file"): o for o in json.loads(mf.read_text(encoding="utf-8"))}

    items = []
    files = sorted(p for p in scan_dir.iterdir()
                   if p.suffix.lower() in (".pdf", ".jpg", ".jpeg", ".png") and p.is_file())
    for p in files:
        text = pdf_text(p) if p.suffix.lower() == ".pdf" else ""
        ov = overrides.get(p.name, {})
        amount = ov.get("amount", guess_amount(text))
        kwh = ov.get("kwh", guess_kwh(text))
        note = ov.get("note", "")
        detail = ov.get("detail")
        if not detail:
            detail = f"ค่าชาร์จ EV {kwh:.2f} kWh" if kwh else "ค่าชาร์จ EV"
            station = guess_station(text)
            if station:
                detail += f" — สถานี {station}"
            if note:
                detail += f" — {note}"
        items.append({
            "file": p.name,
            "date": ov.get("date", guess_date(text)),
            "category": ov.get("category", guess_category(text + " " + note)),
            "detail": detail,
            "amount": amount,
            "note": note or ("(กรุณากรอกยอดเงิน)" if amount is None else ""),
            "image": p,  # PDF ก็ฝังได้ผ่านการ render; รูปฝังตรง
            "is_pdf": p.suffix.lower() == ".pdf",
        })
    return items


def build_xlsx(items, month, title, budget):
    wb = Workbook()
    ws = wb.active
    ws.title = "รายงาน"
    widths = [8, 16, 18, 42, 16, 30, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.merge_cells("A1:G1")
    ws["A1"] = f"{title}"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A2:G2")
    ws["A2"] = f"ประจำเดือน {month} — วงเงินอนุมัติ {budget:,.2f} บาท"
    ws["A2"].font = Font(size=11, italic=True, name=THAI_FONT)

    row = 4
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.fill, cell.font, cell.alignment, cell.border = HDR_FILL, HDR_FONT, CENTER, THIN
    ws.row_dimensions[row].height = 24

    r = row
    total = 0.0
    for i, it in enumerate(items, 1):
        r += 1
        amount = it["amount"]
        if amount is not None:
            total += amount
        vals = [i, it["date"], it["category"], it["detail"],
                amount if amount is not None else "-",
                it["note"], ""]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font, cell.border = BODY_FONT, THIN
            cell.alignment = RIGHT if c == 5 else (CENTER if c in (1, 2) else LEFT)
        if amount is not None:
            ws.cell(row=r, column=5).number_format = "#,##0.00"
        ws.row_dimensions[r].height = IMG_H_PX * 0.75 + 10

        img_path = it["image"]
        if img_path.suffix.lower() == ".pdf":
            # render หน้าแรกด้วย pdftoppm (soffice เครื่องนี้ render ไทยไม่ได้)
            png_dir = PROCESSED / "pdf_png"
            png_dir.mkdir(parents=True, exist_ok=True)
            png = png_dir / f"{img_path.stem}.png"
            if not png.exists():
                subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1",
                                "-singlefile", "-q", str(img_path), str(png.with_suffix(""))],
                               capture_output=True)
            if png.exists():
                img_path = png
        if img_path.suffix.lower() in (".jpg", ".jpeg", ".png"):
            img = XlImage(str(img_path))
            scale = min(IMG_W_PX / img.width, IMG_H_PX / img.height, 1.0)
            w_px, h_px = int(img.width * scale), int(img.height * scale)
            # twoCellAnchor (viewer บางตัวอ่าน oneCellAnchor ของ openpyxl ไม่ได้)
            from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor
            from openpyxl.utils.units import pixels_to_EMU
            frm = AnchorMarker(col=6, colOff=0, row=r - 1, rowOff=0)
            to = AnchorMarker(col=6, colOff=pixels_to_EMU(w_px), row=r - 1, rowOff=pixels_to_EMU(h_px))
            img.anchor = TwoCellAnchor(editAs="oneCell", _from=frm, to=to)
            ws.add_image(img)

    r += 2
    ws.cell(row=r, column=4, value="รวมทั้งสิ้น").font = Font(bold=True, name=THAI_FONT)
    tc = ws.cell(row=r, column=5, value=round(total, 2))
    tc.font, tc.number_format, tc.border = Font(bold=True, name=THAI_FONT), "#,##0.00", THIN

    # สรุปตามหมวดหมู่
    r += 2
    ws.cell(row=r, column=2, value="สรุปตามหมวดหมู่").font = Font(bold=True, size=12, name=THAI_FONT)
    r += 1
    for c, h in enumerate(["", "หมวดหมู่", "รวม (บาท)", "สัดส่วน (%)"], 1):
        cell = ws.cell(row=r, column=c, value=h)
        cell.fill, cell.font, cell.border = HDR_FILL, HDR_FONT, THIN
    by_cat = {}
    for it in items:
        if it["amount"] is not None:
            by_cat[it["category"]] = by_cat.get(it["category"], 0.0) + it["amount"]
    for cat, amt in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        r += 1
        ws.cell(row=r, column=2, value=cat).font = BODY_FONT
        c3 = ws.cell(row=r, column=3, value=round(amt, 2)); c3.number_format = "#,##0.00"; c3.font = BODY_FONT
        c4 = ws.cell(row=r, column=4, value=f"{amt / total * 100:.1f}%"); c4.font = BODY_FONT
    r += 1
    ws.cell(row=r, column=2, value="รวม").font = Font(bold=True, name=THAI_FONT)
    c3 = ws.cell(row=r, column=3, value=round(total, 2)); c3.number_format = "#,##0.00"; c3.font = Font(bold=True, name=THAI_FONT)
    c4 = ws.cell(row=r, column=4, value="100.0%" if total else "-"); c4.font = Font(bold=True, name=THAI_FONT)
    r += 2
    remain = budget - total
    ws.cell(row=r, column=2, value=f"วงเงิน {budget:,.2f} / ใช้ {total:,.2f} / คงเหลือ {remain:,.2f} บาท").font = Font(bold=True, color="C00000" if remain < 0 else "006100", name=THAI_FONT)

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True

    out_xlsx = OUTPUT / f"ค่าใช้จ่ายชาร์จEV_{month}.xlsx"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    wb.save(out_xlsx)
    fix_drawing_xml(out_xlsx)
    return out_xlsx, total


def fix_drawing_xml(xlsx_path: Path):
    """openpyxl เขียน drawing แบบ default-namespace ซึ่ง viewer บางตัวอ่านไม่ได้
    แปลงเป็นแบบ xdr: prefixed ตามที่ Excel เขียนจริง (zip เขียนใหม่)"""
    import re
    import zipfile
    tags = ["wsDr", "twoCellAnchor", "oneCellAnchor", "absoluteAnchor", "from", "to",
            "col", "colOff", "row", "rowOff", "pic", "nvPicPr", "cNvPr", "cNvPicPr",
            "blipFill", "spPr", "clientData"]
    tmp = xlsx_path.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(xlsx_path) as zin, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if re.match(r"xl/drawings/drawing\d+\.xml$", info.filename):
                s = data.decode("utf-8")
                for t in tags:
                    s = re.sub(rf"<(/?)(?={t}[ />])", r"<\1xdr:", s)
                s = s.replace(
                    '<xdr:wsDr xmlns:a=',
                    '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/'
                    'drawingml/2006/spreadsheetDrawing" xmlns:a=')
                s = re.sub(
                    r'xmlns="http://schemas\.openxmlformats\.org/'
                    r'drawingml/2006/spreadsheetDrawing"', '', s)
                data = s.encode("utf-8")
            zout.writestr(info, data)
    tmp.replace(xlsx_path)


def to_pdf(items, month, title, budget, total):
    """สร้าง PDF ด้วย reportlab (LibreOffice เครื่องนี้ render อักษรไทยไม่ได้)"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from pdf_export import build_pdf
    pdf_path = OUTPUT / f"ค่าใช้จ่ายชาร์จEV_{month}.pdf"
    build_pdf(items, month, title, budget, total, pdf_path)
    return pdf_path if pdf_path.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="เช่น 2569-11 (พ.ศ.-เดือน)")
    ap.add_argument("--title", default="ค่าใช้จ่ายชาร์จ EV ประจำเดือน")
    ap.add_argument("--budget", type=float, default=5000.0)
    ap.add_argument("--dir", default=None, help="โฟลเดอร์ใบเสร็จ (default: data/inbox)")
    args = ap.parse_args()

    scan = Path(args.dir) if args.dir else INBOX
    if not scan.exists() or not any(p for p in scan.iterdir() if p.is_file()):
        print(f"ไม่พบไฟล์ใน {scan} — วางใบเสร็จก่อนแล้วรันใหม่")
        sys.exit(1)

    items = collect_receipts(args.month, scan)
    if not items:
        print("ไม่มีไฟล์หลักฐานที่รู้จัก (.pdf .jpg .png)")
        sys.exit(1)

    xlsx, total = build_xlsx(items, args.month, args.title, args.budget)
    pdf = to_pdf(items, args.month, args.title, args.budget, total)
    missing = [i["file"] for i in items if i["amount"] is None]
    print(f"สร้างแล้ว: {xlsx}" + (f"\nและ: {pdf}" if pdf else " (PDF ล้มเหลว — ลองเปิด LibreOffice ค้างไว้)"))
    print(f"รวม: {total:,.2f} บาท / วงเงิน {args.budget:,.2f}")
    if missing:
        print(f"⚠ รายการที่หายอดเงินไม่ได้ ให้เติมใน items.json: {missing}")


if __name__ == "__main__":
    main()
