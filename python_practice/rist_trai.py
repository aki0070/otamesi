hobbies = ["読書", "知恵の輪", "十字架パズル", "ルービックキューブ"]
print(f"私の趣味リスト: {hobbies}")
print(f"一番最初の趣味: {hobbies[0]}")
print(f"趣味の数: {len(hobbies)}")

hobbies.append("料理")
print(f"新しい趣味を追加後: {hobbies}")

hobbies[1] = "プログラミング"
print(f"趣味を変更後: {hobbies}")

hobbies.insert(2, "水耕栽培")
print(f"趣味を追加後{hobbies}")

