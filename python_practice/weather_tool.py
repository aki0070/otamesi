import os
import sys
import requests
import json
import argparse
from dotenv import load_dotenv
# .envファイルから環境変数を組み込む
load_dotenv()

def get_weather_data(api_key, city_name):
    #指定された都市の天気データを取得して返すa関数
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ja"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"エラー: APIリクエストに失敗 - {e}")
        return None
    except json.JSONDecodeError:
        print("エラー: レスポンスの解析に失敗。")
        return None

if __name__== "__main__":
    # .envファイルからAPIキーを読み込む
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    # APIキーが設定eeされているか確認
    if not API_KEY:
        print("エラー: APIキーが.envファイルに設定されていません。")
        sys.exit(1) # プログラムを終了
    #１．パーサー（因数解析器）を作成
    parser = argparse.ArgumentParser(description="指定された都市の現在の天気を表示します。")
    #２.受け付ける因数を定義
    parser.add_argument("--city", default="Matsuyama", help="天気を表示する都市名（例：Tokyo)")
    #　３．実際に因数を解析
    args = parser.parse_args() 

    CITY = args.city

    print(f"---{CITY}の天気を検索します ---")
    weather_data = get_weather_data(API_KEY, CITY)

    if weather_data:
        try:

            print(f"都市名: {weather_data['name']}")
            print(f"天気: {weather_data['weather'][0]['description']}")
            print(f"気温: {weather_data['main']['temp']}℃")
            print(f"湿度: {weather_data['main']['humidity']}%")
        except KeyError:

            print("エラー: レスポンスからデータを読み取れませんでした。")
