import datetime
import os
import pdfplumber
import requests
from pathlib import Path

PDF_DIR = Path(__file__).resolve().parent.parent
TOKEN   = os.environ["LINE_NOTIFY_TOKEN"]
TODAY   = datetime.date.today()
FILE    = PDF_DIR / f"{TODAY:%Y%m}_給食.pdf"

def extract_menu(pdf_path: Path, target: datetime.date) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    key = f"{target.month}月{target.day}日"
    for line in text.splitlines():
        if key in line:
            return line.strip()
    return f"{key} の献立が見つかりませんでした。"

def send_line(message: str):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    requests.post(url, headers=headers, data={"message": message})

if __name__ == "__main__":
    menu = extract_menu(FILE, TODAY)
    send_line(f"【今日の給食】\n{menu}")
