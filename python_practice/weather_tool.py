import requests
import json

API_KEY = "1176ea5c7874e74eb868737dfaa11624"
CITY_NAME = "Matsuyama"

url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric&lang=ja"

try:
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    print(f"都市名: {data['name']}")
    print(f"天気: {data['weather'][0]['description']}")
    print(f"気温: {data['main']['temp']}℃")
    print(f"湿度: {data['main']['humidity']}%")

except requests.exceptions.RequestException as e:
    print(f"エラー: APIへのリクエストに失敗しました - {e}")
except json.JSONDecodeError:
    print("エラー: レスポンスの解析に失敗しました。")
except KeyError:
    print("エラー: レスポンスから予期せぬデータ形式を受け取りました。")

