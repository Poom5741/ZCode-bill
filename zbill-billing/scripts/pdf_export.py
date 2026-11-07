#!/usr/bin/env python3
"""สร้าง PDF ด้วย fpdf2 + text shaping (จัดสระ/วรรณยุกต์ไทยถูกต้อง)

หมายเหตุ: reportlab ไม่ทำ Thai shaping ทำให้สระลอย, LibreOffice headless
เครื่องนี้ render ไทยไม่ได้เลย — จึงต้องใช้ fpdf2 + uharfbuzz
"""
import subprocess
from pathlib import Path

from fpdf import FPDF
from PIL import Image as PILImage

THONBURI = "/System/Library/Fonts/Supplemental/Thonburi.ttc"
NAVY = (31, 56, 100)
GRID = (150, 150, 150)
ZEBRA = (242, 245, 250)

# landscape A4: 297 x 210 mm, margin 15
PAGE_W, MARGIN = 297, 15
TABLE_W = PAGE_W - 2 * MARGIN
COL_W = [12, 27, 30, 62, 25, 55, 46]  # รวม 257
IMG_MAX_W, IMG_MAX_H = 42, 30  # mm
LINE_H = 5.2
FONT_S = 9.5


def new_pdf():
    pdf = FPDF(orientation="L", format="A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.add_font("Thonburi", "", THONBURI)
    pdf.add_font("Thonburi", "B", THONBURI)
    pdf.set_text_shaping(True)
    return pdf


def n_lines(pdf, text, width, size=FONT_S):
    """จำนวนบรรทัดเมื่อ wrap ในความกว้าง width (mm)"""
    if not text:
        return 1
    pdf.set_font("Thonburi", size=size)
    return max(1, len(multi_cell_lines(pdf, text, width)))


def multi_cell_lines(pdf, text, width):
    return pdf.multi_cell(w=width, text=str(text), dry_run=True, output="LINES")


def draw_wrapped(pdf, text, x, y, width, size=FONT_S, align="L", style=""):
    pdf.set_xy(x, y)
    pdf.set_font("Thonburi", style=style, size=size)
    pdf.multi_cell(width, LINE_H, text=str(text) if text else "", align=align)


def cell_image(pdf, path: Path, x, y):
    src = Path(path)
    if src.suffix.lower() == ".pdf":
        cache_dir = Path(__file__).resolve().parent.parent / "data" / "processed" / "pdf_png"
        cache_dir.mkdir(parents=True, exist_ok=True)
        png = cache_dir / (src.stem + ".png")
        if not png.exists():
            subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1",
                            "-singlefile", "-q", str(src), str(png.with_suffix(""))],
                           capture_output=True)
        src = png if png.exists() else src
    try:
        with PILImage.open(src) as im:
            w, h = im.size
        scale = min(IMG_MAX_W / w, IMG_MAX_H / h)
        pdf.image(str(src), x=x, y=y, w=w * scale, h=h * scale)
    except Exception:
        draw_wrapped(pdf, "(ไม่พบรูป)", x, y + 10, COL_W[-1] - 4, align="C")


