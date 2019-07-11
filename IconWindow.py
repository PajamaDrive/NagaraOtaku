import tkinter as tk
from functions import getImg

class IconWindow:
    @property
    def window(self):
        return self.__window

    def __init__(self):
        self.__window_width = 100
        self.__window_height = 50
        self.__window = tk.Tk()
        self.__window.title("NagaraOtaku")
        self.__window.geometry(str(self.__window_width) + "x" + str(self.__window_height))
        #アイコン用の画像
        self.__window_icon_img = tk.Canvas(
            self.__window, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__window_width,  # 幅を設定
            height = self.__window_height # 高さを設定
        )
        self.__window_icon_img.pack()
        self.__window_icon_tkimg = getImg(self.__window, "config/fig/logo.ico", self.__window_width, self.__window_height)
        self.__window_icon_img.create_image(
            int(self.__window_width / 2),
            int(self.__window_height / 2),
            image = self.__window_icon_tkimg
        )

if __name__ == "__main__":
    a = IconWindow()
    a.window.mainloop()
