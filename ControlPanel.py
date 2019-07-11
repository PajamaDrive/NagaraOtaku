import tkinter as tk
from tkinter import font
from functions import getImg
from create_train_data import getCharacter

class ControlPanel:
    def __init__(self, parent):
        self.__parent = parent
        self.__frame_padx = 10
        self.__frame_pady = 10
        self.__button_width = 75
        self.__button_height = 40
        self.__train_test_width = 75
        self.__train_test_height = 40
        self.__initialize_width = 140
        self.__initialize_height = 40
        self.setFormParts()

    @property
    def download_button(self):
        return self.__form_button

    @property
    def select_button(self):
        return self.__select_button

    @property
    def onoff_button(self):
        return self.__train_test_button

    @property
    def initialize_button(self):
        return self.__initialize_button

    @property
    def form(self):
        return self.__form

    @property
    def character_name(self):
        return self.__character_name

    @character_name.setter
    def character_name(self, character_name):
        self.__character_name = character_name

    @property
    def character_list(self):
        return self.__character_list

    @property
    def video_quality_value(self):
        return str(self.__video_quality_value.get())

    @property
    def audio_quality_value(self):
        return self.__audio_quality_value.get()

    @property
    def is_train(self):
        return self.__train_value.get()

    @property
    def interval(self):
        return int(self.__interval_form.get())

    def setFormParts(self):
        #動画選択フォームの配置
        self.__select_frame = tk.Frame(self.__parent)
        self.__select_frame.pack(padx = self.__frame_padx, pady = self.__frame_pady)
        #リモートな動画選択フォーム
        self.setRemoteFormParts()
        #ローカルな動画選択フォーム
        self.setLocalFormParts()

    def setRemoteFormParts(self):
        self.__remote_frame = tk.LabelFrame(self.__select_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 4, text = "ネットから動画を選択")
        self.__remote_frame.pack(padx = self.__frame_padx, side = "left")
        #動画URLフォームの配置
        self.__form_frame = tk.LabelFrame(self.__remote_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "動画のURLを入力")
        self.__form_frame.pack(side = "left")
        #フォーム
        self.__form = tk.Entry(self.__form_frame, width = 30)
        self.__form.pack(side = "left")
        #動画ダウンロードのボタン
        self.__form_button = tk.Canvas(
            self.__form_frame, # 親要素をメインウィンドウに設定
            bg = "#ffffff",
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__form_button.pack(padx = self.__frame_padx, side = "left")
        self.__form_tkimg = getImg(self.__form_button, "config/fig/download.jpg", self.__button_width, self.__button_height)
        self.__form_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__form_tkimg,
            tags = "download"
        )
        self.__form_button.bind("<Enter>", self.formHover)
        self.__form_button.bind("<Leave>", self.formUnhover)
        #画質のラジオボタンの配置
        self.__video_quality_radio_frame = tk.LabelFrame(self.__remote_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "画質を選択")
        self.__video_quality_radio_frame.pack(padx = self.__frame_padx, side = "left")
        #ラジオボタンの設定
        self.__video_quality_value = tk.IntVar()
        self.__video_quality_value.set(136)
        self.__video_quality_radio_button_1080 = tk.Radiobutton(self.__video_quality_radio_frame, text = "1080p", variable = self.__video_quality_value, value = 137)
        self.__video_quality_radio_button_1080.pack()
        self.__video_quality_radio_button_720 = tk.Radiobutton(self.__video_quality_radio_frame, text = "720p", variable = self.__video_quality_value, value = 136)
        self.__video_quality_radio_button_720.pack()
        self.__video_quality_radio_button_480 = tk.Radiobutton(self.__video_quality_radio_frame, text = "480p", variable = self.__video_quality_value, value = 135)
        self.__video_quality_radio_button_480.pack()
        self.__video_quality_radio_button_360 = tk.Radiobutton(self.__video_quality_radio_frame, text = "360p", variable = self.__video_quality_value, value = 134)
        self.__video_quality_radio_button_360.pack()
        self.__video_quality_radio_button_240 = tk.Radiobutton(self.__video_quality_radio_frame, text = "240p", variable = self.__video_quality_value, value = 133)
        self.__video_quality_radio_button_240.pack()
        self.__video_quality_radio_button_144 = tk.Radiobutton(self.__video_quality_radio_frame, text = "144p", variable = self.__video_quality_value, value = 160)
        self.__video_quality_radio_button_144.pack()

    def setLocalFormParts(self):
        self.__local_frame = tk.LabelFrame(self.__select_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 4, text = "ローカルから動画を選択")
        self.__local_frame.pack(padx = self.__frame_padx, side = "left")
        self.__quality_select_frame = tk.Frame(self.__local_frame)
        self.__quality_select_frame.pack(padx = self.__frame_padx, side = "left")
        #音質のラジオボタンの配置
        self.__audio_quality_radio_frame = tk.LabelFrame(self.__quality_select_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "サンプリングレートを選択")
        self.__audio_quality_radio_frame.pack(pady = self.__frame_pady)
        #ラジオボタンの設定
        self.__audio_quality_value = tk.IntVar()
        self.__audio_quality_value.set(44100)
        self.__audio_quality_radio_button_44100 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "44100Hz", variable = self.__audio_quality_value, value = 44100)
        self.__audio_quality_radio_button_44100.pack()
        self.__audio_quality_radio_button_32000 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "32000Hz", variable = self.__audio_quality_value, value = 32000)
        self.__audio_quality_radio_button_32000.pack()
        self.__audio_quality_radio_button_16000 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "16000Hz", variable = self.__audio_quality_value, value = 16000)
        self.__audio_quality_radio_button_16000.pack()
        #動画選択のボタン
        self.__select_button = tk.Canvas(
            self.__quality_select_frame, # 親要素をメインウィンドウに設定
            bg = "#ffffff",
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__select_button.pack()
        self.__select_tkimg = getImg(self.__select_button, "config/fig/select.jpg", self.__button_width, self.__button_height)
        self.__select_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__select_tkimg,
            tags = "select"
        )
        self.__select_button.bind("<Enter>", self.selectHover)
        self.__select_button.bind("<Leave>", self.selectUnhover)
        #訓練と本番の選択フォーム
        self.setTrainTestFormParts()

    def setTrainTestFormParts(self):
        #訓練・本番のラジオボタンの配置
        self.__train_frame = tk.Frame(self.__local_frame)
        self.__train_frame.pack(padx = self.__frame_padx, side = "left")
        self.__train_radio_frame = tk.LabelFrame(self.__train_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "訓練/本番を選択")
        self.__train_radio_frame.pack()
        self.__train_value = tk.IntVar()
        self.__train_value.set(0)
        self.__train_radio_button = tk.Radiobutton(self.__train_radio_frame, text = "訓練", variable = self.__train_value, value = 1)
        self.__train_radio_button.pack()
        self.__test_radio_button = tk.Radiobutton(self.__train_radio_frame, text = "本番", variable = self.__train_value, value = 0)
        self.__test_radio_button.pack()
        #通知の間隔
        self.__interval_frame = tk.Frame(self.__train_frame)
        self.__interval_frame.pack(pady = self.__frame_pady)
        self.__interval_text = tk.StringVar()
        self.__interval_text.set("認識の頻度")
        self.__interval_text_font = font.Font(self.__interval_frame, family = 'Helvetica', size = 15, weight = "bold")
        self.__interval_text_label = tk.Label(
            self.__interval_frame,
            textvariable = self.__interval_text,
            font = self.__interval_text_font
        )
        self.__interval_text_label.pack()
        self.__interval_form = tk.Entry(self.__interval_frame, width = 3)
        self.__interval_form.insert(tk.END, "5")
        self.__interval_form.pack(side = "left")
        self.__interval_second_text = tk.StringVar()
        self.__interval_second_text.set("秒")
        self.__interval_second_font = font.Font(self.__interval_frame, family = 'Helvetica', size = 12)
        self.__interval_second_label = tk.Label(
            self.__interval_frame,
            textvariable = self.__interval_second_text,
            font = self.__interval_second_font
        )
        self.__interval_second_label.pack(side = "left")

        #訓練ON/OFFの設定
        self.__train_test_frame = tk.Frame(self.__train_frame)
        self.__train_test_frame.pack()
        self.__train_test_text = tk.StringVar()
        self.__train_test_text.set("訓練/本番の状態")
        self.__train_test_font = font.Font(self.__train_test_frame, family = 'Helvetica', size = 15, weight = 'bold')
        self.__train_test_label = tk.Label(
            self.__train_test_frame,
            textvariable = self.__train_test_text,
            font = self.__train_test_font
        )
        self.__train_test_label.pack()
        #通知画像
        self.__train_test_button = tk.Canvas(
            self.__train_test_frame, # 親要素をメインウィンドウに設定
            bg = "#ffffff",
            highlightthickness = 0,
            width = self.__train_test_width,  # 幅を設定
            height = self.__train_test_height # 高さを設定
        )
        self.__train_test_button.pack()
        self.__train_test_tkimg = getImg(self.__train_test_button, "config/fig/on.jpg", self.__train_test_width, self.__train_test_height)
        self.__train_test_button.create_image(
            int(self.__train_test_width / 2),
            int(self.__train_test_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )
        self.__train_test_button.bind("<Enter>", self.onHover)
        self.__train_test_button.bind("<Leave>", self.onUnhover)
        #キャラクター名の選択
        self.__classfier_frame = tk.Frame(self.__local_frame)
        self.__classfier_frame.pack(padx = self.__frame_padx, side = "left")
        self.__character_frame = tk.LabelFrame(self.__classfier_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "キャラクター名を選択")
        self.__character_frame.pack()
        self.__character_frame.grid_rowconfigure(0, weight = 1)
        self.__character_frame.grid_columnconfigure(0, weight = 1)
        self.__characters = tk.StringVar()
        self.updateCharacterList()
        self.__character_list = tk.Listbox(self.__character_frame, listvariable = self.__characters, height = 5)
        self.__character_name = ""
        self.__character_list.bind("<<ListboxSelect>>", self.setCharacterName)
        self.__character_list.grid(row = 0, column = 0)
        #スクロールバーの設定
        self.__character_scrollbar_y = tk.Scrollbar(self.__character_frame, orient = "vertical", command = self.__character_list.yview)
        self.__character_scrollbar_y.grid(row = 0, column = 1, sticky = "ns")
        #スクロールバーの表示をボックスに合わせる
        self.__character_list.config(yscrollcommand = self.__character_scrollbar_y.set)
        #初期化ボタンの設定
        self.__initialize_button = tk.Canvas(
            self.__classfier_frame, # 親要素をメインウィンドウに設定
            bg = "#ffffff",
            highlightthickness = 0,
            width = self.__initialize_width,  # 幅を設定
            height = self.__initialize_height # 高さを設定
        )
        self.__initialize_button.pack(pady = self.__frame_pady)
        self.__initialize_tkimg = getImg(self.__initialize_button, "config/fig/initialize.jpg", self.__initialize_width, self.__initialize_height)
        self.__initialize_button.create_image(
            int(self.__initialize_width / 2),
            int(self.__initialize_height / 2),
            image = self.__initialize_tkimg,
            tags = "initialize"
        )
        self.__initialize_button.bind("<Enter>", self.initializeHover)
        self.__initialize_button.bind("<Leave>", self.initializeUnhover)

    def setCharacterName(self, event):
        index = self.__character_list.curselection()[0]
        if index == 0:
            self.__character_name = ""
        else:
            self.__character_name = self.__character_string[index]

    def changeButtonImg(self, img_path):
        self.__train_test_tkimg = getImg(self.__train_test_button, img_path, self.__train_test_width, self.__train_test_height)
        self.__train_test_button.create_image(
            int(self.__train_test_width / 2),
            int(self.__train_test_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )
        if "on.jpg" in img_path:
            self.__train_test_button.bind("<Enter>", self.onHover)
            self.__train_test_button.bind("<Leave>", self.onUnhover)
        else:
            self.__train_test_button.bind("<Enter>", self.offHover)
            self.__train_test_button.bind("<Leave>", self.offUnhover)

    def updateCharacterList(self):
        self.__character_string = ["新規に追加"] + getCharacter()
        self.__characters.set(self.__character_string)

    def formHover(self, event):
        self.__form_tkimg = getImg(self.__form_button, "config/fig/download_hover.jpg", self.__button_width, self.__button_height)
        self.__form_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__form_tkimg,
            tags = "download"
        )

    def formUnhover(self, event):
        self.__form_tkimg = getImg(self.__form_button, "config/fig/download.jpg", self.__button_width, self.__button_height)
        self.__form_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__form_tkimg,
            tags = "download"
        )

    def selectHover(self, event):
        self.__select_tkimg = getImg(self.__select_button, "config/fig/select_hover.jpg", self.__button_width, self.__button_height)
        self.__select_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__select_tkimg,
            tags = "select"
        )

    def selectUnhover(self, event):
        self.__select_tkimg = getImg(self.__select_button, "config/fig/select.jpg", self.__button_width, self.__button_height)
        self.__select_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__select_tkimg,
            tags = "select"
        )

    def onHover(self, event):
        self.__train_test_tkimg = getImg(self.__train_test_button, "config/fig/on_hover.jpg", self.__button_width, self.__button_height)
        self.__train_test_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )

    def onUnhover(self, event):
        self.__train_test_tkimg = getImg(self.__train_test_button, "config/fig/on.jpg", self.__button_width, self.__button_height)
        self.__train_test_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )

    def offHover(self, event):
        self.__train_test_tkimg = getImg(self.__train_test_button, "config/fig/off_hover.jpg", self.__button_width, self.__button_height)
        self.__train_test_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )

    def offUnhover(self, event):
        self.__train_test_tkimg = getImg(self.__train_test_button, "config/fig/off.jpg", self.__button_width, self.__button_height)
        self.__train_test_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )

    def initializeHover(self, event):
        self.__initialize_tkimg = getImg(self.__initialize_button, "config/fig/initialize_hover.jpg", self.__initialize_width, self.__initialize_height)
        self.__initialize_button.create_image(
            int(self.__initialize_width / 2),
            int(self.__initialize_height / 2),
            image = self.__initialize_tkimg,
            tags = "initialize"
        )

    def initializeUnhover(self, event):
        self.__initialize_tkimg = getImg(self.__initialize_button, "config/fig/initialize.jpg", self.__initialize_width, self.__initialize_height)
        self.__initialize_button.create_image(
            int(self.__initialize_width / 2),
            int(self.__initialize_height / 2),
            image = self.__initialize_tkimg,
            tags = "initialize"
        )
