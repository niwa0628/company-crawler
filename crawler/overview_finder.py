from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler.utils import extract_company_info

def extract_overview_info(driver, url, wait_time=10):
    """
    概要ページにアクセスして本文と抽出情報を取得。
    """
    print(f"[OVERVIEW] アクセス中: {url}")
    try:
        driver.get(url)

        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        body_text = driver.find_element(By.TAG_NAME, "body").text
        extracted = extract_company_info(body_text)

        return {
            "status": "success",
            "source_url": url,
            "text_sample": body_text[:300],
            "extracted": extracted
        }

    except Exception as e:
        return {
            "status": "error",
            "source_url": url,
            "reason": str(e),
            "extracted": None
        }