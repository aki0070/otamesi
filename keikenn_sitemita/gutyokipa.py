import random
def janken():
    hands = ["グー","パー","チョキ"]
    while True:
        try:
            user_hand = int(input("あなたの手を入力してください (0:グー, 1:パー,2:チョキ) : "))
            if user_hand not in [0,1,2]:
                raise ValueError
        except ValueError:
            print("0から2の数字を入力してください。")
            continue
        computer_hand =random.randint(0, 2)
        print(f"コンピュータの手: {hands[computer_hand]}")
        if user_hand == computer_hand:
            print("あいこ")
        elif (user_hand - computer_hand + 3) % 3 == 1:
            print("あなたの勝ち！")
        else:
            print("あなたの負け！")
        play_again = input("もう一度a遊びますか？ (y/n): ")
        if play_again.lower() != "y":
            break
if __name__=="__main__":
    janken()
    
