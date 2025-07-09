try:
    print("最初の数字を入力してください。")
    num1 = int(input())
    print("次の数字を入力してください。") 
    num2 = int(input())
    result = num1 + num2
    print("計算結果:", result)

except ValueError:
    print("エラー: 数字以外が入録されました。正しい数字を入力してください。")

