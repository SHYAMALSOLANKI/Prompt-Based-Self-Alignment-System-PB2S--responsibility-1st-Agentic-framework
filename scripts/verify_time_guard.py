import json, sys, re
from datetime import date

FUTURE_PHRASES = [
    "in the future", "future date", "because that date is in the future"
]

def extract_dates(text: str):
    t = text.lower()
    out = set()
    for y, m, d in re.findall(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b", t):
        out.add((int(y), int(m), int(d)))
    mons = "jan feb mar apr may jun jul aug sep oct nov dec".split()
    for d, mon, y in re.findall(r"\b(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(20\d{2})\b", t):
        out.add((int(y), mons.index(mon)+1, int(d)))
    for mon, d, y in re.findall(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2}),?\s+(20\d{2})\b", t):
        out.add((int(y), mons.index(mon)+1, int(d)))
    return out

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--file":
        print("usage: python scripts/verify_time_guard.py --file <pb2s_response.json>")
        sys.exit(2)
    data = json.load(open(sys.argv[2], "r", encoding="utf-8"))
    text = data["text"] if "text" in data else data.get("response","")
    user = data.get("user_prompt","")  # optional if you store it
    today = date.today()
    dates = extract_dates(user or "")
    says_future = any(p in (text or "").lower() for p in FUTURE_PHRASES)
    if says_future:
        for y,m,d in dates:
            try:
                if date(y,m,d) <= today:
                    print(f"FAIL: model claimed 'future' for {y:04d}-{m:02d}-{d:02d}")
                    sys.exit(1)
            except ValueError:
                pass
    print("PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
