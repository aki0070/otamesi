from dotenv import load_dotenv
load_dotenv()

import os
import requests
from pushbullet import Pushbullet
import datetime
import schedule
import time

# 環境変数
API_KEY = os.getenv('OWM_API_KEY')
PB_TOKEN = os.getenv('PB_TOKEN')

# Pushbullet初期化
pb = Pushbullet(PB_TOKEN)

def check_rain():
    try:
        CITY = "Matsuyama,jp"
        URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if 'list' not in data:
            raise ValueError("APIから必要なデータが返ってこなかった！")

        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        target_hours = [6, 9]

        rain_expected = False

        for forecast in data['list']:
            dt_txt = forecast['dt_txt']
            dt = datetime.datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')

            if dt.date() == tomorrow.date() and dt.hour in target_hours:
                weather_main = forecast['weather'][0]['main']
                if 'Rain' in weather_main:
                    rain_expected = True
                    break

        if rain_expected:
            pb.push_note("☂️ 明日の朝、雨予報！", "見守り隊の時間帯は雨かも！傘を準備してください☂️")
        else:
            print("明日の朝は雨予報なし！安心して出動できます！")

    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
    except ValueError as ve:
        print(f"データエラー: {ve}")
    except Exception as ex:
        print(f"予期せぬエラー: {ex}")

# スケジューリング設定（毎日16:00）
schedule.every().day.at("16:00").do(check_rain)

print("スケジューラー起動中！Ctrl+Cで終了できます。")

while True:
    schedule.run_pending()
    time.sleep(60)
