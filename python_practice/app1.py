import tkinter as tk
import random

def dispLabel():
    kuji = ["大吉","中吉","小吉","凶"]
    lbl.configure(text=random.choice(kuji))

root = tk.Tk()
root.geometry("600x400")

lbl = tk.Label(text="今日の運勢は？")
btn = tk.Button(text="ボタン", command = dispLabel)

lbl.pack()
btn.pack()
tk.mainloop()

