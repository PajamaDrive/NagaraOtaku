import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import CV
import pathlib
import os
import platform
import VideoController as vc
import threading
import shutil
import zipfile
import re
import sys
import subprocess
import importlib
import IconWindow
import TitleBar
import ScrollCanvas
import ControlPanel
import StatusFrame
import VideoFrame
from functions import getQuality, resource_path

class NagaraOtaku:
    def __init__(self):
        self.__window_width = 900
        self.__window_height = 400
        self.__os_toolbar_height = 20
        self.__user_process_time = 0
        self.__cycle = 5
        self.__first_time_flag = True
        self.__is_on = True
        self.__train_process = None
        self.__create_train_process = None
        self.__load_thread = None
        self.__detect_thread = None
        self.__button_available = True
        self.__detect_num = 0
        self.__img_process_time = None
        self.__img_disp_num = 0
        self.__MAX_DETECT_NUM = 3
        self.__ADJUST_SEC = 5
        self.__LINE_CHAR_NUM = 25
        self.__visible = True
        self.__maximize = False
        self.__minimize_window = None
        self.__vc = vc.VideoController()
        self.__train_cv = CV.CV()
        self.__current_path = pathlib.Path(sys.argv[0])
        self.__dirpath = pathlib.Path(__file__).parent if self.__current_path.suffix == ".py" else self.__current_path.parent
        #Tkinterの初期設定
        self.__root = tk.Tk()
        self.__root.title("NagaraOtaku")
        #タイトルバーの削除など
        self.__root.overrideredirect(True)
        self.__root.overrideredirect(False)
        self.__root.resizable(width = 1, height = 1)
        self.__root.geometry(str(self.__window_width) + "x" + str(self.__window_height))
        #タイトルバーの作成
        if platform.system() == "Darwin":
             self.__title_bar = TitleBar.TitleBar(self.__root)
        #本体部分のフレーム
        self.__root_frame = tk.Frame(self.__root)
        self.__root_frame.pack(fill = "both")
        self.__root_frame.grid_rowconfigure(0, weight = 1)
        self.__root_frame.grid_columnconfigure(0, weight = 1)
        #スクロール可能な領域の作成
        self.__scroll_canvas = ScrollCanvas.ScrollCanvas(self.__root_frame, self.__window_width, self.__window_height)
        #コントロールパネルの作成
        self.__control_panel = ControlPanel.ControlPanel(self.__scroll_canvas.frame)
        #ステータス表示領域の作成
        self.__status_frame = StatusFrame.StatusFrame(self.__scroll_canvas.frame)
        #関数をバインド
        self.bindFixFrameFunction()

    @property
    def root(self):
        return self.__root

#パーツの配置
    def bindFixFrameFunction(self):
        #タイトルバー関連
        if platform.system() == "Darwin":
            self.__title_bar.bar.bind("<Button-1>", self.startMove)
            self.__title_bar.bar.bind("<ButtonRelease-1>", self.stopMove)
            self.__title_bar.bar.bind("<B1-Motion>", self.windowMoving)
            self.__title_bar.delete.tag_bind("delete", "<ButtonPress-1>", self.closeWindow)
            self.__title_bar.minimize.tag_bind("minimize", "<ButtonPress-1>", self.minimizeWindow)
            self.__title_bar.maximize.tag_bind("maximize", "<ButtonPress-1>", self.maximizeWindow)
        #スクロールバー関連
        self.__scroll_canvas.scrollbar_x.bind("<ButtonPress-1>", self.onScrolling)
        self.__scroll_canvas.scrollbar_y.bind("<ButtonPress-1>", self.onScrolling)
        self.__scroll_canvas.resize_canvas.bind("<B1-Motion>", self.setWindowSize)
        self.__scroll_canvas.resize_canvas.bind("<ButtonRelease-1>", self.resizeWindow)
        #コントロールパネル関連
        self.__control_panel.download_button.tag_bind("download", "<ButtonPress-1>", self.setVideoURL)
        self.__control_panel.select_button.tag_bind("select", "<ButtonPress-1>", self.setVideoFile)
        self.__control_panel.onoff_button.tag_bind("train_test", "<ButtonPress-1>", self.turnTrainTest)
        self.__control_panel.initialize_button.tag_bind("initialize", "<ButtonPress-1>", self.initializeCharacter)

    def bindVideoFrameFunction(self):
        self.__video.canvas.canvas.bind("<ButtonPress-1>", self.videoStopOrStart)
        self.__video.canvas.seek_bar.bind("<B1-Motion>", self.seekPos)
        self.__video.canvas.volume_scale.bind("<B1-Motion>", self.volumePos)
        self.__video.button.rewind_button.tag_bind("rewind", "<ButtonPress-1>", self.videoRewind)
        self.__video.button.pause_button.tag_bind("pause", "<ButtonPress-1>", self.videoStopOrStart)
        self.__video.button.fastforward_button.tag_bind("fastforward", "<ButtonPress-1>", self.videoFastForward)
        self.__video.button.volume_down_button.tag_bind("volume_down", "<ButtonPress-1>", self.volumeDown)
        self.__video.button.volume_up_button.tag_bind("volume_up", "<ButtonPress-1>", self.volumeUp)

    def setCanvasParts(self):
        self.__first_time_flag = False
        self.__video = VideoFrame.VideoFrame(self.__scroll_canvas.frame)
        self.__vc.cv.setImgSize(self.__video.canvas.width, self.__video.canvas.height)
        self.bindVideoFrameFunction()
