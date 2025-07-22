import pandas as pd

sunspot_file_path = 'SN_m_tot_V2.0.txt' 

df_raw_sunspot = pd.read_csv(sunspot_file_path, header=None, sep=r'\s+', engine='python', 
                             usecols=[0, 1, 2, 3, 4, 5], # インデックス0から5まで（6列）
                             na_values=['-1', '-1.0']) 

# 列に分かりやすい名前をつける (列名を6つに修正)
df_raw_sunspot.columns = ['Year', 'Month', 'Date_Fraction', 'Sunspot_Number', 
                          'Std_Dev', 'Obs_Count'] # <- ここを修正！'Obs_Flag'を削除

# ↓↓↓ その他の処理はコメントアウトを解除し、すべて実行できるようにしてください ↓↓↓

# 黒点数がNaN（欠損値）の行を削除する (観測がない期間は分析から除外)
df_sunspot = df_raw_sunspot.dropna(subset=['Sunspot_Number']).copy()

# 日付列 (YearとMonth) を結合して日付型に変換する
df_sunspot['Date'] = pd.to_datetime(df_sunspot['Year'].astype(str) + '-' + df_sunspot['Month'].astype(str) + '-01')

# 日付をインデックスに設定する（時系列データ分析の基本）
df_sunspot.set_index('Date', inplace=True)

# 必要な列 (Sunspot_Number) だけに絞る
df_sunspot = df_sunspot[['Sunspot_Number']]

# 読み込んだデータの最初の5行と最後の5行を表示して確認
print("--- 太陽黒点データ (先頭) ---")
print(df_sunspot.head())
print("\n--- 太陽黒点データ (末尾) ---")
print(df_sunspot.tail())

# データの情報（欠損値の有無、データ型、期間など）を表示して確認
print("\n--- 太陽黒点データ情報 ---")
print(df_sunspot.info())

# 統計情報を表示
print("\n--- 太陽黒点データ統計 ---")
print(df_sunspot.describe())