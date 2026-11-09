#!/usr/bin/env python3
"""ดึงอีเมลยืนยันการชาร์จ EV/ใบเสร็จจาก Gmail (IMAP + App Password)

    .venv/bin/python scripts/fetch_receipts.py --month 2569-11   # พ.ศ.-เดือน
    .venv/bin/python scripts/fetch_receipts.py --month 2026-11 --ce

จะค้นหาอีเมลในเดือนนั้น คัดกรองด้วย classifier (คะแนนคำสำคัญ) แล้วดึงไฟล์แนบ
(PDF/รูป) ลง data/inbox/ + เขียน data/inbox/items.json ให้แก้ยอดเงินเองได้
"""
import argparse
import base64
import email
import imaplib
import json
import re
import sys
from datetime import date
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX_DIR = ROOT / "data" / "inbox"
CREDS = Path.home() / ".gmail-imap" / "credentials.json"

# คำสำคัญ classifier: (น้ำหนัก, คำ) — คำ EV ชัดเจน ใช้ตัวเดียวผ่านได้
KEYWORDS = [
    (3, ["ev charg", "charging session", "charging record", "ชาร์จ", "สถานีชาร์จ",
         "kwh", "sparkev", "spark ev", "evti", "elexa", "igreen", "topup",
         "เติมเงิน", "เติมเครดิต"]),
    # คำ generic (receipt/invoice) เอาเพียงตัวเดียวไม่พอ ต้องมี hint จาก sender/คำ EV ร่วม
    (1, ["receipt", "invoice", "ใบเสร็จ", "ใบกำกับ", "payment success",
         "ชำระเงินสำเร็จ", "ยืนยันการชำระ"]),
]
# น้ำหนักพิเศษจาก sender ที่รู้จัก (app ชาร์จ EV ที่ใช้ + เจอจากอีเมลจริง)
# คำสั้นใช้ regex \b กัน match ผิด (เช่น "ev" ไม่ให้โดน "daily.dev")
SENDER_HINTS = [
    (3, ["sparkev.co", "ptg.co.th", "pt.co.th", "egat.co.th", r"\bev\b", "evi",
         "evpop", "chargepoint", "plugit", "haupcar", "voltra", "elexa",
         "igreen", "mea.or.th", "pea-evmobile", "evolt", "pea ev"]),
    # KTC/ธนาคาร: ให้น้ำหนักเฉพาะเมื่อ subject มีแจ้งยืนยันรายการ
    (2, ["ktc.co.th", "kasikornbank.com", "scb.co.th"]),
]

# คำสำหรับ Gmail full-text search (X-GM-RAW) — เจาะทีละคำ ไม่ยิง broad เกิน
GM_QUERY_TERMS = '(elexa OR igreen OR "spark ev" OR evti OR "charging record" OR ' \
                 '"charging session" OR "ev charging" OR ชาร์จ OR เติมเงิน OR topup OR ' \
                 'from:egat.co.th OR from:mea.or.th OR from:pt.co.th OR from:ktc.co.th)'
SPAM_WORDS = ["newsletter", "promotion", "ข่าวสาร", "unsubscribe", "ส่วนลดพิเศษ"]
THRESHOLD = 3


def thai_to_ce(month: str, ce: bool) -> str:
    """แปลง 2569-11 -> 2026-11 (IMAP ใช้ปี ค.ศ.)"""
    if ce:
        return month
    y, m = month.split("-")
    return f"{int(y) - 543:04d}-{m}"


def decode_subj(raw) -> str:
    try:
        return str(make_header(decode_header(raw or "")))
    except Exception:
        return str(raw or "")


def _hint_match(hint: str, text: str) -> bool:
    return bool(re.search(hint, text, re.I)) if hint.startswith(r"\b") else hint.lower() in text


def score(text: str, sender: str = ""):
    low = (text + " " + sender).lower()
    ev_hit = any(k.lower() in low for w, words in KEYWORDS if w >= 3 for k in words)
    generic_hit = any(k.lower() in low for w, words in KEYWORDS if w == 1 for k in words)
    sender_low = sender.lower()
    sender_boost = sum(w for w, words in SENDER_HINTS if any(_hint_match(k, sender_low) for k in words))
    # คำ generic นับเฉพาะเมื่อมี EV hit หรือ sender เป็นที่รู้จักร่วมด้วย
    s = (3 if ev_hit else 0) + ((1 if (ev_hit or sender_boost >= 3) else 0) if generic_hit else 0) + sender_boost
    spam = any(w.lower() in low for w in SPAM_WORDS)
    return s, spam