#タイトルバー関連のバインド
    def closeWindow(self, event):
        if not self.__first_time_flag:
            if self.__vc.play_flag:
                self.videoStopOrStart(None)
                self.deniedPlayVideo()

        if not self.__vc.cv.cap is None:
            self.__vc.deniedPlayVideo()
            self.__vc.cv.quitVideo()
        self.__vc.audio.quitAudio()
        if not self.__minimize_window is None:
            self.__minimize_window.window.destroy()
        self.__root.destroy()

    def minimizeWindow(self, event):
        self.__root.state("withdrawn")
        self.__visible = False
        self.__minimize_window = IconWindow.IconWindow()
        th = threading.Thread(target = self.windowThread)
        th.setDaemon(True)
        th.start()
        self.__minimize_window.window.mainloop()

    def windowThread(self):
        self.__minimize_window.window.iconify()
        self.__minimize_window.window.bind("<Map>", self.windowMap)
        self.__minimize_window.window.protocol("WM_DELETE_WINDOW", self.miniWindowDestroy)

    def windowMap(self, event):
        self.__visible = True
        self.__root.state("normal")
        self.__minimize_window.window.destroy()
        self.__minimize_window = None

    def miniWindowDestroy(self):
        self.__minimize_window.window.destroy()
        if not self.__visible:
            self.closeWindow(None)

    def maximizeWindow(self, event):
        w, h = (0, 0)
        if self.__maximize:
            w, h = self.__window_width, self.__window_height
        else:
            w, h = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__root.geometry("%dx%d+0+%d" % (w, h, self.__os_toolbar_height))
        self.__maximize = not self.__maximize

    def startMove(self, event):
        self.__x = event.x
        self.__y = event.y

    def stopMove(self, event):
        self.__x = None
        self.__y = None

    def windowMoving(self,event):
        x = (event.x_root - self.__x)
        y = max((event.y_root - self.__y), self.__os_toolbar_height)
        self.__root.geometry("+%s+%s" % (x, y))
#スクロールのバインド
    def onScrolling(self, event):
        if not self.__first_time_flag:
            if self.__vc.play_flag:
                self.videoStopOrStart(None)
                self.deniedPlayVideo()
#リサイズのバインド
    def resizeWindow(self, event):
        self.__root.geometry(str(self.__window_width) + "x" + str(self.__window_height))

    def setWindowSize(self, event):
        self.__window_width = max(400, event.x_root)
        self.__window_height = max(300, event.y_root)