def build_pdf(items, month, title, budget, total, out_path: Path):
    pdf = new_pdf()
    xs = [MARGIN + sum(COL_W[:i]) for i in range(len(COL_W))]
    pad = 2  # mm

    pdf.set_font("Thonburi", style="B", size=14)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(TABLE_W, 9, text=title)
    pdf.set_font("Thonburi", size=10)
    pdf.set_xy(MARGIN, MARGIN + 9)
    pdf.cell(TABLE_W, 6, text=f"ประจำเดือน {month} — วงเงินอนุมัติ {budget:,.2f} บาท")

    y = MARGIN + 20
    header = ["ลำดับ", "วันที่", "หมวดหมู่", "รายละเอียด", "จำนวนเงิน (บาท)",
              "แหล่งที่มา / หมายเหตุ", "รูปประกอบ"]
    aligns = ["C", "C", "C", "L", "R", "L", "C"]

    def header_row(y):
        pdf.set_fill_color(*NAVY)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Thonburi", style="B", size=FONT_S)
        pdf.rect(MARGIN, y, TABLE_W, 9, style="F")
        for i, h in enumerate(header):
            pdf.set_xy(xs[i], y + 2)
            pdf.cell(COL_W[i], 5, text=h, align="C")
        pdf.set_text_color(0, 0, 0)
        return y + 9

    y = header_row(y)
    for idx, it in enumerate(items, 1):
        texts = [str(idx), it["date"], it["category"], it["detail"],
                 f"{it['amount']:,.2f}" if it["amount"] is not None else "-",
                 it["note"], ""]
        widths = [COL_W[i] - 2 * pad for i in range(7)]
        line_counts = [n_lines(pdf, texts[i], widths[i]) for i in range(7)]
        text_h = max(l * LINE_H for l in line_counts) + 2 * pad
        row_h = max(text_h, IMG_MAX_H + 4)
        if y + row_h > 195:  # หน้าใหม่ + หัวตารางซ้ำ
            pdf.add_page()
            y = MARGIN
            y = header_row(y)
        # พื้นหลัง zebra
        if idx % 2 == 0:
            pdf.set_fill_color(*ZEBRA)
            pdf.rect(MARGIN, y, TABLE_W, row_h, style="F")
        # เส้น
        pdf.set_draw_color(*GRID)
        pdf.set_line_width(0.2)
        for i in range(len(COL_W)):
            pdf.rect(xs[i], y, COL_W[i], row_h)
        # ข้อความ
        for i in range(6):
            draw_wrapped(pdf, texts[i], xs[i] + pad, y + pad + 0.5, widths[i],
                         align=aligns[i], style="B" if i == 4 else "")
        cell_image(pdf, it["image"], xs[6] + (COL_W[6] - IMG_MAX_W) / 2, y + 2)
        y += row_h

    # รวมทั้งสิ้น
    y += 4
    bold = "B"
    pdf.set_draw_color(*GRID)
    pdf.rect(xs[3], y, COL_W[3] + COL_W[2], 8)
    pdf.rect(xs[4], y, COL_W[4], 8)
    draw_wrapped(pdf, "รวมทั้งสิ้น", xs[3] + pad, y + 1.5, COL_W[3] + COL_W[2] - 2 * pad, style=bold)
    draw_wrapped(pdf, f"{total:,.2f}", xs[4] + pad, y + 1.5, COL_W[4] - 2 * pad, align="R", style=bold)

    # สรุปตามหมวดหมู่
    y += 12
    by_cat = {}
    for it in items:
        if it["amount"] is not None:
            by_cat[it["category"]] = by_cat.get(it["category"], 0.0) + it["amount"]
    sw = [70, 30, 30]
    sx = [MARGIN + 60, MARGIN + 60 + sw[0], MARGIN + 60 + sw[0] + sw[1]]
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Thonburi", style="B", size=FONT_S)
    pdf.rect(sx[0], y, sum(sw), 8, style="F")
    for i, h in enumerate(["หมวดหมู่", "รวม (บาท)", "สัดส่วน (%)"]):
        pdf.set_xy(sx[i] + pad, y + 2)
        pdf.cell(sw[i] - 2 * pad, 5, text=h, align="C" if i else "L")
    pdf.set_text_color(0, 0, 0)
    y += 8
    rows = sorted(by_cat.items(), key=lambda kv: -kv[1]) + [("รวม", total)]
    for cat, amt in rows:
        rh = 7
        last = cat == "รวม"
        for i in range(3):
            pdf.rect(sx[i], y, sw[i], rh)
        if last:
            pdf.set_fill_color(*ZEBRA)
            pdf.rect(sx[0], y, sum(sw), rh, style="F")
        style = bold if last else ""
        vals = [cat, f"{amt:,.2f}", f"{amt / total * 100:.1f}%" if total else "-"]
        draw_wrapped(pdf, vals[0], sx[0] + pad, y + 1, sw[0] - 2 * pad, style=style)
        draw_wrapped(pdf, vals[1], sx[1] + pad, y + 1, sw[1] - 2 * pad, align="R", style=style)
        draw_wrapped(pdf, vals[2], sx[2] + pad, y + 1, sw[2] - 2 * pad, align="C", style=style)
        y += rh

    # วงเงิน
    y += 4
    remain = budget - total
    pdf.set_font("Thonburi", style="B", size=10)
    pdf.set_text_color(*(192, 0, 0) if remain < 0 else (0, 97, 0))
    pdf.set_xy(MARGIN, y)
    pdf.cell(TABLE_W, 6, text=f"วงเงิน {budget:,.2f} / ใช้ {total:,.2f} / คงเหลือ {remain:,.2f} บาท")
    pdf.set_text_color(0, 0, 0)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))
