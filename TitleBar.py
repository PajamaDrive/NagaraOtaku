import tkinter as tk
from tkinter import font
from functions import getImg

class TitleBar:
    def __init__(self, parent):
        self.__window_button_width = 15
        self.__window_button_height = 15
        self.__window_button_pad = 5
        self.__parent = parent
        self.__title_bar = tk.Frame(self.__parent, bg = "#E0E0E0", cursor = "fleur")
        self.__title_bar.pack(fill = "x")
        #ウィンドウを閉じるボタン
        self.__delete_button = tk.Canvas(
            self.__title_bar, # 親要素をメインウィンドウに設定
            bg = "#E0E0E0",
            highlightthickness = 0,
            width = self.__window_button_width,  # 幅を設定
            height = self.__window_button_height # 高さを設定
        )
        self.__delete_button.pack(side = "left", padx = self.__window_button_pad, pady = self.__window_button_pad)
        self.__delete_tkimg = getImg(self.__delete_button, "config/fig/delete_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__delete_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__delete_tkimg,
            tags = "delete"
        )
        self.__delete_button.bind("<Enter>", self.deleteHover)
        self.__delete_button.bind("<Leave>", self.deleteUnhover)
        #最小化ボタン
        self.__minimize_button = tk.Canvas(
            self.__title_bar, # 親要素をメインウィンドウに設定
            bg = "#E0E0E0",
            highlightthickness = 0,
            width = self.__window_button_width,  # 幅を設定
            height = self.__window_button_height # 高さを設定
        )
        self.__minimize_button.pack(side = "left", padx = self.__window_button_pad, pady = self.__window_button_pad)
        self.__minimize_tkimg = getImg(self.__minimize_button, "config/fig/minimize_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__minimize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__minimize_tkimg,
            tags = "minimize"
        )
        self.__minimize_button.bind("<Enter>", self.minimizeHover)
        self.__minimize_button.bind("<Leave>", self.minimizeUnhover)
        #最大化ボタン
        self.__maximize_button = tk.Canvas(
            self.__title_bar, # 親要素をメインウィンドウに設定
            bg = "#E0E0E0",
            highlightthickness = 0,
            width = self.__window_button_width,  # 幅を設定
            height = self.__window_button_height # 高さを設定
        )
        self.__maximize_button.pack(side = "left", padx = self.__window_button_pad, pady = self.__window_button_pad)
        self.__maximize_tkimg = getImg(self.__maximize_button, "config/fig/maximize_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__maximize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__maximize_tkimg,
            tags = "maximize"
        )
        self.__maximize_button.bind("<Enter>", self.maximizeHover)
        self.__maximize_button.bind("<Leave>", self.maximizeUnhover)
        #タイトルのテキスト
        self.__title_frame = tk.Frame(self.__title_bar, bg = "#E0E0E0")
        self.__title_frame.pack()
        self.__title_text = tk.StringVar()
        self.__title_text.set("NagaraOtaku")
        self.__title_font = font.Font(self.__title_frame, family = 'Helvetica', size = 15, weight = 'bold')
        self.__title_label = tk.Label(
            self.__title_frame,
            bg = "#E0E0E0",
            textvariable = self.__title_text,
            font = self.__title_font
        )
        self.__title_label.pack()

    @property
    def bar(self):
        return self.__title_bar

    @property
    def delete(self):
        return self.__delete_button

    @property
    def minimize(self):
        return self.__minimize_button

    @property
    def maximize(self):
        return self.__maximize_button

    def deleteHover(self, event):
        self.__delete_tkimg = getImg(self.__delete_button, "config/fig/delete.jpg", self.__window_button_width, self.__window_button_height)
        self.__delete_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__delete_tkimg,
            tags = "delete"
        )

    def deleteUnhover(self, event):
        self.__delete_tkimg = getImg(self.__delete_button, "config/fig/delete_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__delete_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__delete_tkimg,
            tags = "delete"
        )

    def minimizeHover(self, event):
        self.__minimize_tkimg = getImg(self.__minimize_button, "config/fig/minimize.jpg", self.__window_button_width, self.__window_button_height)
        self.__minimize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__minimize_tkimg,
            tags = "minimize"
        )

    def minimizeUnhover(self, event):
        self.__minimize_tkimg = getImg(self.__minimize_button, "config/fig/minimize_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__minimize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__minimize_tkimg,
            tags = "minimize"
        )

    def maximizeHover(self, event):
        self.__maximize_tkimg = getImg(self.__maximize_button, "config/fig/maximize.jpg", self.__window_button_width, self.__window_button_height)
        self.__maximize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__maximize_tkimg,
            tags = "maximize"
        )

    def maximizeUnhover(self, event):
        self.__maximize_tkimg = getImg(self.__maximize_button, "config/fig/maximize_plain.jpg", self.__window_button_width, self.__window_button_height)
        self.__maximize_button.create_image(
            int(self.__window_button_width / 2),
            int(self.__window_button_height / 2),
            image = self.__maximize_tkimg,
            tags = "maximize"
        )