#コントロールパネル関連のバインド
    def setVideoURL(self, event):
        if len(self.__control_panel.form.get()) != 0:
            self.__vc.downloader.video_format = self.__control_panel.video_quality_value
            self.__vc.downloader.download_url = self.__control_panel.form.get()
            self.__vc.downloadVideo(str(self.__dirpath))
            if self.__vc.downloader.is_error == True:
                messagebox.showerror("エラー", "このURLは有効ではありません")
            elif self.__vc.downloader.downloadable == False:
                messagebox.showerror("エラー", "この動画の画質は" + ",".join(getQuality(self.__vc.downloader.quality_list)) + "しか選択できません")
            else:
                self.changeStatus("Download")
        else:
            messagebox.showerror("エラー", "URLを入力してください")

    def setVideoFile(self, event):
        self.__filetype = [("動画ファイル", ("*.mp4", "*.mov", "*.avi", "*.wmv", "*.flv"))]
        video_path = filedialog.askopenfilename(filetypes = self.__filetype, initialdir = self.__dirpath)
        if video_path:
            if self.__control_panel.is_train.get():
                self.__train_cv.video_path = video_path
            else:
                self.__vc.cv.video_path = video_path
            self.loadVideo()

    def turnTrainTest(self, event):
        self.__is_on = not self.__is_on
        if self.__is_on:
            self.__control_panel.changeButtonImg("config/fig/on.jpg")
            if self.__vc.play_flag:
                self.setDetectTimer()
        else:
            self.__control_panel.changeButtonImg("config/fig/off.jpg")

    def initializeCharacter(self, event):
        ret = messagebox.askyesno("確認", "識別器を初期化しますか?")
        if ret == True:
            classifier_path = pathlib.Path(resource_path(str(self.__dirpath) + "/config/classifier.xml"))
            if classifier_path.exists():
                classifier_path.unlink()
            character_path = pathlib.Path(resource_path(str(self.__dirpath) + "/config/characters.txt"))
            if character_path.exists():
                character_path.unlink()
            if pathlib.Path(resource_path(str(self.__dirpath) + "/tmp/train")).exists():
                shutil.rmtree(resource_path(str(self.__dirpath) + "/tmp/train"))
        self.__control_panel.updateCharacterList()

#ビデオフレーム関連のバインド
    def seekPos(self, *args):
        if self.__button_available:
            self.deniedPlayVideo()
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * self.__video.canvas.seek_bar.get()))
            self.setCanvas()

    def volumePos(self, *args):
        if self.__button_available:
            self.__vc.audio.setVolume(self.__video.canvas.volume_scale.get() * 0.05)

    def videoRewind(self, event):
        if self.__button_available:
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * max(0, self.__vc.cv.cap.get(0) / 1000 - 5)))
            self.setCanvas()

    def videoStopOrStart(self, event):
        if self.__button_available:
            self.__vc.videoStopOrStart()
            if self.__vc.play_flag:
                self.dispImg()
                self.__video.button.invertPauseAndStop("config/fig/pause.jpg")
                if self.__is_on:
                    self.setDetectTimer()
            else:
                self.__video.button.invertPauseAndStop("config/fig/start.jpg")
                self.__img_process_time = None

    def videoFastForward(self, event):
        if self.__button_available:
            self.__vc.setVideoPosition(int(self.__vc.cv.video_fps * min(self.__vc.cv.video_len, self.__vc.cv.cap.get(0) / 1000 + 5)))
            self.setCanvas()

    def volumeDown(self, event):
        if self.__button_available:
            self.__vc.audio.setVolume(max(0.0, self.__vc.audio.volume - 0.05))
            self.__video.canvas.volume_scale.set(max(0, self.__video.canvas.volume_scale.get() - 1))

    def volumeUp(self, event):
        if self.__button_available:
            self.__vc.audio.setVolume(min(1.0, self.__vc.audio.volume + 0.05))
            self.__video.canvas.volume_scale.set(min(20, self.__video.canvas.volume_scale.get() + 1))

