import tkinter as tk
import tkinter.font as font
import os
import cv2
import re
import ffmpeg
import pygame
import random
import time
import youtube_dl
from PIL import Image, ImageTk

class Audio:
    def __init__(self):
        self.__frequency = 44100
        if self.__frequency % 1000 == 0:
            self.__ar = self.__frequency // 1000
        else:
            self.__ar = self.__frequency / 1000
        self.__ar = str(self.__ar) + "k"

    def createMP3(self, cv):
        self.__audio_title = cv.video_title + ".mp3"
        self.__audio_path = cv.work_directory + "/" + self.__audio_title
        if not os.path.isfile(self.__audio_path):
            out, _ = (
                ffmpeg
                .input(cv.in_video_path)
                .output(self.__audio_path, acodec='mp3', ac=2, ar=self.__ar)
                .overwrite_output()
                .run(capture_stdout=True)
            )

    def initAudio(self):
        pygame.mixer.init(frequency = self.__frequency // 2)
        pygame.mixer.music.load(self.__audio_path) #音源を読み込み

    def startAudio(self, second):
        pygame.mixer.music.play(loops = 0, start = second)

    def stopAudio(self):
        pygame.mixer.music.stop()

    def pauseAudio(self):
        pygame.mixer.music.pause()

    def unpauseAudio(self):
        pygame.mixer.music.unpause()

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
        self.__video_title = ""
        self.__work_directory = "../video/NagaraOtaku"

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
    def work_directory(self):
        return self.__work_directory

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

    def loadVideo(self, video_name):
        #動画のパス
        self.__in_video_path = self.__work_directory + "/" + video_name
        if not os.path.isfile(self.__in_video_path):
            print("ファイルが開けません")
        self.__cap = cv2.VideoCapture(self.__in_video_path)
        self.__video_frame = self.__cap.get(cv2.CAP_PROP_FRAME_COUNT) # フレーム数を取得する
        self.__video_fps = self.__cap.get(cv2.CAP_PROP_FPS)           # FPS を取得する
        self.__video_len = self.__video_frame // self.__video_fps
        self.__whole_time.setTime(self.__video_len)
        self.__video_title = re.sub("\..+$", "", video_name, count = 1)

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

    @property
    def download_url(self):
        return self.__download_url

    @download_url.setter
    def download_url(self, url):
        self.__download_url = url

    def downloadVideo(self):
        return


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

    def loadNewVideo(self, video_name):
        self.__cv.loadVideo(video_name)
        self.__audio.createMP3(self.__cv)
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

class GUI:
    def __init__(self):
        self.__window_width = 1200
        self.__window_height = 800
        self.__button_width = 10
        self.__vc = VideoController()
        self.__root = tk.Tk()
        #Tkinterの初期設定
        self.__root.title("NagaraOtaku")
        self.__root.geometry(str(self.__window_width) + "x" + str(self.__window_height))
        self.__root.resizable(width = 1, height = 1)

        #動画URLのフォーム
        self.__form_frame = tk.LabelFrame(self.__root, padx = 15, pady = 15, bd = 2, text = "動画のURLを入力")
        self.__form_frame.pack(pady = 10)
        self.__form = tk.Entry(self.__form_frame, width = 50)
        self.__form.pack(side = "left")
        #動画ダウンロードのボタン
        self.__form_button = tk.Button(self.__form_frame, text = "ダウンロード", width = self.__button_width)
        self.__form_button.bind("<ButtonPress-1>", self.setVideoURL)
        self.__form_button.pack(side = "left")
        #動画関連の配置
        #キャンバス(動画描画部分)の設定
        self.__canvas_frame = tk.Frame(self.__root)
        self.__canvas_frame.pack()
        self.__canvas = tk.Canvas(
            self.__canvas_frame, # 親要素をメインウィンドウに設定
            width = self.__vc.cv.disp_img_width,  # 幅を設定
            height = self.__vc.cv.disp_img_height # 高さを設定
        )
        self.__canvas.pack()
        #self.canvas.place(relx = self.canvas_relx, relwidth = self.canvas_relwidth,  rely = self.canvas_rely, relheight = self.canvas_relheight)
        #ビデオのタイトル
        self.__video_title_text = tk.StringVar()
        self.__video_title_font = font.Font(self.__canvas_frame, family='Helvetica', size=20, weight='bold')
        self.__video_title_label = tk.Label(
            self.__canvas_frame,
            textvariable = self.__video_title_text,
            font = self.__video_title_font
        )
        self.__video_title_label.pack()
        #ビデオの時間
        self.__video_time_text = tk.StringVar()
        self.__video_time_label = tk.Label(
            self.__canvas_frame,
            textvariable = self.__video_time_text
        )
        self.__video_time_label.pack()
        #動画操作ボタン関連の配置
        #早戻しボタン
        self.__video_button_frame = tk.Frame(self.__root)
        self.__video_button_frame.pack()
        self.__rewind_button = tk.Button(self.__video_button_frame, text = "5秒戻す", width = self.__button_width)
        self.__rewind_button.bind("<ButtonPress-1>", self.videoRewind)
        self.__rewind_button.pack(padx = 20, pady = 10, side = "left")
        #再生・一時停止ボタン
        self.__pause_button = tk.Button(self.__video_button_frame, text = "再生/一時停止", width = self.__button_width)
        self.__pause_button.bind("<ButtonPress-1>", self.videoStopOrStart)
        self.__pause_button.pack(padx = 20, pady = 10, side = "left")
        #早送りボタン
        self.__fast_forward_button = tk.Button(self.__video_button_frame, text = "5秒送る", width = self.__button_width)
        self.__fast_forward_button.bind("<ButtonPress-1>", self.videoFastForward)
        self.__fast_forward_button.pack(padx = 20, pady = 10, side = "left")
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

    def setVideoURL(self, event):
        self.__vc.downloader.download_url = self.__form.get()
        self.__vc.downloader.downloadVideo()

    def loadNewVideo(self, video_name):
        self.__vc.loadNewVideo(video_name)
        self.__video_title_text.set(self.__vc.cv.video_title)
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
        self.__process_time = (time.time() - self.__vc.fetch_time) * 1000

    def dispImg(self):
        if self.__vc.play_flag:
            self.setCanvas()
            self.__root.after(int(1000 / self.__vc.cv.video_fps - self.__process_time), self.dispImg)


if __name__ == "__main__":
    gui = GUI()
    gui.loadNewVideo("tsukino_intro.mov")
    gui.root.mainloop()
