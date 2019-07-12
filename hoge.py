from tkinter import *

# メインウィンドウの設定
root = Tk()
root.minsize(100, 100)
root.maxsize(400, 400)

# キャンバスの設定
c0 = Canvas(root, bg = 'darkgreen', width = 200, height = 200)
id = c0.create_rectangle(20, 20, 180, 180, fill = 'red')
c0.pack(fill = BOTH, expand = True)

# 図形の大きさを変更
def change_size(event):
    print(c0.winfo_width())
    print(c0.winfo_height())
    w = c0.winfo_width()
    h = c0.winfo_height()
    c0.coords(id, 20, 20, w - 20, h - 20)

# バインディングの設定
root.bind('<Configure>', change_size)

root.mainloop()