#描画関連
    def loadVideo(self):
        if self.__control_panel.is_train.get():
            self.__train_cv.loadVideo()
        else:
            self.__vc.loadVideo()
        if self.__first_time_flag == False:
            self.__video.button.invertPauseAndStop("config/fig/start.jpg")
        if self.__control_panel.is_train.get() == True:
            ret = messagebox.askyesno("確認", "訓練中にこの動画を閲覧しますか?")
            while not self.__control_panel.character_name:
                    self.__control_panel.character_name = simpledialog.askstring("新規入力", "キャラクター名を入力してください(英字)")
                    if self.__control_panel.character_name is None:
                        break
            if self.__control_panel.character_name:
                if ret == True:
                    self.__vc.cv.video_path = self.__train_cv.video_path
                    self.__vc.loadVideo()
                    if not pathlib.Path(self.__vc.audio.audio_path).exists():
                        self.__vc.audio.frequency = self.__control_panel.audio_quality_value
                        messagebox.showinfo("確認", "サンプリング周波数" + str(self.__vc.audio.frequency) + "Hzでmp3ファイルを生成します")
                        self.__vc.audio.createMP3BackGround(self.__vc.cv)
                        self.changeStatus("MP3")
                    else:
                        if self.__first_time_flag == True:
                            self.setCanvasParts()
                        self.prepareVideo()

                #別スレッドで訓練開始
                jpg_list = []
                if pathlib.Path(resource_path(str(self.__dirpath) + "/tmp/train/" + self.__control_panel.character_name + ".zip")).exists():
                    with zipfile.ZipFile(resource_path(str(self.__dirpath) + "/tmp/train/" + self.__control_panel.character_name + ".zip"), "r") as train_zip:
                        jpg_list = [path for path in train_zip.namelist() if self.__train_cv.video_title in path]
                if len(jpg_list) == 0:
                    self.__create_train_process = subprocess.Popen(("python", resource_path("lib/create_train_data.py"), self.__train_cv.video_path, self.__control_panel.character_name, self.__dirpath))
                    time.sleep(0.5)
                    self.changeStatus("CreateData")
                else:
                    if self.__is_on:
                        self.__train_process = subprocess.Popen(("python", resource_path("lib/train.py"), self.__dirpath))
                        self.changeStatus("Train")
                if len(self.__control_panel.character_list.curselection()) == 0 or self.__control_panel.character_list.curselection()[0] == 0:
                    self.__control_panel.character_name = ""
                self.__control_panel.updateCharacterList()

        else:
            if not pathlib.Path(self.__vc.audio.audio_path).exists():
                self.__vc.audio.frequency = self.__control_panel.audio_quality_value
                messagebox.showinfo("確認", "サンプリング周波数" + str(self.__vc.audio.frequency) + "Hzでmp3ファイルを生成します")
                self.__vc.audio.createMP3BackGround(self.__vc.cv)
                self.changeStatus("MP3")
            else:
                if self.__first_time_flag == True:
                    self.setCanvasParts()
                self.prepareVideo()
            if self.__vc.cv.classifier is None and pathlib.Path(resource_path(str(self.__dirpath) + "/config/classifier.xml")).exists():
                self.__load_thread = threading.Thread(target = self.__vc.cv.loadClassifier, args = (str(self.__dirpath), ))
                self.__load_thread.setDaemon(True)
                self.__load_thread.start()
                self.changeStatus("Load")

    def prepareVideo(self):
        self.__vc.audio.initAudio()
        #ここで　cvの幅を決定
        self.__vc.cv.disp_img_width
        title = list(re.sub("_[0-9]{3,4}p\Z", "", "".join([self.__vc.cv.video_title[j] for j in range(len(self.__vc.cv.video_title)) if ord(self.__vc.cv.video_title[j]) in range(65536)])))
        if len(title) > self.__LINE_CHAR_NUM:
            i = 0
            while i < (len(title) + int(len(title) / self.__LINE_CHAR_NUM)):
                if i != 0 and i % self.__LINE_CHAR_NUM == 0:
                    title.insert(i, os.linesep)
                    i += 1
                i += 1
        self.__video.canvas.video_title.set("".join(title))
        self.__video.canvas.seek_bar.config(to = self.__vc.cv.whole_time.getWholeSecond())
        self.setCanvas()

    def setCanvas(self):
        self.__vc.fetchImg()
        self.__video.canvas.seek_bar.set(int(self.__vc.cv.cap.get(0) / 1000))
        if self.__vc.cv.ret == False:
            self.__vc.play_flag == False
            return
        self.__video.canvas.video_time.set("{0:0>2}:{1:0>2}:{2:0>2} / {3:0>2}:{4:0>2}:{5:0>2}".format(*self.__vc.cv.current_time.getTime(), *self.__vc.cv.whole_time.getTime()))
        self.__video.canvas.canvas.create_image(
            int(self.__vc.cv.disp_img_width / 2),
            int(self.__vc.cv.disp_img_height / 2),
            image = self.__vc.cv.canvas_img,
            tags = "image"
        )

    def dispImg(self):
        self.__img_process_time = time.time()
        if self.__vc.play_flag:
            self.__img_disp_num  = (self.__img_disp_num + 1) % (self.__ADJUST_SEC * int(self.__vc.cv.video_fps))
            self.setCanvas()
            if self.__img_disp_num == 0:
                self.__vc.adjustVideoAndAudio()
            self.__root.after(max(1, int((1 / self.__vc.cv.video_fps - (time.time() - self.__img_process_time)) * 1000)), self.dispImg)

    def deniedPlayVideo(self):
        self.__vc.deniedPlayVideo()
        if not self.__first_time_flag:
            self.__video.button.invertPauseAndStop("config/fig/start.jpg")

