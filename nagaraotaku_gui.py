import tkinter as tk
import tkinter.font as font
import tkinter.filedialog as filedialog
import os
import cv2
import re
import ffmpeg
import pygame
import random
import time
import youtube_dl
import subprocess
from PIL import Image, ImageTk

class Audio:
    def __init__(self):
        self.__frequency = 44100
        if self.__frequency % 1000 == 0:
            self.__ar = self.__frequency // 1000
        else:
            self.__ar = self.__frequency / 1000
        self.__ar = str(self.__ar) + "k"

    @property
    def volume(self):
        return self.__volume

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, rate):
        self.__frequency = rate

    def createMP3BackGround(self, cv):
        self.__audio_title = cv.video_title + ".mp3"
        self.__audio_path = cv.parent_directory + "/" + self.__audio_title
        if not os.path.isfile(self.__audio_path):
            self.__command = (
                "ffmpeg",
                "-i",
                cv.video_path,
                "-acodec",
                "mp3",
                "-ac",
                "2",
                "-ar",
                self.__ar,
                self.__audio_path
            )
            subprocess.Popen(self.__command)

    def createMP3ForeGround(self, cv):
        self.__audio_title = cv.video_title + ".mp3"
        self.__audio_path = cv.parent_directory + "/" + self.__audio_title
        if not os.path.isfile(self.__audio_path):
            out, _ = (
                ffmpeg
                .input(cv.video_path)
                .output(self.__audio_path, acodec='mp3', ac=2, ar=self.__ar)
                .overwrite_output()
                .run(capture_stdout=True)
            )

    def initAudio(self):
        pygame.mixer.init(frequency = self.__frequency // 2)
        pygame.mixer.music.load(self.__audio_path) #音源を読み込みS
        self.__volume = pygame.mixer.music.get_volume()

    def startAudio(self, second):
        pygame.mixer.music.play(loops = 0, start = second + 0.1)

    def stopAudio(self):
        pygame.mixer.music.stop()

    def pauseAudio(self):
        pygame.mixer.music.pause()

    def unpauseAudio(self):
        pygame.mixer.music.unpause()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume)
        self.__volume = volume

    def volume0to100(self):
        return str(round(self.__volume * 100 + 0.5))

