import tkinter as tk
from tkinter import font
from functions import getImg

class StatusFrame:
    def __init__(self, parent):
        self.__parent = parent
        self.__status_width = 135
        self.__status_height = 40
        self.__status_padx = 10
        self.__frame_pady = 20
        self.__is_creating = False
        self.__is_downloading = False
        self.__is_training = False
        self.__is_loading = False
        self.__is_creating_data = False
        self.__status_list = {1 : "Download", 2 : "MP3", 4 : "Train", 8 : "Load", 16 : "CreateData"}
        #ステータス表示
        self.__status_frame = tk.Frame(self.__parent)
        self.__status_frame.pack(pady = self.__frame_pady)
        self.__status_text = tk.StringVar()
        self.__status_text.set("現在の状態")
        self.__status_font = font.Font(self.__status_frame, family = 'Helvetica', size = 15, weight = 'bold')
        self.__status_label = tk.Label(
            self.__status_frame,
            textvariable = self.__status_text,
            font = self.__status_font
        )
        self.__status_label.pack()
        #待機
        self.__wait_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__wait_img.pack(padx = self.__status_padx, side = "left")
        self.__wait_tkimg = getImg(self.__wait_img, "config/fig/waiting.jpg", self.__status_width, self.__status_height)
        self.__wait_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__wait_tkimg
        )
        #mp3 creating
        self.__mp3_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__mp3_img.pack(padx = self.__status_padx, side = "left")
        self.__mp3_tkimg = getImg(self.__mp3_img, "config/fig/not_creating_mp3.jpg", self.__status_width, self.__status_height)
        self.__mp3_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__mp3_tkimg
        )
        #download
        self.__download_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__download_img.pack(padx = self.__status_padx, side = "left")
        self.__download_tkimg = getImg(self.__download_img, "config/fig/not_downloading.jpg", self.__status_width, self.__status_height)
        self.__download_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__download_tkimg
        )
        #create train data
        self.__create_data_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__create_data_img.pack(padx = self.__status_padx, side = "left")
        self.__create_data_tkimg = getImg(self.__create_data_img, "config/fig/not_creating_train.jpg", self.__status_width, self.__status_height)
        self.__create_data_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__create_data_tkimg
        )
        #train
        self.__train_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__train_img.pack(padx = self.__status_padx, side = "left")
        self.__train_tkimg = getImg(self.__train_img, "config/fig/not_training.jpg", self.__status_width, self.__status_height)
        self.__train_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__train_tkimg
        )
        #load
        self.__load_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__load_img.pack(padx = self.__status_padx, side = "left")
        self.__load_tkimg = getImg(self.__load_img, "config/fig/not_loading.jpg", self.__status_width, self.__status_height)
        self.__load_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__load_tkimg
        )

    def changeStatus(self, status):
        if status == self.__status_list[1]:
            self.__is_downloading = not self.__is_downloading
            if self.__is_downloading:
                self.__download_tkimg = getImg(self.__download_img, "config/fig/downloading.jpg", self.__status_width, self.__status_height)
            else:
                self.__download_tkimg = getImg(self.__download_img, "config/fig/not_downloading.jpg", self.__status_width, self.__status_height)
            self.__download_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__download_tkimg
            )
        if status == self.__status_list[2]:
            self.__is_creating = not self.__is_creating
            if self.__is_creating:
                self.__mp3_tkimg = getImg(self.__mp3_img, "config/fig/creating_mp3.jpg", self.__status_width, self.__status_height)
            else:
                self.__mp3_tkimg = getImg(self.__mp3_img, "config/fig/not_creating_mp3.jpg", self.__status_width, self.__status_height)
            self.__mp3_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__mp3_tkimg
            )
        if status == self.__status_list[4]:
            self.__is_training = not self.__is_training
            if self.__is_training:
                self.__train_tkimg = getImg(self.__train_img, "config/fig/training.jpg", self.__status_width, self.__status_height)
            else:
                self.__train_tkimg = getImg(self.__train_img, "config/fig/not_training.jpg", self.__status_width, self.__status_height)
            self.__train_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__train_tkimg
            )
        if status == self.__status_list[8]:
            self.__is_loading = not self.__is_loading
            if self.__is_loading:
                self.__load_tkimg = getImg(self.__load_img, "config/fig/loading.jpg", self.__status_width, self.__status_height)
            else:
                self.__load_tkimg = getImg(self.__load_img, "config/fig/not_loading.jpg", self.__status_width, self.__status_height)
            self.__load_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__load_tkimg
            )
        if status == self.__status_list[16]:
            self.__is_creating_data = not self.__is_creating_data
            if self.__is_creating_data:
                self.__create_data_tkimg = getImg(self.__create_data_img, "config/fig/creating_train.jpg", self.__status_width, self.__status_height)
            else:
                self.__create_data_tkimg = getImg(self.__create_data_img, "config/fig/not_creating_train.jpg", self.__status_width, self.__status_height)
            self.__create_data_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__create_data_tkimg
            )
        if self.__is_creating or self.__is_training or self.__is_downloading or self.__is_loading or self.__is_creating_data:
            self.__wait_tkimg = getImg(self.__wait_img, "config/fig/not_waiting.jpg", self.__status_width, self.__status_height)
        else:
            self.__wait_tkimg = getImg(self.__wait_img, "config/fig/waiting.jpg", self.__status_width, self.__status_height)
        self.__wait_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__wait_tkimg
        )

    def getStatus(self):
        status = 0
        if self.__is_downloading:
            status += 1
        if self.__is_creating:
            status += 2
        if self.__is_training:
            status += 4
        if self.__is_loading:
            status += 8
        if self.__is_creating_data:
            status += 16
        return [self.__status_list[2 ** i] for i in range(5) if status & (2 ** i)]

    def getDeniedStatus(self):
        return [self.__status_list[2]]
