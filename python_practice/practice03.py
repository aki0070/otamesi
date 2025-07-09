try:
    print("最初の文字を入力して下さい。")
    num1 = int(input())

    print("次の数字を入れてください。")
    num2 = int(input())

    result = num1 + num2

    print(f"計算結果: {result}")

    with open("result.txt", "w") as f:
        f.write(f"計算の答えは  {result} です。")

    print("結果を result.txt に 保存しました。")
except ValueError:
    print("エラー: 数字を入力してください。")