def search_and_fetch(month_thai: str, ce=False, min_score=THRESHOLD, dry=False):
    c = json.loads(CREDS.read_text())
    m = imaplib.IMAP4_SSL(c["host"], c["port"])
    m.login(c["email"], c["app_password"])
    m.select("INBOX", readonly=True)

    month_ce = thai_to_ce(month_thai, ce)
    y, mo = (int(x) for x in month_ce.split("-"))
    since = date(y, mo, 1)
    nxt = date(y + 1, 1, 1) if mo == 12 else date(y, mo + 1, 1)
    # Gmail full-text search (X-GM-RAW) + กรองช่วงวันที่ด้วย after/before
    # ต้องใช้ literal + CHARSET UTF-8 เพราะ query มีคำไทย (imaplib .literal)
    raw = f'{GM_QUERY_TERMS} after:{since:%Y/%m/%d} before:{nxt:%Y/%m/%d}'
    m.literal = raw.encode("utf-8")
    typ, ids = m.search("UTF-8", "X-GM-RAW")
    if typ != "OK":
        print("ค้นหาล้มเหลว:", typ, ids)
        sys.exit(1)
    id_list = ids[0].split()
    print(f"อีเมลที่ Gmail ค้นเจอในเดือน {month_ce}: {len(id_list)} ฉบับ")

    # ผ่าน 1: ดึง header เป็นชุด (batch 200 ฉบับ/ครั้ง) เพื่อคัดกรอง
    candidates = []
    id_strs = [i.decode() for i in id_list]
    for batch_start in range(0, len(id_strs), 200):
        batch = ",".join(id_strs[batch_start:batch_start + 200])
        typ, msg_datas = m.fetch(batch, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
        for msg_data in msg_datas:
            if not isinstance(msg_data, tuple):
                continue
            msg = email.message_from_bytes(msg_data[1])
            subj = decode_subj(msg["Subject"])
            frm = decode_subj(msg["From"])
            try:
                d = parsedate_to_datetime(msg["Date"]).strftime("%d %b %Y")
            except Exception:
                d = ""
            s, spam = score(f"{subj} {frm}", sender=frm)
            if not spam and s >= min_score:
                candidates.append({"id": msg_data[0].decode().split(" ")[0],
                                   "subject": subj, "from": frm,
                                   "date": d, "score": s, "attachments": []})
    print(f"ผ่านคัดกรองจาก header: {len(candidates)} ฉบับ")

    # ผ่าน 2: ดึงเต็มเฉพาะตัวที่ผ่าน เพื่อเอาไฟล์แนบ
    matched = []
    for c in candidates:
        typ, msg_data = m.fetch(c["id"], "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        matched.append(c)
        if dry:
            continue
        for part in msg.walk():
            fn = part.get_filename()
            if not fn:
                continue
            fn = str(make_header(decode_header(fn)))
            if not re.search(r"\.(pdf|jpe?g|png)$", fn, re.I):
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            INBOX_DIR.mkdir(parents=True, exist_ok=True)
            out = INBOX_DIR / f"{d.replace(' ', '')}_{fn}" if d else INBOX_DIR / fn
            n = 1
            while out.exists():
                out = out.with_name(f"{out.stem}-{n}{out.suffix}")
                n += 1
            out.write_bytes(payload)
            matched[-1]["attachments"].append(out.name)
            print(f"  บันทึก: {out.name}  ({len(payload)//1024} KB)")
    m.logout()

    if not dry and matched:
        mf = INBOX_DIR / "items.json"
        existing = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else []
        known = {e.get("file") for e in existing}
        for e in matched:
            for fn in e["attachments"]:
                if fn not in known:
                    existing.append({"file": fn, "date": e["date"],
                                     "note": f"จากอีเมล: {e['subject'][:60]}"})
        mf.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return matched


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="2569-11 (พ.ศ.) หรือ 2026-11 ถ้าใช้ --ce")
    ap.add_argument("--ce", action="store_true", help="month เป็นปี ค.ศ. แล้ว")
    ap.add_argument("--min-score", type=int, default=THRESHOLD)
    ap.add_argument("--dry", action="store_true", help="แสดงผลคัดกรองอย่างเดียว ไม่ดึงไฟล์")
    a = ap.parse_args()
    results = search_and_fetch(a.month, a.ce, a.min_score, a.dry)
    print(f"\nผ่าน classifier: {len(results)} ฉบับ")
    for e in results:
        print(f"  [{e['score']}] {e['date']} | {e['subject'][:60]} | {e['from'][:40]}")
    if not results:
        print("ไม่พบอีเมลที่ตรง — ลอง --min-score 1 หรือเพิ่มชื่อ app ใน KEYWORDS ของสคริปต์")
