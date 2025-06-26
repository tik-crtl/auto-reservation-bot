from datetime import datetime, timedelta
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ① ユーザー情報
NAME = "田中太陽"
EMAIL = "is0730xf@ed.ritsumei.ac.jp"
STUDENT_ID = "28433"
FACULTY = "情報理工学部"

# ② 曜日ごとの希望時間帯（0=月曜, ..., 6=日曜）
RESERVATION_SCHEDULE = {
    0: ["14:30～15:45", "15:45～17:00"],
    1: ["13:15～14:45"],
    2: ["13:15～14:45"],
    3: ["17:00～18:15", "18:15～19:30"],
    4: ["17:00～18:15", "18:15～19:30"]
}

# ③ ヘッドレスChrome起動
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    # ④ 予約ページへアクセス
    driver.get("https://select-type.com/rsv/index.php")

    # ⑤ 来週の今日の曜日と日付を取得
    today = datetime.today()
    target_day = today + timedelta(days=7)
    target_weekday = target_day.weekday()
    target_day_str = target_day.strftime("%Y/%m/%d")

    # ⑥ 該当曜日に希望時間がなければスキップ
    if target_weekday not in RESERVATION_SCHEDULE:
        print("今日は予約対象の曜日ではありません。")
    else:
        print(f"来週（{target_day_str}）の予約を開始します...")
        time.sleep(3)  # ページ読み込み待機（調整可）

        # ⑦ 利用可能なボタン一覧を取得し、希望時間を探す
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OICトレーニングルーム')]")
        reserved = False

        for btn in buttons:
            for desired in RESERVATION_SCHEDULE[target_weekday]:
                if desired in btn.text and "×" not in btn.text:
                    btn.click()
                    time.sleep(1)

                    # ⑧ 「次へ」をクリック
                    driver.find_element(By.XPATH, "//button[contains(text(), '次へ')]").click()
                    time.sleep(1)

                    # ⑨ 入力フォーム記入
                    driver.find_element(By.NAME, "name").send_keys(NAME)
                    driver.find_element(By.NAME, "email").send_keys(EMAIL)
                    driver.find_element(By.NAME, "email2").send_keys(EMAIL)
                    driver.find_element(By.NAME, "textfield1").send_keys(STUDENT_ID)
                    driver.find_element(By.NAME, "textfield2").send_keys(FACULTY)

                    # ⑩ 最後の「次へ」で送信（本番ではボタン押下を有効に）
                    driver.find_element(By.XPATH, "//button[contains(text(), '次へ')]").click()
                    print(f"✅ {target_day_str} の {desired} を予約しました。")
                    reserved = True
                    break
            if reserved:
                break

        if not reserved:
            print(f"❌ {target_day_str} の希望時間は満席でした。")

finally:
    driver.quit()
