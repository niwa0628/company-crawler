from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 🔍 概要キーワードレンジャー（日本語＋英語で構成）
OVERVIEW_KEYWORDS = [
    "会社概要", "企業情報", "会社案内", "企業概要",  # ジャパニーズレッド
    "Company", "About", "About Us", "Corporate Profile"  # イングリッシュブルー
]

# 🛠️ ドライバー起動ブラック
def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    print("[DRIVER] 戦闘準備完了（headless: {}）".format(headless))
    return webdriver.Chrome(options=options)

# 🚀 リンクスキャンイエロー（概要リンク探索隊）
def find_overview_links(driver, base_url, timeout=10):
    print(f"[LINK-SCAN] {base_url} に出動！")
    driver.get(base_url)
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")
    overview_links = []

    for link in links:
        text = link.text.strip()
        href = link.get_attribute("href") or ""
        full_url = urljoin(base_url, href)

        # 🔎 キーワードレーダー発動！
        if any(kw.lower() in (text + href).lower() for kw in OVERVIEW_KEYWORDS):
            overview_links.append((text or "[no-text]", full_url))

    if overview_links:
        print(f"[SUCCESS] {len(overview_links)} 件の概要候補を発見！")
    else:
        print("[EMPTY] 概要らしきリンクは見当たらず…")

    return overview_links