#ステータス関連
    def changeStatus(self, status):
        self.__status_frame.changeStatus(status)
        time.sleep(0.5)
        if status in self.__status_frame.getStatus():
            if status in self.__status_frame.getDeniedStatus():
                self.__button_available = False
                self.deniedPlayVideo()
            self.startWatchThread(status)

    def startWatchThread(self, status):
        func_name = "self.watch" + status
        th = threading.Thread(target = eval(func_name))
        th.setDaemon(True)
        th.start()

    def watchTrain(self):
        if not self.__train_process is None and self.__train_process.poll() is None:
            th = threading.Timer(1, self.watchTrain)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("Train")
            self.__load_thread = threading.Thread(target = self.__vc.cv.loadClassifier, args = (str(self.__dirpath), ))
            self.__load_thread.setDaemon(True)
            self.__load_thread.start()
            self.changeStatus("Load")

    def watchDownload(self):
        if not self.__vc.downloader.proc is None and self.__vc.downloader.proc.poll() is None:
            th = threading.Timer(1, self.watchDownload)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("Download")

    def watchMP3(self):
        if not self.__vc.audio.proc is None and self.__vc.audio.proc.poll() is None:
            th = threading.Timer(1, self.watchMP3)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("MP3")
            if self.__first_time_flag == True:
                self.setCanvasParts()
            self.prepareVideo()
            self.__button_available = True

    def watchLoad(self):
        if not self.__load_thread is None and self.__load_thread.is_alive():
            th = threading.Timer(1, self.watchLoad)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("Load")
            self.__control_panel.is_train.set(0)
            self.__control_panel.changeTrainTestImg()
            self.__is_on = True
            self.__control_panel.changeButtonImg("config/fig/on.jpg")
            self.setDetectTimer()

    def watchCreateData(self):
        if not self.__create_train_process is None and self.__create_train_process.poll() is None:
            th = threading.Timer(1, self.watchCreateData)
            th.setDaemon(True)
            th.start()
        else:
            self.changeStatus("CreateData")
            if self.__is_on:
                self.__train_process = subprocess.Popen(("python", resource_path("lib/train.py"), self.__dirpath))
                self.changeStatus("Train")

#顔認識関連
    def setDetectTimer(self):
        if self.__is_on and not self.__control_panel.is_train.get():
            if not self.__vc.cv.classifier is None and (self.__load_thread is None or not self.__load_thread.is_alive()):
                if self.__detect_thread is None or not self.__detect_thread.is_alive():
                    self.__cycle = self.__control_panel.interval
                    self.__detect_num = 0
                    self.__detect_thread = threading.Timer(self.__cycle, self.detectTimer)
                    self.__detect_thread.setDaemon(True)
                    self.__detect_thread.start()

    def detectTimer(self):
        if self.__load_thread is None or not self.__load_thread.is_alive():
            #検出できた時の処理
            if self.__vc.cv.character_names != [] and self.__vc.cv.confidenceds != []:
                self.noticeDetection()
            if self.__detect_num <= self.__MAX_DETECT_NUM:
                if self.__vc.play_flag:
                    th = threading.Thread(target = self.__vc.cv.detectCharacter, args = (str(self.__dirpath),))
                    th.setDaemon(True)
                    th.start()
                if self.__is_on and not self.__control_panel.is_train.get():
                    self.__cycle = self.__control_panel.interval
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
            notify_module = importlib.import_module("plyer")
            for i in range(len(self.__vc.cv.character_names)):
                notify_module.notification.notify(title = "Detect notification", message = self.__vc.cv.character_names[i] + " detect", app_name = "NagaraOtaku")
            self.__detect_num += 1
        self.__vc.cv.clearList()
        if self.__detect_num >= self.__MAX_DETECT_NUM:
            self.turnTrainTest(None)
            self.__detect_num = 0

if __name__ == "__main__":
    no_gui = NagaraOtaku()
    no_gui.root.mainloop()