class VideoTime:
    def __init__(self):
        self.__hour = 0
        self.__min = 0
        self.__sec = 0

    @property
    def hour(self):
        return self.__hour

    @property
    def min(self):
        return self.__min

    @property
    def sec(self):
        return self.__sec

    def setTime(self, time):
        temp = time
        self.__hour = int(temp // 3600)
        temp %= 3600
        self.__min = int(temp // 60)
        temp %= 60
        self.__sec = int(temp)

    def getTime(self):
        return self.__hour, self.__min, self.__sec

class CV:
    def __init__(self):
        self.__disp_img_width = 800
        self.__disp_img_height = 450
        self.__current_time = VideoTime()
        self.__whole_time = VideoTime()
        self.__video_path = ""
        self.__video_title = ""
        self.__parent_directory = ""

    @property
    def disp_img_width(self):
        return self.__disp_img_width

    @property
    def disp_img_height(self):
        return self.__disp_img_height

    @property
    def current_time(self):
        return self.__current_time

    @property
    def whole_time(self):
        return self.__whole_time

    @property
    def video_title(self):
        return self.__video_title

    @property
    def parent_directory(self):
        return self.__parent_directory

    @property
    def cap(self):
        return self.__cap

    @property
    def ret(self):
        return self.__ret

    @property
    def video_fps(self):
        return self.__video_fps

    @property
    def video_len(self):
        return self.__video_len

    @property
    def canvas_img(self):
        return self.__canvas_img

    @property
    def video_path(self):
        return self.__video_path

    @video_path.setter
    def video_path(self, path):
        self.__video_path = path

    def loadVideo(self):
        #動画のパス
        if not os.path.isfile(self.__video_path):
            return
        self.__cap = cv2.VideoCapture(self.__video_path)
        self.__video_frame = self.__cap.get(cv2.CAP_PROP_FRAME_COUNT) # フレーム数を取得する
        self.__video_fps = self.__cap.get(cv2.CAP_PROP_FPS)           # FPS を取得する
        self.__video_len = self.__video_frame // self.__video_fps
        self.__whole_time.setTime(self.__video_len)
        self.__parent_directory, self.__video_file_name = os.path.split(self.__video_path)
        self.__video_title = os.path.splitext(self.__video_file_name)[0]

    def getFrameImage(self):
        self.__ret, self.__frame = self.__cap.read()
        if self.__ret == False:
            return
        self.__resize_frame = cv2.resize(self.__frame, (self.__disp_img_width, self.__disp_img_height))
        self.__convert_color_frame = cv2.cvtColor(self.__resize_frame, cv2.COLOR_BGR2RGB)
        self.__frame_pil = Image.fromarray(self.__convert_color_frame)
        self.__canvas_img = ImageTk.PhotoImage(self.__frame_pil)

class YoutubeDownloader:
    def __init__(self):
        self.__download_url = ""
        #1080p:137, 720p:136, 480p:135, 360p:134, 240p:133, 144p:160
        self.__video_format = "136"
        self.__audio_format = "140"
        self.__download_format = "mp4"

    @property
    def download_url(self):
        return self.__download_url

    @download_url.setter
    def download_url(self, url):
        self.__download_url = url

    @property
    def video_format(self):
        return self.__video_format

    @video_format.setter
    def video_format(self, format):
        self.__video_format = format


    def downloadVideo(self):
        self.__command = (
            "youtube-dl",
            "--format",
            self.__video_format + "+" + self.__audio_format,
            "--merge-output-format",
            self.__download_format,
            "--output",
            "%(title)s_%(height)sp.%(ext)s",
            self.__download_url
        )
        subprocess.Popen(self.__command)

class VideoController:
    def __init__(self):
        self.__cv = CV()
        self.__audio = Audio()
        self.__downloader = YoutubeDownloader()

    @property
    def cv(self):
        return self.__cv

    @property
    def downloader(self):
        return self.__downloader

    @property
    def fetch_time(self):
        return self.__fetch_time

    @property
    def play_flag(self):
        return self.__play_flag

    @property
    def audio(self):
        return self.__audio

    def loadVideo(self):
        self.__cv.loadVideo()
        self.__audio.createMP3ForeGround(self.__cv)
        self.__audio.initAudio()
        self.__play_flag = False

    def videoStopOrStart(self):
        self.__play_flag = not self.__play_flag
        if self.__play_flag:
            self.__audio.startAudio(self.__cv.cap.get(0) / 1000)
        else:
            self.__audio.stopAudio()

    def setVideoPosition(self, frame_pos):
        self.__cv.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        self.__audio.stopAudio()
        if self.__play_flag:
            self.__audio.startAudio(self.__cv.cap.get(0) / 1000)

    def fetchImg(self):
        self.__fetch_time = time.time()
        self.__cv.getFrameImage()
        #動画の秒数の表示
        self.__cv.current_time.setTime(int(self.__cv.cap.get(1) / self.__cv.video_fps))

    def downloadVideo(self):
        self.__downloader.downloadVideo()
        self.__audio.createMP3BackGround(self.__cv)

class GUI:
    def __init__(self):
        self.__window_width = 1200
        self.__window_height = 800
        self.__scroll_canvas_width = self.__window_width - 50
        self.__button_width = 10
        self.__scroll_width = 5
        self.__button_padx = 20
        self.__user_process_time = 0
        self.__vc = VideoController()
        self.__root = tk.Tk()
        #Tkinterの初期設定
        self.__root.title("NagaraOtaku")
        self.__root.geometry(str(self.__window_width) + "x" + str(self.__window_height))
        self.__root.resizable(width = 1, height = 1)
        self.__root_frame = tk.Frame(self.__root)
        self.__root_frame.pack(fill = "both")
        #全体をキャンバスで覆う
        self.__scroll_canvas = tk.Canvas(self.__root_frame, width = self.__scroll_canvas_width, height = self.__window_height)
        #スクロールバーの設置
        self.__scrollbar = tk.Scrollbar(self.__root_frame, orient = "vertical", command = self.__scroll_canvas.yview)
        self.__scroll_canvas.config(yscrollcommand = self.__scrollbar.set)
        self.__scroll_canvas.pack(padx = 10, pady = 10, side = "left")
        self.__scrollbar.pack(side = "right", fill = "y")
        self.__scroll_frame = tk.Frame(self.__scroll_canvas)
        self.__scroll_canvas.create_window((0, 0), window = self.__scroll_frame)
        self.__scroll_frame.bind("<Configure>", self.scrollCanvas)

        self.setFormParts()
        self.setCanvasParts()
        self.setVideoButtonParts()

        #ボタンの文字が表示されないバグを解消
        self.__root.update()
        self.__root.geometry('%dx%d' % (self.__window_width + 1,self.__window_height + 1))

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
        self.__remote_frame = tk.LabelFrame(self.__select_frame, padx = 15, pady = 15, bd = 4, text = "ネットから動画を選択")
        self.__remote_frame.pack(padx = self.__button_padx, side = "left")
        #動画URLフォームの配置
        self.__form_frame = tk.LabelFrame(self.__remote_frame, padx = 15, pady = 15, bd = 2, text = "動画のURLを入力")
        self.__form_frame.pack(side = "left")
        #フォーム
        self.__form = tk.Entry(self.__form_frame, width = 30)
        self.__form.pack(side = "left")
        #動画ダウンロードのボタン
        self.__form_button = tk.Button(self.__form_frame, text = "ダウンロード", width = self.__button_width)
        self.__form_button.bind("<ButtonPress-1>", self.setVideoURL)
        self.__form_button.pack(padx = self.__button_padx, side = "left")
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
        #ローカルな動画選択フォーム
        self.__local_frame = tk.LabelFrame(self.__select_frame, padx = 15, pady = 15, bd = 4, text = "ローカルから動画を選択")
        self.__local_frame.pack(padx = self.__button_padx, side = "left")
        #音質のラジオボタンの配置
        self.__audio_quality_radio_frame = tk.LabelFrame(self.__local_frame, padx = 15, pady = 15, bd = 2, text = "サンプリングレートを選択")
        self.__audio_quality_radio_frame.pack(padx = self.__button_padx, side = "left")
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

        self.__select_button = tk.Button(self.__local_frame, text = "動画を選択", width = self.__button_width)
        self.__select_button.bind("<ButtonPress-1>", self.setVideoFile)
        self.__select_button.pack(padx = self.__button_padx, side = "left")

    def setCanvasParts(self):
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
        #self.canvas.place(relx = self.canvas_relx, relwidth = self.canvas_relwidth,  rely = self.canvas_rely, relheight = self.canvas_relheight)
        #テキストの配置
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
        self.__video_time_label = tk.Label(
            self.__video_text_frame,
            textvariable = self.__video_time_text
        )
        self.__video_time_label.pack()
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
        self.__audio_button_frame = tk.Frame(self.__audio_frame)
        self.__audio_button_frame.pack()
        #音量を下げるボタン
        self.__audio_volume_down_button = tk.Button(self.__audio_button_frame, text = "音量Down", width = self.__button_width)
        self.__audio_volume_down_button.bind("<ButtonPress-1>", self.volumeDown)
        self.__audio_volume_down_button.pack(padx = self.__button_padx, side = "left")
        #音量を上げるボタン
        self.__audio_volume_up_button = tk.Button(self.__audio_button_frame, text = "音量Up", width = self.__button_width)
        self.__audio_volume_up_button.bind("<ButtonPress-1>", self.volumeUp)
        self.__audio_volume_up_button.pack(padx = self.__button_padx, side = "left")

    def setVideoButtonParts(self):
        #動画操作ボタン関連の配置
        self.__video_button_frame = tk.Frame(self.__scroll_frame)
        self.__video_button_frame.pack()
        #早戻しボタン
        self.__rewind_button = tk.Button(self.__video_button_frame, text = "5秒戻す", width = self.__button_width)
        self.__rewind_button.bind("<ButtonPress-1>", self.videoRewind)
        self.__rewind_button.pack(padx = self.__button_padx, pady = 10, side = "left")
        #再生・一時停止ボタン
        self.__pause_button = tk.Button(self.__video_button_frame, text = "再生/一時停止", width = self.__button_width)
        self.__pause_button.bind("<ButtonPress-1>", self.videoStopOrStart)
        self.__pause_button.pack(padx = self.__button_padx, pady = 10, side = "left")
        #早送りボタン
        self.__fast_forward_button = tk.Button(self.__video_button_frame, text = "5秒送る", width = self.__button_width)
        self.__fast_forward_button.bind("<ButtonPress-1>", self.videoFastForward)
        self.__fast_forward_button.pack(padx = self.__button_padx, pady = 10, side = "left")


    def setVideoURL(self, event):
        self.__vc.downloader.download_url = self.__form.get()
        self.__vc.downloadVideo()

    def loadVideo(self):
        self.__vc.loadVideo()
        self.__video_title_text.set("".join([self.__vc.cv.video_title[j] for j in range(len(self.__vc.cv.video_title)) if ord(self.__vc.cv.video_title[j]) in range(65536)]))
        self.__audio_volume_text.set(self.__vc.audio.volume0to100())
        self.setCanvas()

    def videoStopOrStart(self, event):
        self.__vc.videoStopOrStart()
        if self.__vc.play_flag:
            self.dispImg()

    def videoRewind(self, event):
        self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * max(0, self.__vc.cv.cap.get(0) / 1000 - 5)))
        self.setCanvas()

    def videoFastForward(self, event):
        self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * min(self.__vc.cv.video_len, self.__vc.cv.cap.get(0) / 1000 + 5)))
        self.setCanvas()

    def setCanvas(self):
        self.__vc.fetchImg()
        if self.__vc.cv.ret == False:
            self.__vc.play_flag == False
            return
        self.__video_time_text.set("{0:0>2}:{1:0>2}:{2:0>2}/{3:0>2}:{4:0>2}:{5:0>2}".format(*self.__vc.cv.current_time.getTime(), *self.__vc.cv.whole_time.getTime()))
        self.__canvas.create_image(
            int(self.__vc.cv.disp_img_width / 2),
            int(self.__vc.cv.disp_img_height / 2),
            image = self.__vc.cv.canvas_img,
            tags = "image"
        )
        self.__canvas.tag_bind("image", "<ButtonPress-1>", self.videoStopOrStart)
        #canvas.tag_bind("image", "<ButtonPress-2>", self.videoRewind)
        self.__img_process_time = (time.time() - self.__vc.fetch_time) * 1000

    def dispImg(self):
        if self.__vc.play_flag:
            self.setCanvas()
            self.__root.after(int(1000 / self.__vc.cv.video_fps - self.__img_process_time), self.dispImg)

    def volumeDown(self, event):
        self.__vc.audio.setVolume(max(0.0, self.__vc.audio.volume - 0.05))
        self.__audio_volume_text.set(self.__vc.audio.volume0to100())

    def volumeUp(self, event):
        self.__vc.audio.setVolume(min(1.0, self.__vc.audio.volume + 0.05))
        self.__audio_volume_text.set(self.__vc.audio.volume0to100())

    def setVideoFile(self, event):
        self.__filetype = [("動画ファイル", ("*.mp4", "*.mov", "*.avi", "*.wmv", "*.flv"))]
        self.__dirpath = os.path.abspath(os.path.dirname(__file__))
        self.__vc.cv.video_path = filedialog.askopenfilename(filetypes = self.__filetype, initialdir = self.__dirpath)
        self.loadVideo()

    def setVideoQuality(self):
        self.__vc.downloader.video_format = str(self.__video_quality_value.get())

    def setAudioQuality(self):
        self.__vc.audio.frequency = self.__audio_quality_value.get()

    def scrollCanvas(self, event):
        self.__scroll_canvas.config(scrollregion = self.__scroll_canvas.bbox("all"), height = self.__window_height * 2)

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
