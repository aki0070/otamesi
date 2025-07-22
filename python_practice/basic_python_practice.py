# Part 0: ライブラリのインポート（道具を準備）
import datetime # 日付と時刻を扱うための標準ライブラリ
import random   # ランダムな値を生成するための標準ライブラリ

# Part 1: 定数と初期データの定義（変わらない値と、プログラムが扱う初期の情報）
MAX_TASKS = 3 # 1日に記録できるタスクの最大数
DEFAULT_NAME = "名無しさん" # 名前が入力されなかった場合のデフォルト値
REPORT_TEMPLATE_HEADER = "\n--- 日報レポート ---" # レポートのヘッダー部分
REPORT_TEMPLATE_FOOTER = "--------------------" # レポートのフッター部分

# ユーザーからタスクのステータスを選ぶための選択肢
STATUS_CHOICES = ["完了", "進行中", "未着手", "中断"]

# Part 2: 日報情報を収集する関数（特定の仕事を切り出す）
def collect_report_info():
    """
    ユーザーから日報情報を収集し、辞書として返す関数。
    """
    print("\n--- 日報入力 ---")
    
    # ユーザー名を入力してもらう（入力、変数）
    user_name = input("あなたの名前を入力してください (省略可): ")
    if not user_name: # もしもuser_nameが空っぽなら（条件分岐、論理否定）
        user_name = DEFAULT_NAME # デフォルト名を使う
        print(f"名前が入力されなかったので、{user_name} とします。")

    # 今日の日付を取得（ライブラリの利用、オブジェクトのメソッド）
    today = datetime.date.today() # datetimeライブラリのdateモジュールのtoday()メソッドを呼び出し
    print(f"今日の日付: {today}")

    tasks = [] # 複数のタスクを格納する空のリストを準備（リスト）
    print(f"最大{MAX_TASKS}個のタスクを入力できます。")

    # タスクを繰り返し入力してもらう（forループ、リストへの追加、条件分岐）
    for i in range(MAX_TASKS): # MAX_TASKSの回数だけ繰り返す
        task_description = input(f"タスク{i+1}の内容を入力してください (終了する場合は'q'): ")
        if task_description.lower() == 'q': # 入力が'q'（大文字小文字問わず）ならループを抜ける
            print("タスク入力を終了します。")
            break # ループを抜ける（break文）
        
        # タスクのステータスを選択してもらう（whileループ、条件分岐、リスト、エラーハンドリング）
        while True: # 正しいステータスが入力されるまで繰り返す（無限ループに見えるが、breakで抜ける）
            print(f"  ステータスを選んでください: {STATUS_CHOICES}")
            status_input = input("  ステータス (例: 完了): ").strip() # 前後の空白を削除
            if status_input in STATUS_CHOICES: # もし入力が選択肢の中に存在すれば（in演算子）
                break # 正しい入力なのでループを抜ける
            else:
                print("  無効なステータスです。選択肢の中から選んでください。")

        tasks.append({"description": task_description, "status": status_input}) # リストに辞書を追加（リストメソッド、辞書）
    
    # 収集した情報を辞書として返す（辞書、戻り値）
    return {
        "name": user_name,
        "date": today.strftime("%Y年%m月%d日"), # 日付オブジェクトを文字列に整形
        "tasks": tasks
    }

# Part 3: 日報レポートを生成する関数（別の仕事、引数を受け取る）
def generate_report(report_data):
    """
    収集した日報データからレポート文字列を生成する関数。
    """
    report_lines = [] # レポートの各行を格納する空のリスト

    # ヘッダーを追加
    report_lines.append(REPORT_TEMPLATE_HEADER)
    report_lines.append(f"日付: {report_data['date']}")
    report_lines.append(f"名前: {report_data['name']}")
    report_lines.append("\n--- タスクリスト ---")

    # タスクリストを繰り返し処理（forループ、辞書からの値取得、条件分岐）
    if not report_data['tasks']: # もしタスクリストが空っぽなら
        report_lines.append("本日、登録されたタスクはありませんでした。")
    else:
        for task in report_data['tasks']: # タスクリストの各タスク（辞書）を一つずつ取り出す
            report_lines.append(f"- {task['description']} (状態: {task['status']})")
    
    # フッターを追加
    report_lines.append(REPORT_TEMPLATE_FOOTER)

    # リストの各行を改行で結合して、一つの長い文字列として返す（文字列メソッド、戻り値）
    return "\n".join(report_lines)

# Part 4: メインの実行ブロック（プログラムの開始点）
if __name__ == "__main__":
    print("Python基本構文総仕上げプログラムを開始します。")

    # 日報情報を収集
    daily_report_data = collect_report_info() # collect_report_info()関数を呼び出し、戻り値を受け取る

    # 日報レポートを生成
    final_report = generate_report(daily_report_data) # generate_report()関数を呼び出し、戻り値を受け取る

    # レポートを表示
    print(final_report) # 最終レポートを表示

    print("\nプログラムが終了しました。お疲れ様でした！")