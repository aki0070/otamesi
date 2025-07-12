import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("EXCHANGERATE_API_KEY")

# ドルを取得するURL
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'

# Making our request
response = requests.get(url)
data = response.json()
df = json.loads(json.dumps(data))
# JPYUSDのデータのみ抽出
usd_rate = df['conversion_rates']['JPY']
print(f"１ドルは{usd_rate}円です。")


