import pandas as pd
from crawler.link_extractor import setup_driver, find_overview_links
from crawler.overview_finder import extract_overview_info
from crawler.utils import save_result_to_csv

EXCEL_PATH = "data/company_list.xlsx"
SHEET_NAME = "調査リスト"
URL_COLUMN = "企業ホームページ"
OUTPUT_PATH = "data/results.csv"

def load_company_info(excel_path, sheet_name, url_column, date_column="作業日"):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # フィルタ条件：URLがあって、作業日が空白
    df_filtered = df[df[url_column].notna() & df[date_column].isna()]

    result = []
    for _, row in df_filtered.iterrows():
        result.append({
            "No": row.get("No", ""),
            "社名": row.get("社名", ""),
            "URL": str(row[url_column])
        })

    return result



if __name__ == "__main__":
    companies = load_company_info(EXCEL_PATH, SHEET_NAME, URL_COLUMN)
    
    if companies:
        target = companies[0]
        url = target["URL"]

        print(f"[INFO] 処理対象URL: {url}")

        driver = setup_driver(headless=False)
        try:
            links = find_overview_links(driver, url)
            print("[概要リンク候補]")
            for text, link in links:
                print(f"- {text}: {link}")

            if links:
                first_link = links[0][1]
                print(f"\n[OVERVIEW] {first_link} にアクセスします...")
                result = extract_overview_info(driver, first_link)

                if result["status"] == "success":
                    print("[OK] 概要情報の取得成功")
                    print("📄 テキスト抜粋:")
                    print(result["text_sample"])

                    print("\n📦 抽出結果:")
                    for k, v in result["extracted"].items():
                        print(f"  {k}: {v if v else '（抽出できず）'}")

                else:
                    print("[ERROR] 概要ページの取得に失敗")
                    print(f"理由: {result['reason']}")

            else:
                print("[WARN] 概要リンク候補が見つかりませんでした。")

        finally:
            driver.quit()
    if result["status"] == "success":
        extracted = result["extracted"]
        row = {
             "No": target["No"],
            "社名": target["社名"],
            "URL": first_link,
            "電話番号": extracted["tel"],
            "メールアドレス": extracted["email"],
            "郵便番号": extracted["zip"],
            "住所": extracted["address"],
            "ステータス": "success",
            "エラー理由": ""
        }
    else:
        row = {
             "No": target["No"],
            "社名": target["社名"],
            "URL": first_link,
            "電話番号": "",
            "メールアドレス": "",
            "郵便番号": "",
            "住所": "",
            "ステータス": "error",
            "エラー理由": result["reason"]
        }
    save_result_to_csv(OUTPUT_PATH, row)
    print(f"[CSV] 結果を {OUTPUT_PATH} に保存しました。")