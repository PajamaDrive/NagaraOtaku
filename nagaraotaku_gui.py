import tkinter as tk
import tkinter.font as font
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as sd
import time
import CV
import pathlib
import os
import platform
from PIL import Image, ImageTk
import VideoController as vc
import threading
import shutil
import zipfile
from create_train_data import getCharacter
import subprocess

class GUI:
    def __init__(self):
        self.__window_width = 1200
        self.__window_height = 600
        self.__scroll_canvas_width = self.__window_width - 50
        self.__button_width = 75
        self.__button_height = 40
        self.__scroll_width = 5
        self.__button_padx = 20
        self.__status_width = 135
        self.__status_height = 40
        self.__status_padx = 10
        self.__train_test_width = 75
        self.__train_test_height = 40
        self.__initialize_width = 140
        self.__initialize_height = 40
        self.__user_process_time = 0
        self.__cycle = 5
        self.__first_time_flag = True
        self.__is_on = True
        self.__is_creating = False
        self.__is_downloading = False
        self.__is_training = False
        self.__is_loading = False
        self.__is_creating_data = False
        self.__train_process = None
        self.__create_train_process = None
        self.__load_thread = None
        self.__detect_thread = None
        self.__button_available = True
        self.__detect_num = 0
        self.__vc = vc.VideoController()
        self.__root = tk.Tk()
        #Tkinterの初期設定
        self.__root.title("NagaraOtaku")
        self.__root.geometry(str(self.__window_width) + "x" + str(self.__window_height))
        self.__root.resizable(width = 1, height = 1)
        self.__root_frame = tk.Frame(self.__root)
        self.__root_frame.pack(fill = "both")
        self.__root_frame.grid_rowconfigure(0, weight = 1)
        self.__root_frame.grid_columnconfigure(0, weight = 1)
        #全体をキャンバスで覆う
        self.__scroll_canvas = tk.Canvas(self.__root_frame, width = self.__scroll_canvas_width, height = self.__window_height)
        self.__scroll_canvas.grid(column = 0, row = 0, sticky = "nwse")
        #スクロールバーの設置
        self.__scrollbar_x = tk.Scrollbar(self.__root_frame, orient = "horizontal", command = self.__scroll_canvas.xview)
        self.__scrollbar_x.grid(column = 0, row = 1, sticky = "we")
        self.__scrollbar_y = tk.Scrollbar(self.__root_frame, orient = "vertical", command = self.__scroll_canvas.yview)
        self.__scrollbar_y.grid(column = 1, row = 0, sticky = "ns")
        self.__scroll_canvas.config(xscrollcommand = self.__scrollbar_x.set)
        self.__scroll_canvas.config(yscrollcommand = self.__scrollbar_y.set)
        self.__scroll_frame = tk.Frame(self.__scroll_canvas)
        self.__scroll_canvas.create_window((0, 0), window = self.__scroll_frame)
        self.__scroll_frame.bind("<Configure>", self.scrollCanvas)

        self.setFormParts()
        self.setStatusParts()

    @property
    def root(self):
        return self.__root

    @property
    def video_title_text(self):
        return self.__video_title_text

    @property
    def video_time_text(self):
        return self.__video_time_text

    @property
    def canvas(self):
        return self.__canvas

    @property
    def vc(self):
        return self.__vc

    def setFormParts(self):
        #動画選択フォームの配置
        self.__select_frame = tk.Frame(self.__scroll_frame)
        self.__select_frame.pack(pady = 10)
        #リモートな動画選択フォーム
        self.setRemoteFormParts()
        #ローカルな動画選択フォーム
        self.setLocalFormParts()

    def setCanvasParts(self):
        self.__first_time_flag = False
        #動画関連の配置
        self.__canvas_frame = tk.Frame(self.__scroll_frame)
        self.__canvas_frame.pack()
        #キャンバス(動画描画部分)の設定
        self.__canvas = tk.Canvas(
            self.__canvas_frame, # 親要素をメインウィンドウに設定
            width = self.__vc.cv.disp_img_width,  # 幅を設定
            height = self.__vc.cv.disp_img_height # 高さを設定
        )
        self.__canvas.pack()
        #シークバーの配置
        self.__video_current_pos = tk.DoubleVar()
        #self.__video_current_pos.trace("w", self.seekPos)
        self.__video_seek_bar = tk.Scale(self.__canvas_frame, variable = self.__video_current_pos, orient = "horizontal", length = self.__vc.cv.disp_img_width, from_ = 0, to = self.__vc.cv.whole_time.getWholeSecond(), showvalue = 0)
        self.__video_seek_bar.pack()
        self.__video_seek_bar.bind("<B1-Motion>", self.seekPos)
        #self.__video_seek_bar.bind("<ButtonRelease-1>", self.videoStopOrStart)
        #テキスト等の配置
        self.setVideoTextParts()

    def setRemoteFormParts(self):
        self.__remote_frame = tk.LabelFrame(self.__select_frame, padx = 15, pady = 15, bd = 4, text = "ネットから動画を選択")
        self.__remote_frame.pack(padx = self.__button_padx, side = "left")
        #動画URLフォームの配置
        self.__form_frame = tk.LabelFrame(self.__remote_frame, padx = 15, pady = 15, bd = 2, text = "動画のURLを入力")
        self.__form_frame.pack(side = "left")
        #フォーム
        self.__form = tk.Entry(self.__form_frame, width = 30)
        self.__form.pack(side = "left")
        #動画ダウンロードのボタン
        self.__form_button = tk.Canvas(
            self.__form_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__form_button.pack(padx = self.__button_padx, side = "left")
        self.__form_tkimg = self.getImg("config/fig/download.jpg", self.__button_width, self.__button_height)
        self.__form_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__form_tkimg,
            tags = "download"
        )
        self.__form_button.tag_bind("download", "<ButtonPress-1>", self.setVideoURL)
        #画質のラジオボタンの配置
        self.__video_quality_radio_frame = tk.LabelFrame(self.__remote_frame, padx = 15, pady = 15, bd = 2, text = "画質を選択")
        self.__video_quality_radio_frame.pack(padx = self.__button_padx, side = "left")
        #ラジオボタンの設定
        self.__video_quality_value = tk.IntVar()
        self.__video_quality_value.set(136)
        self.__video_quality_radio_button_1080 = tk.Radiobutton(self.__video_quality_radio_frame, text = "1080p", variable = self.__video_quality_value, value = 137, command = self.setVideoQuality)
        self.__video_quality_radio_button_1080.pack()
        self.__video_quality_radio_button_720 = tk.Radiobutton(self.__video_quality_radio_frame, text = "720p", variable = self.__video_quality_value, value = 136, command = self.setVideoQuality)
        self.__video_quality_radio_button_720.pack()
        self.__video_quality_radio_button_480 = tk.Radiobutton(self.__video_quality_radio_frame, text = "480p", variable = self.__video_quality_value, value = 135, command = self.setVideoQuality)
        self.__video_quality_radio_button_480.pack()
        self.__video_quality_radio_button_360 = tk.Radiobutton(self.__video_quality_radio_frame, text = "360p", variable = self.__video_quality_value, value = 134, command = self.setVideoQuality)
        self.__video_quality_radio_button_360.pack()
        self.__video_quality_radio_button_240 = tk.Radiobutton(self.__video_quality_radio_frame, text = "240p", variable = self.__video_quality_value, value = 133, command = self.setVideoQuality)
        self.__video_quality_radio_button_240.pack()
        self.__video_quality_radio_button_144 = tk.Radiobutton(self.__video_quality_radio_frame, text = "144p", variable = self.__video_quality_value, value = 160, command = self.setVideoQuality)
        self.__video_quality_radio_button_144.pack()

    def setLocalFormParts(self):
        self.__local_frame = tk.LabelFrame(self.__select_frame, padx = 15, pady = 15, bd = 4, text = "ローカルから動画を選択")
        self.__local_frame.pack(padx = self.__button_padx, side = "left")
        self.__quality_select_frame = tk.Frame(self.__local_frame)
        self.__quality_select_frame.pack(padx = self.__button_padx, side = "left")
        #音質のラジオボタンの配置
        self.__audio_quality_radio_frame = tk.LabelFrame(self.__quality_select_frame, padx = 15, pady = 15, bd = 2, text = "サンプリングレートを選択")
        self.__audio_quality_radio_frame.pack(pady = 10)
        #ラジオボタンの設定
        self.__audio_quality_value = tk.IntVar()
        self.__audio_quality_value.set(44100)
        self.__audio_quality_radio_button_44100 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "44100Hz", variable = self.__audio_quality_value, value = 44100, command = self.setAudioQuality)
        self.__audio_quality_radio_button_44100.pack()
        self.__audio_quality_radio_button_32000 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "32000Hz", variable = self.__audio_quality_value, value = 32000, command = self.setAudioQuality)
        self.__audio_quality_radio_button_32000.pack()
        self.__audio_quality_radio_button_16000 = tk.Radiobutton(self.__audio_quality_radio_frame, text = "16000Hz", variable = self.__audio_quality_value, value = 16000, command = self.setAudioQuality)
        self.__audio_quality_radio_button_16000.pack()
        #動画選択のボタン
        self.__select_button = tk.Canvas(
            self.__quality_select_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__select_button.pack()
        self.__select_tkimg = self.getImg("config/fig/select.jpg", self.__button_width, self.__button_height)
        self.__select_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__select_tkimg,
            tags = "select"
        )
        self.__select_button.tag_bind("select", "<ButtonPress-1>", self.setVideoFile)
        #訓練と本番の選択フォーム
        self.setTrainTestFormParts()

    def setStatusParts(self):
        #ステータス表示
        self.__status_frame = tk.Frame(self.__scroll_frame)
        self.__status_frame.pack()
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
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__wait_img.pack(padx = self.__status_padx, side = "left")
        self.__wait_tkimg = self.getImg("config/fig/waiting.jpg", self.__status_width, self.__status_height)
        self.__wait_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__wait_tkimg
        )
        #mp3 creating
        self.__mp3_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__mp3_img.pack(padx = self.__status_padx, side = "left")
        self.__mp3_tkimg = self.getImg("config/fig/not_creating_mp3.jpg", self.__status_width, self.__status_height)
        self.__mp3_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__mp3_tkimg
        )
        #download
        self.__download_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__download_img.pack(padx = self.__status_padx, side = "left")
        self.__download_tkimg = self.getImg("config/fig/not_downloading.jpg", self.__status_width, self.__status_height)
        self.__download_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__download_tkimg
        )
        #create train data
        self.__create_data_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__create_data_img.pack(padx = self.__status_padx, side = "left")
        self.__create_data_tkimg = self.getImg("config/fig/not_creating_train.jpg", self.__status_width, self.__status_height)
        self.__create_data_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__create_data_tkimg
        )
        #train
        self.__train_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__train_img.pack(padx = self.__status_padx, side = "left")
        self.__train_tkimg = self.getImg("config/fig/not_training.jpg", self.__status_width, self.__status_height)
        self.__train_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__train_tkimg
        )
        #load
        self.__load_img = tk.Canvas(
            self.__status_frame, # 親要素をメインウィンドウに設定
            width = self.__status_width,  # 幅を設定
            height = self.__status_height # 高さを設定
        )
        self.__load_img.pack(padx = self.__status_padx, side = "left")
        self.__load_tkimg = self.getImg("config/fig/not_loading.jpg", self.__status_width, self.__status_height)
        self.__load_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__load_tkimg
        )

    def setTrainTestFormParts(self):
        #訓練・本番のラジオボタンの配置
        self.__train_frame = tk.Frame(self.__local_frame)
        self.__train_frame.pack(padx = self.__button_padx, side = "left")
        self.__train_radio_frame = tk.LabelFrame(self.__train_frame, padx = 15, pady = 15, bd = 2, text = "訓練/本番を選択")
        self.__train_radio_frame.pack()
        self.__train_value = tk.IntVar()
        self.__train_value.set(0)
        self.__is_train = 0
        self.__train_radio_button = tk.Radiobutton(self.__train_radio_frame, text = "訓練", variable = self.__train_value, value = 1, command = self.setTrainTest)
        self.__train_radio_button.pack()
        self.__test_radio_button = tk.Radiobutton(self.__train_radio_frame, text = "本番", variable = self.__train_value, value = 0, command = self.setTrainTest)
        self.__test_radio_button.pack()
        #通知の間隔
        self.__interval_frame = tk.Frame(self.__train_frame)
        self.__interval_frame.pack(pady = 5)
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
        self.__train_test_img = tk.Canvas(
            self.__train_test_frame, # 親要素をメインウィンドウに設定
            width = self.__train_test_width,  # 幅を設定
            height = self.__train_test_height # 高さを設定
        )
        self.__train_test_img.pack()
        self.__train_test_tkimg = self.getImg("config/fig/on.jpg", self.__train_test_width, self.__train_test_height)
        self.__train_test_img.create_image(
            int(self.__train_test_width / 2),
            int(self.__train_test_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )
        self.__train_test_img.tag_bind("train_test", "<ButtonPress-1>", self.turnTrainTest)

        #キャラクター名の選択
        self.__classfier_frame = tk.Frame(self.__local_frame)
        self.__classfier_frame.pack(padx = self.__button_padx, side = "left")
        self.__character_frame = tk.LabelFrame(self.__classfier_frame, padx = 15, pady = 15, bd = 2, text = "キャラクター名を選択")
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
        self.__initialize_img = tk.Canvas(
            self.__classfier_frame, # 親要素をメインウィンドウに設定
            width = self.__initialize_width,  # 幅を設定
            height = self.__initialize_height # 高さを設定
        )
        self.__initialize_img.pack(pady = 10)
        self.__initialize_tkimg = self.getImg("config/fig/initialize.jpg", self.__initialize_width, self.__initialize_height)
        self.__initialize_img.create_image(
            int(self.__initialize_width / 2),
            int(self.__initialize_height / 2),
            image = self.__initialize_tkimg,
            tags = "initialize"
        )
        self.__initialize_img.tag_bind("initialize", "<ButtonPress-1>", self.initializeCharacter)

    def setVideoTextParts(self):
        self.__text_frame = tk.Frame(self.__canvas_frame)
        self.__text_frame.pack(pady = 10)
        self.__video_text_frame = tk.Frame(self.__text_frame)
        self.__video_text_frame.pack(side = "left")
        #ビデオのタイトル
        self.__video_title_text = tk.StringVar()
        self.__video_title_font = font.Font(self.__video_text_frame, family = 'Helvetica', size = 20, weight = 'bold')
        self.__video_title_label = tk.Label(
            self.__video_text_frame,
            textvariable = self.__video_title_text,
            font = self.__video_title_font
        )
        self.__video_title_label.pack()
        #ビデオの時間
        self.__video_time_text = tk.StringVar()
        self.__video_time_font = font.Font(self.__video_text_frame, family = 'Helvetica', size = 15)
        self.__video_time_label = tk.Label(
            self.__video_text_frame,
            textvariable = self.__video_time_text,
            font = self.__video_time_font
        )
        self.__video_time_label.pack()
        #動画操作ボタン関連の配置
        self.setVideoButtonParts()
        #音量に関するオブジェクトの配置
        self.__audio_frame = tk.Frame(self.__text_frame)
        self.__audio_frame.pack()
        #音量表示
        self.__audio_volume_text = tk.StringVar()
        self.__audio_title_font = font.Font(self.__audio_frame, family = 'Helvetica', size = 20, weight = 'bold')
        self.__audio_title_label = tk.Label(self.__audio_frame, text = "音量", font = self.__audio_title_font)
        self.__audio_title_label.pack()
        self.__audio_volume_label = tk.Label(
            self.__audio_frame,
            textvariable = self.__audio_volume_text,
        )
        self.__audio_volume_label.pack()
        #音量調節ボタンの配置
        self.setAudioButtonParts()

    def setVideoButtonParts(self):
        self.__video_button_frame = tk.Frame(self.__video_text_frame)
        self.__video_button_frame.pack()
        #早戻しボタン
        self.__rewind_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__rewind_button.pack(padx = self.__button_padx, side = "left")
        self.__rewind_tkimg = self.getImg("config/fig/rewind.jpg", self.__button_width, self.__button_height)
        self.__rewind_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__rewind_tkimg,
            tags = "rewind"
        )
        self.__rewind_button.tag_bind("rewind", "<ButtonPress-1>", self.videoRewind)
        #再生・一時停止ボタン
        self.__pause_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__pause_button.pack(padx = self.__button_padx, side = "left")
        self.__pause_tkimg = self.getImg("config/fig/start.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )
        self.__pause_button.tag_bind("pause", "<ButtonPress-1>", self.videoStopOrStart)
        #早送りボタン
        self.__fast_forward_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__fast_forward_button.pack(padx = self.__button_padx, side = "left")
        self.__fast_forward_tkimg = self.getImg("config/fig/fastforward.jpg", self.__button_width, self.__button_height)
        self.__fast_forward_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__fast_forward_tkimg,
            tags = "fastforward"
        )
        self.__fast_forward_button.tag_bind("fastforward", "<ButtonPress-1>", self.videoFastForward)

    def setAudioButtonParts(self):
        self.__audio_button_frame = tk.Frame(self.__audio_frame)
        self.__audio_button_frame.pack()
        #音量を下げるボタン
        self.__audio_volume_down_button = tk.Canvas(
            self.__audio_button_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__audio_volume_down_button.pack(padx = self.__button_padx, side = "left")
        self.__audio_volume_down_tkimg = self.getImg("config/Fig/volume_down.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_down_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_down_tkimg,
            tags = "volume_down"
        )
        self.__audio_volume_down_button.tag_bind("volume_down", "<ButtonPress-1>", self.volumeDown)
        #音量を上げるボタン
        self.__audio_volume_up_button = tk.Canvas(
            self.__audio_button_frame, # 親要素をメインウィンドウに設定
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__audio_volume_up_button.pack(padx = self.__button_padx, side = "left")
        self.__audio_volume_up_tkimg = self.getImg("config/fig/volume_up.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_up_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_up_tkimg,
            tags = "volume_up"
        )
        self.__audio_volume_up_button.tag_bind("volume_up", "<ButtonPress-1>", self.volumeUp)

    def setVideoURL(self, event):
        if len(self.__form.get()) != 0:
            self.__vc.downloader.download_url = self.__form.get()
            self.__vc.downloadVideo()
            if self.__vc.downloader.is_error == True:
                messagebox.showerror("エラー", "このURLは有効ではありません")
            elif self.__vc.downloader.downloadable == False:
                messagebox.showerror("エラー", "この動画の画質は" + ",".join(self.getQuality(self.__vc.downloader.quality_list)) + "しか選択できません")
            else:
                self.changeStatus("download")
        else:
            messagebox.showerror("エラー", "URLを入力してください")

    def loadVideo(self):
        self.__vc.loadVideo()
        self.__train_cv = CV.CV(video_path = self.__vc.cv.video_path)
        if self.__first_time_flag == False:
            self.__pause_tkimg = self.getImg("config/fig/start.jpg", self.__button_width, self.__button_height)
            self.__pause_button.create_image(
                int(self.__button_width / 2),
                int(self.__button_height / 2),
                image = self.__pause_tkimg,
                tags = "pause"
            )
            self.__pause_button.tag_bind("pause", "<ButtonPress-1>", self.videoStopOrStart)
        if self.__is_train == True:
            ret = messagebox.askyesno("確認", "訓練中にこの動画を閲覧しますか?")
            while not self.__character_name:
                    self.__character_name = sd.askstring("新規入力", "キャラクター名を入力してください(英字)")
                    if self.__character_name is None:
                        break
            if self.__character_name:
                if ret == True:
                    if not pathlib.Path(self.__vc.audio.audio_path).exists():
                        messagebox.showinfo("確認", "サンプリング周波数" + str(self.__vc.audio.frequency) + "Hzでmp3ファイルを生成します")
                        self.__vc.audio.createMP3BackGround(self.__vc.cv)
                        self.changeStatus("mp3")
                    else:
                        if self.__first_time_flag == True:
                            self.setCanvasParts()
                        self.prepareVideo()

                #別スレッドで訓練開始
                jpg_list = []
                if pathlib.Path("tmp/train/" + self.__character_name + ".zip").exists():
                    with zipfile.ZipFile("tmp/train/" + self.__character_name + ".zip", "r") as train_zip:
                        jpg_list = [path for path in train_zip.namelist() if self.__vc.cv.video_title in path]
                if len(jpg_list) == 0:
                    self.__create_train_process = subprocess.Popen(("python", "create_train_data.py", self.__vc.cv.video_path, self.__character_name))
                    self.changeStatus("create_data")
                else:
                    if self.__is_on:
                        self.__train_process = subprocess.Popen(("python", "train.py"))
                        self.changeStatus("train")
                self.updateCharacterList()
                if len(self.__character_list.curselection()) == 0 or self.__character_list.curselection()[0] == 0:
                    self.__character_name = ""

        else:
            if not pathlib.Path(self.__vc.audio.audio_path).exists():
                messagebox.showinfo("確認", "サンプリング周波数" + str(self.__vc.audio.frequency) + "Hzでmp3ファイルを生成します")
                self.__vc.audio.createMP3BackGround(self.__vc.cv)
                self.changeStatus("mp3")
            else:
                if self.__first_time_flag == True:
                    self.setCanvasParts()
                self.prepareVideo()
            if self.__vc.cv.classifier is None and pathlib.Path("config/classifier.xml").exists():
                self.__load_thread = threading.Thread(target = self.__vc.cv.loadClassifier)
                self.__load_thread.setDaemon(True)
                self.__load_thread.start()
                self.changeStatus("load")

    def prepareVideo(self):
        self.__vc.audio.initAudio()
        self.__video_title_text.set("".join([self.__vc.cv.video_title[j] for j in range(len(self.__vc.cv.video_title)) if ord(self.__vc.cv.video_title[j]) in range(65536)]))
        self.__audio_volume_text.set(self.__vc.audio.volume0to100())
        self.setCanvas()

    def videoStopOrStart(self, event):
        if self.__button_available:
            self.__vc.videoStopOrStart()
            if self.__vc.play_flag:
                self.dispImg()
                self.__pause_tkimg = self.getImg("config/fig/pause.jpg", self.__button_width, self.__button_height)
                if self.__is_on:
                    self.setDetectTimer()
            else:
                self.__pause_tkimg = self.getImg("config/fig/start.jpg", self.__button_width, self.__button_height)
            self.__pause_button.create_image(
                int(self.__button_width / 2),
                int(self.__button_height / 2),
                image = self.__pause_tkimg,
                tags = "pause"
            )
            self.__pause_button.tag_bind("pause", "<ButtonPress-1>", self.videoStopOrStart)

    def videoRewind(self, event):
        if self.__button_available:
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * max(0, self.__vc.cv.cap.get(0) / 1000 - 5)))
            self.setCanvas()

    def videoFastForward(self, event):
        if self.__button_available:
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * min(self.__vc.cv.video_len, self.__vc.cv.cap.get(0) / 1000 + 5)))
            self.setCanvas()

    def setCanvas(self):
        self.__vc.fetchImg()
        self.__video_seek_bar.set(int(self.__vc.cv.cap.get(0) / 1000))
        if self.__vc.cv.ret == False:
            self.__vc.play_flag == False
            return
        self.__video_time_text.set("{0:0>2}:{1:0>2}:{2:0>2} / {3:0>2}:{4:0>2}:{5:0>2}".format(*self.__vc.cv.current_time.getTime(), *self.__vc.cv.whole_time.getTime()))
        self.__canvas.create_image(
            int(self.__vc.cv.disp_img_width / 2),
            int(self.__vc.cv.disp_img_height / 2),
            image = self.__vc.cv.canvas_img,
            tags = "image"
        )
        self.__canvas.tag_bind("image", "<ButtonPress-1>", self.videoStopOrStart)
        #canvas.tag_bind("image", "<ButtonPress-2>", self.videoRewind)
        self.__img_process_time = (time.time() - self.__vc.fetch_time) * 1000 + threading.activeCount() * 0.5

    def dispImg(self):
        if self.__vc.play_flag:
            self.setCanvas()
            self.__root.after(int(1000 / self.__vc.cv.video_fps - self.__img_process_time), self.dispImg)

    def volumeDown(self, event):
        if self.__button_available:
            self.__vc.audio.setVolume(max(0.0, self.__vc.audio.volume - 0.05))
            self.__audio_volume_text.set(self.__vc.audio.volume0to100())

    def volumeUp(self, event):
        if self.__button_available:
            self.__vc.audio.setVolume(min(1.0, self.__vc.audio.volume + 0.05))
            self.__audio_volume_text.set(self.__vc.audio.volume0to100())

    def setVideoFile(self, event):
        self.__filetype = [("動画ファイル", ("*.mp4", "*.mov", "*.avi", "*.wmv", "*.flv"))]
        self.__dirpath = pathlib.Path(__file__).parent
        self.__vc.cv.video_path = filedialog.askopenfilename(filetypes = self.__filetype, initialdir = self.__dirpath)
        if self.__vc.cv.video_path:
            self.loadVideo()

    def setVideoQuality(self):
        self.__vc.downloader.video_format = str(self.__video_quality_value.get())

    def setAudioQuality(self):
        self.__vc.audio.frequency = self.__audio_quality_value.get()

    def setTrainTest(self):
        self.__is_train = self.__train_value.get()

    def scrollCanvas(self, event):
        self.__scroll_canvas.config(scrollregion = self.__scroll_canvas.bbox("all"), height = self.__window_height * 2)

    def getImg(self, img_path, width, height):
        img = Image.open(img_path)
        resize_img = img.resize((width, height))
        tkimg = ImageTk.PhotoImage(resize_img)
        return tkimg

    def setCharacterName(self, event):
        index = self.__character_list.curselection()[0]
        if index == 0:
            self.__character_name = ""
        else:
            self.__character_name = self.__character_string[index]

    def updateCharacterList(self):
        self.__character_string = ["新規に追加"] + getCharacter()
        self.__characters.set(self.__character_string)

    def getQuality(self, quality):
        quality_str = []
        if "137" in quality:
            quality_str.append("1080p")
        if "136" in quality:
            quality_str.append("720p")
        if "135" in quality:
            quality_str.append("480p")
        if "134" in quality:
            quality_str.append("360p")
        if "133" in quality:
            quality_str.append("240p")
        if "160" in quality:
            quality_str.append("144p")
        return quality_str

    def changeStatus(self, status):
        if status == "download":
            self.__is_downloading = not self.__is_downloading
            if self.__is_downloading:
                self.__download_tkimg = self.getImg("config/fig/downloading.jpg", self.__status_width, self.__status_height)
                th = threading.Thread(target = self.watchDownload)
                th.setDaemon(True)
                th.start()
            else:
                self.__download_tkimg = self.getImg("config/fig/not_downloading.jpg", self.__status_width, self.__status_height)
            self.__download_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__download_tkimg
            )
        if status == "mp3":
            self.__is_creating = not self.__is_creating
            if self.__is_creating:
                self.__mp3_tkimg = self.getImg("config/fig/creating_mp3.jpg", self.__status_width, self.__status_height)
                th = threading.Thread(target = self.watchMP3)
                th.setDaemon(True)
                th.start()
            else:
                self.__mp3_tkimg = self.getImg("config/fig/not_creating_mp3.jpg", self.__status_width, self.__status_height)
            self.__mp3_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__mp3_tkimg
            )
        if status == "train":
            self.__is_training = not self.__is_training
            if self.__is_training:
                self.__train_tkimg = self.getImg("config/fig/training.jpg", self.__status_width, self.__status_height)
                th = threading.Thread(target = self.watchTrain)
                th.setDaemon(True)
                th.start()
            else:
                self.__train_tkimg = self.getImg("config/fig/not_training.jpg", self.__status_width, self.__status_height)
            self.__train_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__train_tkimg
            )
        if status == "load":
            self.__is_loading = not self.__is_loading
            if self.__is_loading:
                self.__load_tkimg = self.getImg("config/fig/loading.jpg", self.__status_width, self.__status_height)
                th = threading.Thread(target = self.watchLoad)
                th.setDaemon(True)
                th.start()
            else:
                self.__load_tkimg = self.getImg("config/fig/not_loading.jpg", self.__status_width, self.__status_height)
            self.__load_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__load_tkimg
            )
        if status == "create_data":
            self.__is_creating_data = not self.__is_creating_data
            if self.__is_creating_data:
                self.__create_data_tkimg = self.getImg("config/fig/creating_train.jpg", self.__status_width, self.__status_height)
                th = threading.Thread(target = self.watchCreateData)
                th.setDaemon(True)
                th.start()
            else:
                self.__create_data_tkimg = self.getImg("config/fig/not_creating_train.jpg", self.__status_width, self.__status_height)
            self.__create_data_img.create_image(
                int(self.__status_width / 2),
                int(self.__status_height / 2),
                image = self.__create_data_tkimg
            )
        if self.__is_creating or self.__is_training or self.__is_downloading or self.__is_loading or self.__is_creating_data:
            self.__wait_tkimg = self.getImg("config/fig/not_waiting.jpg", self.__status_width, self.__status_height)
        else:
            self.__wait_tkimg = self.getImg("config/fig/waiting.jpg", self.__status_width, self.__status_height)
        self.__wait_img.create_image(
            int(self.__status_width / 2),
            int(self.__status_height / 2),
            image = self.__wait_tkimg
        )

    def watchTrain(self):
        if not self.__train_process is None and self.__train_process.poll() is None:
            th = threading.Timer(1, self.watchTrain)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("train")

    def watchDownload(self):
        if not self.__vc.downloader.proc is None and self.__vc.downloader.proc.poll() is None:
            th = threading.Timer(1, self.watchDownload)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("download")

    def watchMP3(self):
        if not self.__vc.audio.proc is None and self.__vc.audio.proc.poll() is None:
            self.__button_available = False
            self.deniedPlayVideo()
            th = threading.Timer(1, self.watchMP3)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("mp3")
            if self.__first_time_flag == True:
                self.setCanvasParts()
            self.prepareVideo()
            if self.__load_thread is None or not self.__load_thread.is_alive():
                self.__button_available = True

    def watchLoad(self):
        if not self.__load_thread is None and self.__load_thread.is_alive():
            self.__button_available = False
            self.deniedPlayVideo()
            th = threading.Timer(1, self.watchLoad)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("load")
            if self.__vc.audio.proc is None or not self.__vc.audio.proc.poll() is None:
                self.__button_available = True

    def watchCreateData(self):
        if not self.__create_train_process is None and self.__create_train_process.poll() is None:
            th = threading.Timer(1, self.watchCreateData)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("create_data")
            if self.__is_on:
                self.__train_process = subprocess.Popen(("python", "train.py"))
                self.changeStatus("train")

    def detectTimer(self):
        #検出できた時の処理
        if self.__vc.cv.character_names != [] and self.__vc.cv.confidenceds != []:
            self.noticeDetection()
        if self.__detect_num <= 3:
            if self.__vc.play_flag:
                th = threading.Thread(target = self.__vc.cv.detectCharacter)
                th.setDaemon(True)
                th.start()
            if self.__is_on:
                self.__cycle = int(self.__interval_form.get())
                self.__detect_thread = threading.Timer(self.__cycle, self.detectTimer)
                self.__detect_thread.setDaemon(True)
                self.__detect_thread.start()

    def turnTrainTest(self, event):
        self.__is_on = not self.__is_on
        if self.__is_on:
            self.__train_test_tkimg = self.getImg("config/fig/on.jpg", self.__train_test_width, self.__train_test_height)
            self.setDetectTimer()
        else:
            self.__train_test_tkimg = self.getImg("config/fig/off.jpg", self.__train_test_width, self.__train_test_height)
        self.__train_test_img.create_image(
            int(self.__train_test_width / 2),
            int(self.__train_test_height / 2),
            image = self.__train_test_tkimg,
            tags = "train_test"
        )
        self.__train_test_img.tag_bind("train_test", "<ButtonPress-1>", self.turnTrainTest)

    def setDetectTimer(self):
        if self.__detect_thread is None or not self.__detect_thread.is_alive():
            self.__cycle = int(self.__interval_form.get())
            self.__detect_num = 0
            self.__detect_thread = threading.Timer(self.__cycle, self.detectTimer)
            self.__detect_thread.setDaemon(True)
            self.__detect_thread.start()

    def noticeDetection(self):
        #macOSの時の通知
        if platform.system() == "Darwin":
            for i in range(len(self.__vc.cv.character_names)):
                notification_str = "\'display notification \"" + self.__vc.cv.character_names[i] + " detect\" with title \"NagaraOtaku\"\'"
                os.system("osascript -e " + notification_str)
            self.__detect_num += 1
        #WIndowsの時の通知
        elif platform.system() == "Windows":
            for i in range(len(self.__vc.cv.character_names)):
                print("hoge")
            self.__detect_num += 1
        self.__vc.cv.clearList()
        if self.__detect_num >= 3:
            self.turnTrainTest(None)
            self.__detect_num = 0

    def initializeCharacter(self, event):
        ret = messagebox.askyesno("確認", "識別器を初期化しますか?")
        if ret == True:
            classifier_path = pathlib.Path("config/classifier.xml")
            if classifier_path.exists():
                classifier_path.unlink()
            character_path = pathlib.Path("config/characters.txt")
            if character_path.exists():
                character_path.unlink()
            if pathlib.Path("tmp/train").exists():
                shutil.rmtree("tmp/train")
        self.updateCharacterList()

    def seekPos(self, *args):
        if self.__button_available:
            self.deniedPlayVideo()
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * self.__video_seek_bar.get()))
            self.setCanvas()

    def deniedPlayVideo(self):
        self.__vc.deniedPlayVideo()
        self.__pause_tkimg = self.getImg("config/fig/start.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )
        self.__pause_button.tag_bind("pause", "<ButtonPress-1>", self.videoStopOrStart)

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
