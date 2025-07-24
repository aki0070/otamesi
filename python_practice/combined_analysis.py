import pandas as pd
import matplotlib.pyplot as plt # グラフを描画するためのライブラリ
import numpy as np # 数値計算のためのライブラリ（相関分析で使う可能性）

# --- 気象データの読み込みと年次集約 ---
# GHCN-Daily 東京の気象データファイルパス
weather_file_path = 'JA000047662.csv' 

df_raw_weather = pd.read_csv(weather_file_path, header=None, sep=',', engine='python', 
                             usecols=[0, 1, 2, 3, 4, 5, 6, 7], 
                             names=['ID', 'Date', 'Element', 'Value', 'M_Flag', 'Q_Flag', 'S_Flag', 'Obs_Time'],
                             na_values=['-9999'],
                             encoding='utf-8')

df_tmax = df_raw_weather[df_raw_weather['Element'] == 'TMAX'].copy()
df_tmax = df_tmax[['Date', 'Value']]
df_tmax['Date'] = pd.to_datetime(df_tmax['Date'], format='%Y%m%d')
df_tmax['Value'] = df_tmax['Value'] / 10 
df_tmax.rename(columns={'Value': 'Max_Temp_Celsius'}, inplace=True)
df_tmax.set_index('Date', inplace=True)
df_tmax_yearly = df_tmax['Max_Temp_Celsius'].resample('Y').mean().to_frame()
df_tmax_yearly.rename(columns={'Max_Temp_Celsius': 'Yearly_Max_Temp_Celsius'}, inplace=True)


# --- 太陽黒点データの読み込みと年次集約 ---
sunspot_file_path = 'SN_m_tot_V2.0.txt' 

df_raw_sunspot = pd.read_csv(sunspot_file_path, header=None, sep=r'\s+', engine='python', 
                             usecols=[0, 1, 2, 3, 4, 5], 
                             na_values=['-1', '-1.0']) 

df_raw_sunspot.columns = ['Year', 'Month', 'Date_Fraction', 'Sunspot_Number', 
                          'Std_Dev', 'Obs_Count'] 

df_sunspot = df_raw_sunspot.dropna(subset=['Sunspot_Number']).copy()
df_sunspot['Date'] = pd.to_datetime(df_sunspot['Year'].astype(str) + '-' + df_sunspot['Month'].astype(str) + '-01')
df_sunspot.set_index('Date', inplace=True)
df_sunspot = df_sunspot[['Sunspot_Number']]

df_sunspot_yearly = df_sunspot['Sunspot_Number'].resample('Y').mean().to_frame()
df_sunspot_yearly.rename(columns={'Sunspot_Number': 'Yearly_Sunspot_Number'}, inplace=True)

# --- ここからステップ4: データの結合と相関分析 ---

# 結合のために、両方のDataFrameのインデックス（日付）を揃える
# Pandasのmergeメソッドを使って、日付（インデックス）を基準に結合します
# how='inner' は、両方のDataFrameに存在する日付のみを残します（共通期間）。
df_combined = pd.merge(df_tmax_yearly, df_sunspot_yearly, left_index=True, right_index=True, how='inner')

# 結合されたデータの先頭と末尾を表示
print("--- 結合された年次データ (先頭) ---")
print(df_combined.head())
print("\n--- 結合された年次データ (末尾) ---")
print(df_combined.tail())

# データの情報と統計を表示
print("\n--- 結合された年次データ情報 ---")
print(df_combined.info())
print("\n--- 結合された年次データ統計 ---")
print(df_combined.describe())

# 相関係数を計算する
# DataFrameのcorr()メソッドで、各列間の相関係数を計算できます
correlation_matrix = df_combined.corr()
print("\n--- 最高気温と黒点数の相関行列 ---")
print(correlation_matrix)

# 特定の相関係数を取り出す（最高気温と黒点数の相関）
correlation_value = correlation_matrix.loc['Yearly_Max_Temp_Celsius', 'Yearly_Sunspot_Number']
print(f"\n年ごとの最高気温と太陽黒点数の相関係数: {correlation_value:.4f}")

# --- ステップ5: データの可視化作業（グラフ作成）---

# Matplotlibのグラフ描画設定（日本語表示対応）
plt.rcParams['font.family'] = 'DejaVu Sans' # デフォルトのフォント（日本語非対応）
plt.rcParams['axes.unicode_minus'] = False # 負の符号（-）を正しく表示

# 日本語フォントの設定（Ubuntuの場合。必要に応じて他のフォント名に修正）
# 例: 'IPAexGothic', 'Noto Sans CJK JP' などがインストールされていれば使えます
# もし日本語が文字化けする場合は、Ubuntuに日本語フォントをインストールする必要があります。

try:
    # 正しいフォント名を指定します
    plt.rcParams['font.family'] = 'IPAexGothic' 
    plt.rcParams['axes.unicode_minus'] = False # 負の符号（-）を正しく表示

    # （以前のtry-exceptブロックはフォントインストール後のため、基本的にtryブロックが実行されます）
except Exception as e: # 広範なExceptionをキャッチ
    print(f"フォント設定エラー: {e}")
    print("日本語フォントが見つからないか、設定に問題があります。グラフの日本語が文字化けする可能性があります。")
    print("フォント名が正しいか、OSにフォントがインストールされているか確認してください。")
    print("例: sudo apt install fonts-ipaexfont")


# グラフの作成
plt.figure(figsize=(15, 7)) # グラフのサイズを設定

# 最高気温のプロット
plt.plot(df_combined.index, df_combined['Yearly_Max_Temp_Celsius'], label='年ごとの最高気温 (℃)', color='red')

# 太陽黒点数のプロット（第2軸を使って重ねる）
# 気温と黒点数はスケールが大きく異なるため、見やすくするためにy軸を2つ使います
ax2 = plt.twinx() # 2つ目のy軸を作成
ax2.plot(df_combined.index, df_combined['Yearly_Sunspot_Number'], label='年ごとの太陽黒点数', color='blue')

# グラフのタイトルとラベル
plt.title('東京の年ごとの最高気温と太陽黒点数の推移', fontsize=16)
plt.xlabel('年', fontsize=12)
plt.ylabel('年ごとの最高気温 (℃)', fontsize=12, color='red')
ax2.set_ylabel('年ごとの太陽黒点数', fontsize=12, color='blue') # 2つ目のy軸のラベル

plt.grid(True) # グリッド線を表示

# 凡例を表示 (pltとax2の両方の凡例を表示させるため、handlesとlabelsを結合して渡す)
h1, l1 = plt.gca().get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
plt.legend(h1+h2, l1+l2, loc='upper left') # 凡例を表示

plt.tight_layout() # レイアウトを自動調整
plt.show() # グラフを表示

print("\n--- プロジェクト完了 ---")