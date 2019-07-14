import tkinter as tk
from tkinter import font
from functions import getImg, getQuality, getQualityNumber
from create_train_data import getCharacter

class ControlPanel:
    def __init__(self, parent):
        self.__parent = parent
        self.__frame_padx = 10
        self.__frame_pady = 10
        self.__button_width = 75
        self.__button_height = 40
        self.__radiobutton_width = 75
        self.__radiobutton_height = 30
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
    def img1080(self):
        return self.__1080_img

    @property
    def img720(self):
        return self.__720_img

    @property
    def img480(self):
        return self.__480_img

    @property
    def img360(self):
        return self.__360_img

    @property
    def img240(self):
        return self.__240_img

    @property
    def img144(self):
        return self.__144_img

    @img1080.setter
    def img1080(self, img):
        self.__1080_img = img

    @img720.setter
    def img720(self, img):
        self.__720_img = img

    @img480.setter
    def img480(self, img):
        self.__480_img = img

    @img360.setter
    def img360(self, img):
        self.__360_img = img

    @img240.setter
    def img240(self, img):
        self.__240_img = img

    @img144.setter
    def img144(self, img):
        self.__144_img = img

    @property
    def button1080(self):
        return self.__video_quality_radio_button_1080

    @property
    def button720(self):
        return self.__video_quality_radio_button_720

    @property
    def button480(self):
        return self.__video_quality_radio_button_480

    @property
    def button360(self):
        return self.__video_quality_radio_button_360

    @property
    def button240(self):
        return self.__video_quality_radio_button_240

    @property
    def button144(self):
        return self.__video_quality_radio_button_144

    @property
    def img44100(self):
        return self.__44100_img

    @property
    def img32000(self):
        return self.__32000_img

    @property
    def img16000(self):
        return self.__16000_img

    @img44100.setter
    def img44100(self, img):
        self.__44100_img = img

    @img32000.setter
    def img32000(self, img):
        self.__32000_img = img

    @img16000.setter
    def img16000(self, img):
        self.__16000_img = img

    @property
    def button44100(self):
        return self.__audio_quality_radio_button_44100

    @property
    def button32000(self):
        return self.__audio_quality_radio_button_32000

    @property
    def button16000(self):
        return self.__audio_quality_radio_button_16000

    @property
    def imgtrain(self):
        return self.__train_img

    @property
    def imgtest(self):
        return self.__test_img

    @imgtrain.setter
    def imgtrain(self, img):
        self.__train_img = img

    @imgtest.setter
    def imgtest(self, img):
        self.__test_img = img

    @property
    def buttontrain(self):
        return self.__train_radio_button

    @property
    def buttontest(self):
        return self.__test_radio_button

    @property
    def video_quality_frame(self):
        return self.__video_quality_radio_frame

    @property
    def audio_quality_frame(self):
        return self.__audio_quality_radio_frame

    @property
    def train_frame(self):
        return self.__train_radio_frame

    @property
    def radio_width(self):
        return self.__radiobutton_width

    @property
    def radio_height(self):
        return self.__radiobutton_height

    @property
    def audio_quality_value(self):
        return self.__audio_quality_value.get()

    @property
    def video_quality_value(self):
        return str(self.__video_quality_value.get())

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
        self.__pre_video_quality = self.__video_quality_value.get()
        self.__1080_img = getImg(self.__video_quality_radio_frame, "config/fig/1080.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__720_img = getImg(self.__video_quality_radio_frame, "config/fig/720_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__480_img = getImg(self.__video_quality_radio_frame, "config/fig/480.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__360_img = getImg(self.__video_quality_radio_frame, "config/fig/360.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__240_img = getImg(self.__video_quality_radio_frame, "config/fig/240.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__144_img = getImg(self.__video_quality_radio_frame, "config/fig/144.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_1080 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__1080_img, variable = self.__video_quality_value, value = 137, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_1080.pack()
        self.__video_quality_radio_button_1080.bind("<Enter>", self.select1080Hover)
        self.__video_quality_radio_button_1080.bind("<Leave>", self.select1080Unhover)
        self.__video_quality_radio_button_720 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__720_img, variable = self.__video_quality_value, value = 136, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_720.pack()
        self.__video_quality_radio_button_720.bind("<Enter>", self.select720Hover)
        self.__video_quality_radio_button_720.bind("<Leave>", self.select720Unhover)
        self.__video_quality_radio_button_480 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__480_img, variable = self.__video_quality_value, value = 135, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_480.pack()
        self.__video_quality_radio_button_480.bind("<Enter>", self.select480Hover)
        self.__video_quality_radio_button_480.bind("<Leave>", self.select480Unhover)
        self.__video_quality_radio_button_360 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__360_img, variable = self.__video_quality_value, value = 134, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_360.pack()
        self.__video_quality_radio_button_360.bind("<Enter>", self.select360Hover)
        self.__video_quality_radio_button_360.bind("<Leave>", self.select360Unhover)
        self.__video_quality_radio_button_240 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__240_img, variable = self.__video_quality_value, value = 133, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_240.pack()
        self.__video_quality_radio_button_240.bind("<Enter>", self.select240Hover)
        self.__video_quality_radio_button_240.bind("<Leave>", self.select240Unhover)
        self.__video_quality_radio_button_144 = tk.Radiobutton(self.__video_quality_radio_frame, image = self.__144_img, variable = self.__video_quality_value, value = 160, command = self.changeVideoQualityImg)
        self.__video_quality_radio_button_144.pack()
        self.__video_quality_radio_button_144.bind("<Enter>", self.select144Hover)
        self.__video_quality_radio_button_144.bind("<Leave>", self.select144Unhover)

    def setLocalFormParts(self):
        self.__local_frame = tk.LabelFrame(self.__select_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 4, text = "ローカルから動画を選択")
        self.__local_frame.pack(padx = self.__frame_padx, side = "left")
        self.__quality_select_frame = tk.Frame(self.__local_frame)
        self.__quality_select_frame.pack(padx = self.__frame_padx, side = "left")
        #音質のラジオボタンの配置
        self.__audio_quality_radio_frame = tk.LabelFrame(self.__quality_select_frame, padx = self.__frame_padx, pady = self.__frame_pady, bd = 2, text = "サンプルレートを選択")
        self.__audio_quality_radio_frame.pack(pady = self.__frame_pady)
        #ラジオボタンの設定
        self.__audio_quality_value = tk.IntVar()
        self.__audio_quality_value.set(44100)
        self.__pre_audio_quality = self.__audio_quality_value.get()
        self.__44100_img = getImg(self.__audio_quality_radio_frame, "config/fig/44100_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__32000_img = getImg(self.__audio_quality_radio_frame, "config/fig/32000.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__16000_img = getImg(self.__audio_quality_radio_frame, "config/fig/16000.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_44100 = tk.Radiobutton(self.__audio_quality_radio_frame, image = self.__44100_img, variable = self.__audio_quality_value, value = 44100, command = self.changeAudioQualityImg)
        self.__audio_quality_radio_button_44100.pack()
        self.__audio_quality_radio_button_44100.bind("<Enter>", self.select44100Hover)
        self.__audio_quality_radio_button_44100.bind("<Leave>", self.select44100Unhover)
        self.__audio_quality_radio_button_32000 = tk.Radiobutton(self.__audio_quality_radio_frame, image = self.__32000_img, variable = self.__audio_quality_value, value = 32000, command = self.changeAudioQualityImg)
        self.__audio_quality_radio_button_32000.pack()
        self.__audio_quality_radio_button_32000.bind("<Enter>", self.select32000Hover)
        self.__audio_quality_radio_button_32000.bind("<Leave>", self.select32000Unhover)
        self.__audio_quality_radio_button_16000 = tk.Radiobutton(self.__audio_quality_radio_frame, image = self.__16000_img, variable = self.__audio_quality_value, value = 16000, command = self.changeAudioQualityImg)
        self.__audio_quality_radio_button_16000.pack()
        self.__audio_quality_radio_button_16000.bind("<Enter>", self.select16000Hover)
        self.__audio_quality_radio_button_16000.bind("<Leave>", self.select16000Unhover)
        #動画選択のボタン
        self.__select_button = tk.Canvas(
            self.__quality_select_frame, # 親要素をメインウィンドウに設定
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
        self.__pre_train = self.__train_value.get()
        self.__train_img = getImg(self.__train_radio_frame, "config/fig/train.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__test_img = getImg(self.__train_radio_frame, "config/fig/test_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__train_radio_button = tk.Radiobutton(self.__train_radio_frame, image = self.__train_img, variable = self.__train_value, value = 1, command = self.changeTrainTestImg)
        self.__train_radio_button.pack()
        self.__train_radio_button.bind("<Enter>", self.selectTrainHover)
        self.__train_radio_button.bind("<Leave>", self.selectTrainUnhover)
        self.__test_radio_button = tk.Radiobutton(self.__train_radio_frame, image = self.__test_img, variable = self.__train_value, value = 0, command = self.changeTrainTestImg)
        self.__test_radio_button.pack()
        self.__test_radio_button.bind("<Enter>", self.selectTestHover)
        self.__test_radio_button.bind("<Leave>", self.selectTestUnhover)
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

    def changeVideoQualityImg(self):
        pre_quality = "".join(getQuality(str(self.__pre_video_quality))).replace("p", "")
        exec("self.img" + pre_quality + " = getImg(self.video_quality_frame, 'config/fig/" + pre_quality + ".jpg', self.radio_width, self.radio_height)")
        exec("self.button" + pre_quality + ".configure(image = self.img" + pre_quality +")")
        current_quality = "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "")
        exec("self.img" + current_quality + " = getImg(self.video_quality_frame, 'config/fig/" + current_quality + "_select.jpg', self.radio_width, self.radio_height)")
        exec("self.button" + current_quality + ".configure(image = self.img" + current_quality +")")
        self.__pre_video_quality = getQualityNumber(current_quality)

    def changeAudioQualityImg(self):
        pre_quality = str(self.__pre_audio_quality)
        exec("self.img" + pre_quality + " = getImg(self.audio_quality_frame, 'config/fig/" + pre_quality + ".jpg', self.radio_width, self.radio_height)")
        exec("self.button" + pre_quality + ".configure(image = self.img" + pre_quality +")")
        current_quality = str(self.__audio_quality_value.get())
        exec("self.img" + current_quality + " = getImg(self.audio_quality_frame, 'config/fig/" + current_quality + "_select.jpg', self.radio_width, self.radio_height)")
        exec("self.button" + current_quality + ".configure(image = self.img" + current_quality +")")
        self.__pre_audio_quality = int(current_quality)

    def changeTrainTestImg(self):
        pre_status = "train" if self.__pre_train else "test"
        exec("self.img" + pre_status + " = getImg(self.train_frame, 'config/fig/" + pre_status + ".jpg', self.radio_width, self.radio_height)")
        exec("self.button" + pre_status + ".configure(image = self.img" + pre_status +")")
        current_status = "train" if self.__train_value.get() else "test"
        exec("self.img" + current_status + " = getImg(self.train_frame, 'config/fig/" + current_status + "_select.jpg', self.radio_width, self.radio_height)")
        exec("self.button" + current_status + ".configure(image = self.img" + current_status +")")
        self.__pre_train = self.__train_value.get()

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

    def select1080Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "1080":
            self.__1080_img = getImg(self.__video_quality_radio_frame, "config/fig/1080_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__1080_img = getImg(self.__video_quality_radio_frame, "config/fig/1080_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_1080.configure(image = self.__1080_img)

    def select1080Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "1080":
            self.__1080_img = getImg(self.__video_quality_radio_frame, "config/fig/1080_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__1080_img = getImg(self.__video_quality_radio_frame, "config/fig/1080.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_1080.configure(image = self.__1080_img)

    def select720Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "720":
            self.__720_img = getImg(self.__video_quality_radio_frame, "config/fig/720_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__720_img = getImg(self.__video_quality_radio_frame, "config/fig/720_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_720.configure(image = self.__720_img)

    def select720Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "720":
            self.__720_img = getImg(self.__video_quality_radio_frame, "config/fig/720_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__720_img = getImg(self.__video_quality_radio_frame, "config/fig/720.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_720.configure(image = self.__720_img)

    def select480Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "480":
            self.__480_img = getImg(self.__video_quality_radio_frame, "config/fig/480_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__480_img = getImg(self.__video_quality_radio_frame, "config/fig/480_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_480.configure(image = self.__480_img)

    def select480Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "480":
            self.__480_img = getImg(self.__video_quality_radio_frame, "config/fig/480_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__480_img = getImg(self.__video_quality_radio_frame, "config/fig/480.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_480.configure(image = self.__480_img)

    def select360Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "360":
            self.__360_img = getImg(self.__video_quality_radio_frame, "config/fig/360_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__360_img = getImg(self.__video_quality_radio_frame, "config/fig/360_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_360.configure(image = self.__360_img)

    def select360Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "360":
            self.__360_img = getImg(self.__video_quality_radio_frame, "config/fig/360_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__360_img = getImg(self.__video_quality_radio_frame, "config/fig/360.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_360.configure(image = self.__360_img)

    def select240Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "240":
            self.__240_img = getImg(self.__video_quality_radio_frame, "config/fig/240_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__240_img = getImg(self.__video_quality_radio_frame, "config/fig/240_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_240.configure(image = self.__240_img)

    def select240Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "240":
            self.__240_img = getImg(self.__video_quality_radio_frame, "config/fig/240_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__240_img = getImg(self.__video_quality_radio_frame, "config/fig/240.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_240.configure(image = self.__240_img)

    def select144Hover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "144":
            self.__144_img = getImg(self.__video_quality_radio_frame, "config/fig/144_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__144_img = getImg(self.__video_quality_radio_frame, "config/fig/144_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_144.configure(image = self.__144_img)

    def select144Unhover(self, event):
        if  "".join(getQuality(str(self.__video_quality_value.get()))).replace("p", "") == "144":
            self.__144_img = getImg(self.__video_quality_radio_frame, "config/fig/144_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__144_img = getImg(self.__video_quality_radio_frame, "config/fig/144.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__video_quality_radio_button_144.configure(image = self.__144_img)

    def select44100Hover(self, event):
        if  self.__audio_quality_value.get() == 44100:
            self.__44100_img = getImg(self.__audio_quality_radio_frame, "config/fig/44100_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__44100_img = getImg(self.__audio_quality_radio_frame, "config/fig/44100_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_44100.configure(image = self.__44100_img)

    def select44100Unhover(self, event):
        if  self.__audio_quality_value.get() == 44100:
            self.__44100_img = getImg(self.__audio_quality_radio_frame, "config/fig/44100_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__44100_img = getImg(self.__audio_quality_radio_frame, "config/fig/44100.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_44100.configure(image = self.__44100_img)

    def select32000Hover(self, event):
        if  self.__audio_quality_value.get() == 32000:
            self.__32000_img = getImg(self.__audio_quality_radio_frame, "config/fig/32000_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__32000_img = getImg(self.__audio_quality_radio_frame, "config/fig/32000_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_32000.configure(image = self.__32000_img)

    def select32000Unhover(self, event):
        if  self.__audio_quality_value.get() == 32000:
            self.__32000_img = getImg(self.__audio_quality_radio_frame, "config/fig/32000_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__32000_img = getImg(self.__audio_quality_radio_frame, "config/fig/32000.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_32000.configure(image = self.__32000_img)

    def select16000Hover(self, event):
        if  self.__audio_quality_value.get() == 16000:
            self.__16000_img = getImg(self.__audio_quality_radio_frame, "config/fig/16000_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__16000_img = getImg(self.__audio_quality_radio_frame, "config/fig/16000_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_16000.configure(image = self.__16000_img)

    def select16000Unhover(self, event):
        if  self.__audio_quality_value.get() == 16000:
            self.__16000_img = getImg(self.__audio_quality_radio_frame, "config/fig/16000_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__16000_img = getImg(self.__audio_quality_radio_frame, "config/fig/16000.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__audio_quality_radio_button_16000.configure(image = self.__16000_img)

    def selectTrainHover(self, event):
        if  self.__train_value.get() == 1:
            self.__train_img = getImg(self.__train_radio_frame, "config/fig/train_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__train_img = getImg(self.__train_radio_frame, "config/fig/train_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__train_radio_button.configure(image = self.__train_img)

    def selectTrainUnhover(self, event):
        if  self.__train_value.get() == 1:
            self.__train_img = getImg(self.__train_radio_frame, "config/fig/train_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__train_img = getImg(self.__train_radio_frame, "config/fig/train.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__train_radio_button.configure(image = self.__train_img)

    def selectTestHover(self, event):
        if  self.__train_value.get() == 0:
            self.__test_img = getImg(self.__train_radio_frame, "config/fig/test_select_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__test_img = getImg(self.__train_radio_frame, "config/fig/test_hover.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__test_radio_button.configure(image = self.__test_img)

    def selectTestUnhover(self, event):
        if  self.__train_value.get() == 0:
            self.__test_img = getImg(self.__train_radio_frame, "config/fig/test_select.jpg", self.__radiobutton_width, self.__radiobutton_height)
        else:
            self.__test_img = getImg(self.__train_radio_frame, "config/fig/test.jpg", self.__radiobutton_width, self.__radiobutton_height)
        self.__test_radio_button.configure(image = self.__test_img)
