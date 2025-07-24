import requests
import json
import datetime
import os
from dotenv import load_dotenv

# --- 設定項目 ---
# 環境変数からSlack Webhook URLを読み込む (重要: 直接コードに書かない)
load_dotenv() # .env ファイルを読み込む
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# OpenWeatherMap API設定
MATSUYAMA_LAT = 33.8406
MATSUYAMA_LON = 132.7668
# OpenWeatherMap Forecast APIのURL (翌日の予報を取得するため)
API_BASE_URL = "https://api.open-meteo.com/v1/forecast" 

# Part 1: 天気予報を取得する関数
def get_next_day_weather_forecast(lat, lon, base_url):
    """
    翌日の天気予報（最高気温、降水確率、降水量）を取得し、辞書で返す関数。
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,precipitation_sum,precipitation_probability_max",
        "timezone": "Asia/Tokyo",
        "forecast_days": 2 # 今日と翌日の2日間の予報を取得
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        # 翌日（インデックス1）のデータを抽出
        # APIのレスポンス構造: daily -> time[1], temperature_2m_max[1], etc.
        next_day_date = data['daily']['time'][1]
        next_day_max_temp = data['daily']['temperature_2m_max'][1]
        next_day_precipitation_sum = data['daily']['precipitation_sum'][1]
        next_day_precipitation_prob = data['daily']['precipitation_probability_max'][1]

        # 翌日の午前7時の雨予報を判断 (降水量や降水確率を考慮)
        is_rainy = False
        if next_day_precipitation_sum > 0.5 and next_day_precipitation_prob >= 50: # 降水量が0.5mm以上で降水確率50%以上
            is_rainy = True
        elif next_day_precipitation_prob >= 80: # 降水確率80%以上なら少量でも雨と判断
            is_rainy = True

        return {
            "date": next_day_date,
            "max_temp_celsius": next_day_max_temp,
            "precipitation_sum_mm": next_day_precipitation_sum,
            "precipitation_probability_percent": next_day_precipitation_prob,
            "is_rainy_forecast": is_rainy # 雨予報ならTrue、でなければFalse
        }
        
    except requests.exceptions.RequestException as e:
        print(f"天気予報APIエラー: {e}")
        return None
    except json.JSONDecodeError:
        print("天気予報APIエラー: レスポンス解析失敗。")
        return None
    except KeyError as e:
        print(f"天気予報APIエラー: 必要なデータが見つかりません - {e}")
        return None
    except Exception as e:
        print(f"天気予報APIエラー: 予期せぬエラー - {e}")
        return None

# Part 2: Slackへ通知を送信する関数
def send_slack_notification(message, webhook_url):
    """
    SlackのIncoming Webhookを使用してメッセージを送信する関数。
    """
    if not webhook_url:
        print("Slack Webhook URLが設定されていません。")
        return False
        
    headers = {'Content-Type': 'application/json'}
    payload = {'text': message}
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # HTTPエラーがあれば例外発生
        # ↓↓↓ ここから追加 ↓↓↓
        print(f"Slackサーバー応答ステータスコード: {response.status_code}")
        print(f"Slackサーバー応答本文: {response.text}")
        # ↑↑↑ ここまで追加 ↓↑↑

        if response.text == 'ok':
            print("Slack通知を送信しました。")
            return True
        else:
            print(f"Slack通知送信失敗: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Slack通知エラー: {e}")
        return False
    except Exception as e:
        print(f"Slack通知エラー: 予期せぬエラー - {e}")
        return False

# Part 3: メインの実行ブロック
if __name__ == "__main__":
    print("--- こども見守り隊 雨通知サーバー ---")
    
    # 翌日の天気予報を取得
    forecast = get_next_day_weather_forecast(
        MATSUYAMA_LAT,
        MATSUYAMA_LON,
        API_BASE_URL
    )
    
    notification_message = ""
    if forecast:
        # 通知メッセージを作成
        if forecast['is_rainy_forecast']:
            notification_message = (
                f"🚨 明日 ({forecast['date']}) は雨の予報です 🚨\n"
                f"最高気温: {forecast['max_temp_celsius']}℃\n"
                f"降水量: {forecast['precipitation_sum_mm']}mm, 降水確率: {forecast['precipitation_probability_percent']}%\n"
                "子供たちの安全に注意しましょう！傘の準備も忘れずに！"
            )
        else:
            notification_message = (
                f"🌤️ 明日 ({forecast['date']}) は雨の心配はありません 🌤️\n"
                f"最高気温: {forecast['max_temp_celsius']}℃\n"
                "傘は必要ありません。元気にいってらっしゃい！"
            )
        
        print("\n通知メッセージ:\n", notification_message)
        
        # Slackへ通知を送信
        send_slack_notification(notification_message, SLACK_WEBHOOK_URL)
        
    else:
        print("天気予報の取得に失敗したため、通知を送信できません。")
    
    print("\n--- 処理終了 ---")