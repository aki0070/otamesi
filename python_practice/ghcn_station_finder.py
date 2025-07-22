import pandas as pd

# GHCN-Daily観測地点リストファイルのパス
stations_file_path = 'ghcn-stations.csv'

# CSVファイルをPandasのDataFrameとして読み込む
# カンマ区切り、ヘッダーなし、特定の列だけ読み込む（緯度、経度、標高、地点ID、国コード、州コード、地点名）
# ファイルの実際の列構造に合わせてusecolsのインデックスを調整する必要があるかもしれません。
# ドキュメント ghcnd-stations.txt を見ると、以下の列が該当します。
# ID         (0-11)
# LATITUDE   (12-19)
# LONGITUDE  (20-29)
# ELEVATION  (30-37)
# STATE      (38-39) (州コード、国の場合は空)
# NAME       (40-70) (地点名)
# GSN FLAG   (71-74)
# HCN/CRN FLAG (75-78)
# WMO ID     (79-85)
# CSV形式なので、区切り文字はカンマで、文字位置ではなく列番号で指定します。
# ただし、ghcnd-stations.csvは固定幅フォーマットのテキストをCSVとして提供しているため、
# read_fwf (fixed-width formatted)を使う方が正確です。
# 一旦、read_csvで試してみて、うまくいかなければread_fwfに切り替えましょう。

# ghcnd-stations.csv は、固定幅テキスト形式で、カンマ区切りではないので、read_csvではなくread_fwfが適しています。
# 各列の幅を指定します。
col_widths = [11, 9, 10, 7, 3, 31, 5, 5, 6] # ID, LAT, LON, ELEV, STATE, NAME, GSN, HCN, WMOID
col_names = ['ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE', 'NAME', 
             'GSN_FLAG', 'HCN_CRN_FLAG', 'WMO_ID'] # 列に名前をつけます

df_stations = pd.read_fwf(stations_file_path, widths=col_widths, names=col_names, encoding='utf-8')

# 日本の観測地点だけをフィルタリングする
# 国コードはIDの最初の2文字で示されます。日本の場合は'JA'です。
df_japan_stations = df_stations[df_stations['ID'].str.startswith('JA')]

# 読み込んだ日本の観測地点の最初の数行を表示して確認
print(df_japan_stations.head())

# 日本の観測地点の数を表示
print(f"\n日本の観測地点数: {len(df_japan_stations)}地点")

# 東京に近い地点を探すヒントとして、名前や緯度・経度でフィルタリングする例も書いておきます。
# df_tokyo_stations = df_japan_stations[df_japan_stations['NAME'].str.contains('TOKYO', na=False)]
# print("\n東京の観測地点（名前でフィルタ）:")
# print(df_tokyo_stations)

# 東京の観測地点を探す (緯度経度でフィルタリング)
# 東京タワーの緯度経度はおおよそ 緯度: 35.6586, 経度: 139.7454 です。
# その緯度経度に近い地点を探します。
# あるいは、NAME列に'TOKYO'が含まれる地点を探します。

# NAME列に'TOKYO'が含まれる地点を探す例 (小文字・大文字を区別しない検索)
df_tokyo_stations = df_japan_stations[
    df_japan_stations['NAME'].str.contains('TOKYO', case=False, na=False)
]
print("\n東京の観測地点（名前でフィルタ）:")
print(df_tokyo_stations)

# もしこれで適切な地点が見つからなければ、緯度経度でさらに絞り込むことも検討します。
# 例: 緯度が35度台、経度が139度台の地点を探す
# df_tokyo_nearby = df_japan_stations[
#    (df_japan_stations['LATITUDE'] >= 35.0) & (df_japan_stations['LATITUDE'] <= 36.0) &
#    (df_japan_stations['LONGITUDE'] >= 139.0) & (df_japan_stations['LONGITUDE'] <= 140.0)
# ]
# print("\n東京周辺の観測地点（緯度経度でフィルタ）:")
# print(df_tokyo_nearby)