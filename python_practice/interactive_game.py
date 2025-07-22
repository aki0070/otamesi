import random #　乱数生成ライブラリ

print("---数当てゲームへようこそ！---")
print("１から10の数を当ててみてね。")

secret_number = random.randint(1,10)
guess = 0 #　ユーザーの数字を初期化（初回は０aなので条件はTRUEになる）

while guess != secret_number:
    try:
        guess_str = input("あんたの予想は？: ")
        guess = int(guess_str)
        
        if guess < secret_number:
            print("もっと大きいよ")
        elif guess > secret_number:
            print("もっと小さいよ")
        else:
            print(f"🎉正解！{secret_number}")
    except ValueError:
        print("それは数字じゃないよ！ 数字を入力してね。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

print("ゲーム終了！")
