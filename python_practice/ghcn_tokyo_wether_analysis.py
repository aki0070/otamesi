import pandas as pd

weather_file_path = 'JA000047662.csv'

# ファイルをPandasのDataFrameとして読み込む（pd.read_csv に戻す！）
# 区切り文字をカンマ','に指定。カンマで区切られているのでsep=','
# engine='python' はsepに正規表現を使わないので不要だが、付けておいても問題なし
# usecolsはカンマ区切りで読み込んだ際の列番号を指定
df_raw_weather = pd.read_csv(weather_file_path, header=None, sep=',', engine='python', 
                             usecols=[0, 1, 2, 3, 4, 5, 6, 7], # 0から7列目までを読み込み (ID, DATE, ELEMENT, VALUE, M_FLAG, Q_FLAG, S_FLAG, Obs_Time)
                             names=['ID', 'Date', 'Element', 'Value', 'M_Flag', 'Q_Flag', 'S_Flag', 'Obs_Time'],
                             na_values=['-9999'],
                             encoding='utf-8')

# ↓↓↓ 以下は以前指示した確認用のprint文。このままにしておいてください ↓↓↓
print("--- df_raw_weather の先頭 ---")
print(df_raw_weather.head(10)) 
print("\n--- df_raw_weather の情報 ---")
print(df_raw_weather.info())
print("\n--- df_raw_weather の Element 列ユニーク値 ---")
print(df_raw_weather['Element'].unique()) 
# ↑↑↑ ここまで確認用print文。これ以降のコードは一時的にコメントアウトされている状態 ↓↓↓

# 最高気温 (TMAX) のデータだけを抽出する (ここも修正が必要です！.str.strip()を削除)
df_tmax = df_raw_weather[df_raw_weather['Element'] == 'TMAX'].copy() # <- ここを修正！

# 必要な列 (日付と値) だけに絞る
df_tmax = df_tmax[['Date', 'Value']]

# 日付列を日付型に変換する ('YYYYMMDD'形式)
df_tmax['Date'] = pd.to_datetime(df_tmax['Date'], format='%Y%m%d')

# 気温の値 (Value) を華氏の10分の1単位から摂氏に変換する
# (Value / 10) が華氏の数値です。これを摂氏に変換 (摂氏 = (華氏 - 32) * 5 / 9)
df_tmax['Value'] = df_tmax['Value'] / 10

# 列名をより分かりやすく変更
df_tmax.rename(columns={'Value': 'Max_Temp_Celsius'}, inplace=True)

# 日付をインデックスに設定する（時系列データ分析の基本）
df_tmax.set_index('Date', inplace=True)

# 読み込んだデータの最初の5行と最後の5行を表示して確認
print("--- 東京の最高気温データ (先頭) ---")
print(df_tmax.head())
print("\n--- 東京の最高気温データ (末尾) ---")
print(df_tmax.tail())

# データの情報（欠損値の有無、データ型、期間など）を表示して確認
print("\n--- 東京の最高気温データ情報 ---")
print(df_tmax.info())

# 統計情報を表示
print("\n--- 東京の最高気温データ統計 ---")
print(df_tmax.describe())