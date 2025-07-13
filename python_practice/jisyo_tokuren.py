person_info = {
    "name": "明宏",
    "age": 59,
    "occupation": "警察官"
}

print(f"個人情報: {person_info}")

#　特定のキーの値を取り出す
print(f"名前: {person_info['name']}")

#　値を更新（既存のキーに代入）
person_info["occupation"] = "プログラマー"
print(f"職業を変更後: {person_info}")

person_info["city"] = "松山市"
print(f"居住地を追加後: {person_info}")

#　存在しないキーを使うとエラーになるのでget.()メソッドを使うと安全。
email = person_info.get("email", "未登録")
print(f"メールアドレス: {email}")
