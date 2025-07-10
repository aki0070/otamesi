import requests
import json

def get_weather_data(api_key, city_name):
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
    API_KEY = "1176ea5c7874e74eb868737dfaa11624"
    CITY = "Tokyo"

    weather_data = get_weather_data(API_KEY, CITY)

    if weather_data:
        try:

            print(f"都市名: {weather_data['name']}")
            print(f"天気: {weather_data['weather'][0]['description']}")
            print(f"気温: {weather_data['main']['temp']}℃")
            print(f"湿度: {weather_data['main']['humidity']}%")
        except KeyError:

            print("エラー: レスポンスからデータを読み取れませんでした。")

