import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("EXCHANGERATE_API_KEY")

# 日本円を取得するURL
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/JPY'

# Making our request
response = requests.get(url)
data = response.json()
df = json.loads(json.dumps(data))
# JPYUSDのデータのみ抽出
usd_rate = df['conversion_rates']['USD']
print(f"日本円で１円は{usd_rate}ドルです")

