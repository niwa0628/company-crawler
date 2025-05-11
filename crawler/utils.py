import re
import csv
from pathlib import Path

def extract_company_info(text):
    """
    ページ本文から電話番号・メール・住所らしき情報を抽出
    """
    result = {
        "tel": None,
        "email": None,
        "zip": None,
        "address": None
    }

    # 電話番号
    tel_match = re.search(r"0\d{1,4}-\d{1,4}-\d{3,4}", text)
    if tel_match:
        result["tel"] = tel_match.group()

    # メールアドレス
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        result["email"] = email_match.group()

    # 郵便番号
    zip_match = re.search(r"\d{3}-\d{4}", text)
    if zip_match:
        result["zip"] = zip_match.group()

    # 住所（都道府県＋市区町村らしき行を抽出）
    address_match = re.search(r"(東京都|北海道|(?:京都|大阪)府|.{2,3}県)[^\n]{5,40}", text)
    if address_match:
        result["address"] = address_match.group()

    return result

def save_result_to_csv(path, row, header=None):
    file = Path(path)
    write_header = not file.exists()
    
    with open(file, mode="a", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header or row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)