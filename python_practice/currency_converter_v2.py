import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("EXCHANGERATE_API_KEY")
bace_currency ="JPY"
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{bace_currency}"

try:
    #　APIから全データを取得
    response = requests.get(url)
    response.raise_for_status()#エラーがあればここで停止
    data = response.json()
    #　APIリクエストが成功したか確認
    if data.get("result") == "success":
        #　ユーザーに入力を求める
        amount_jpy = float(input("変換したい日本円の金額を入力してください: "))
        target_currency = input("変換先の通貨コードを入力してください(例:　USD): ")
        #　レートを辞書から安全に取り出す
        rates = data.get("conversion_rates", {})
        target_rate = rates.get(target_currency)

        #　レートが見つかった場合のみ計算を実行
        if target_rate:
            converted_amount = amount_jpy * target_rate
            print("---")
            #　f-stringを使った数値フォーマット
            print(f"{amount_jpy:,.0f}円は、約 {converted_amount:,.4} {target_currency}です。")
        else:
            print(f"エラー: 通貨コード '{target_currency}' が見つかりません。")
    else:
        print("エラー: APIから為替レートを取得できませんでした。")

except requests.exceptions.RequestException as e:
    print(f"ネットワークエラー: {e}")
except ValueError:
    print("エラー: a正しい金額（数字）を入力してください。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")

