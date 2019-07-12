import tkinter as tk
from tkinter import font
from functions import getImg

class VideoFrame:
    def __init__(self, parent):
        self.__parent = parent
        self.__canvas = VideoCanvas(self.__parent)
        self.__button = VideoButton(self.__canvas.frame)

    @property
    def canvas(self):
        return self.__canvas

    @property
    def button(self):
        return self.__button

class VideoCanvas:
    def __init__(self, parent):
        self.__parent = parent
        self.__img_width = 800
        self.__img_height = 450
        self.__frame_padx = 20
        self.__frame_pady = 10
        self.__canvas_frame = tk.Frame(parent)
        self.__canvas_frame.pack()
        #動画関連の配置
        self.setCanvasParts()
        #テキストの配置
        self.setVideoTextParts()

    @property
    def width(self):
        return self.__img_width

    @property
    def height(self):
        return self.__img_height

    @property
    def seek_bar(self):
        return self.__video_seek_bar

    @property
    def volume_scale(self):
        return self.__audio_seek_bar

    @property
    def canvas(self):
        return self.__canvas

    @property
    def video_title(self):
        return self.__video_title_text

    @property
    def video_time(self):
        return self.__video_time_text

    @property
    def frame(self):
        return self.__canvas_frame

    def setCanvasParts(self):
        self.__canvas = tk.Canvas(
            self.__canvas_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__img_width,  # 幅を設定
            height = self.__img_height # 高さを設定
        )
        self.__canvas.pack()
        #シークバーの配置
        self.__video_current_pos = tk.DoubleVar()
        self.__video_seek_bar = tk.Scale(self.__canvas_frame, variable = self.__video_current_pos, orient = "horizontal", length = self.__img_width, from_ = 0, to = 1, showvalue = 0)
        self.__video_seek_bar.pack()

    def setVideoTextParts(self):
        self.__video_text_frame = tk.Frame(self.__canvas_frame)
        self.__video_text_frame.pack(pady = self.__frame_pady)
        #ビデオの時間
        self.__video_time_text = tk.StringVar()
        self.__video_time_font = font.Font(self.__video_text_frame, family = 'Helvetica', size = 20, weight = 'bold')
        self.__video_time_label = tk.Label(
            self.__video_text_frame,
            textvariable = self.__video_time_text,
            font = self.__video_time_font
        )
        self.__video_time_label.pack(side = "left", padx = self.__frame_padx)
        #音量表示
        self.__audio_text_frame = tk.Frame(self.__video_text_frame)
        self.__audio_text_frame.pack(side = "left", padx = self.__frame_padx)
        self.__audio_title_font = font.Font(self.__audio_text_frame, family = 'Helvetica', size = 20)
        self.__audio_title_label = tk.Label(self.__audio_text_frame, text = "音量", font = self.__audio_title_font)
        self.__audio_title_label.pack()
        #シークバーの配置
        self.__audio_current_pos = tk.DoubleVar()
        self.__audio_current_pos.set(10)
        self.__audio_seek_bar = tk.Scale(self.__audio_text_frame, variable = self.__audio_current_pos, orient = "horizontal", length = 100, from_ = 0, to = 20, showvalue = 0)
        self.__audio_seek_bar.pack()
        #ビデオのタイトル
        self.__video_title_text = tk.StringVar()
        self.__video_title_font = font.Font(self.__video_text_frame, family = 'Helvetica', size = 20)
        self.__video_title_label = tk.Label(
            self.__video_text_frame,
            textvariable = self.__video_title_text,
            font = self.__video_title_font,
            justify = "left"
        )
        self.__video_title_label.pack(side = "left", padx = self.__frame_padx)

class VideoButton:
    def __init__(self, parent):
        self.__parent = parent
        self.__button_width = 100
        self.__button_height = 60
        self.__button_padx = 20
        self.__button_pady = 20
        self.__frame_padx = 50
        self.__frame_pady = 20
        #動画操作ボタン関連の配置
        self.setVideoButtonParts()
        #音量調節ボタンの配置
        self.setAudioButtonParts()

    @property
    def volume_up_button(self):
        return self.__audio_volume_up_button

    @property
    def volume_down_button(self):
        return self.__audio_volume_down_button

    @property
    def rewind_button(self):
        return self.__rewind_button

    @property
    def pause_button(self):
        return self.__pause_button

    @property
    def fastforward_button(self):
        return self.__fast_forward_button

    def setVideoButtonParts(self):
        self.__video_button_frame = tk.Frame(self.__parent)
        self.__video_button_frame.pack(side = "left", padx = self.__frame_padx, pady = self.__frame_pady)
        #早戻しボタン
        self.__rewind_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__rewind_button.pack(padx = self.__button_padx, side = "left")
        self.__rewind_tkimg = getImg(self.__rewind_button, "config/fig/rewind.jpg", self.__button_width, self.__button_height)
        self.__rewind_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__rewind_tkimg,
            tags = "rewind"
        )
        self.__rewind_button.bind("<Enter>", self.rewindHover)
        self.__rewind_button.bind("<Leave>", self.rewindUnhover)
        #再生・一時停止ボタン
        self.__pause_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__pause_button.pack(padx = self.__button_padx, side = "left")
        self.__pause_tkimg = getImg(self.__pause_button, "config/fig/start.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )
        self.__pause_button.bind("<Enter>", self.startHover)
        self.__pause_button.bind("<Leave>", self.startUnhover)
        #早送りボタン
        self.__fast_forward_button = tk.Canvas(
            self.__video_button_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__fast_forward_button.pack(padx = self.__button_padx, side = "left")
        self.__fast_forward_tkimg = getImg(self.__fast_forward_button, "config/fig/fastforward.jpg", self.__button_width, self.__button_height)
        self.__fast_forward_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__fast_forward_tkimg,
            tags = "fastforward"
        )
        self.__fast_forward_button.bind("<Enter>", self.fastforwardHover)
        self.__fast_forward_button.bind("<Leave>", self.fastforwardUnhover)

    def setAudioButtonParts(self):
        #音量に関するオブジェクトの配置
        self.__audio_button_frame = tk.Frame(self.__parent)
        self.__audio_button_frame.pack(side = "left", padx = self.__frame_padx, pady = self.__frame_pady)
        #音量を下げるボタン
        self.__audio_volume_down_button = tk.Canvas(
            self.__audio_button_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__audio_volume_down_button.pack(padx = self.__button_padx, side = "left")
        self.__audio_volume_down_tkimg = getImg(self.__audio_volume_down_button, "config/Fig/volume_down.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_down_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_down_tkimg,
            tags = "volume_down"
        )
        self.__audio_volume_down_button.bind("<Enter>", self.volumeDownHover)
        self.__audio_volume_down_button.bind("<Leave>", self.volumeDownUnhover)
        #音量を上げるボタン
        self.__audio_volume_up_button = tk.Canvas(
            self.__audio_button_frame, # 親要素をメインウィンドウに設定
            highlightthickness = 0,
            width = self.__button_width,  # 幅を設定
            height = self.__button_height # 高さを設定
        )
        self.__audio_volume_up_button.pack(padx = self.__button_padx, side = "left")
        self.__audio_volume_up_tkimg = getImg(self.__audio_volume_up_button, "config/fig/volume_up.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_up_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_up_tkimg,
            tags = "volume_up"
        )
        self.__audio_volume_up_button.bind("<Enter>", self.volumeUpHover)
        self.__audio_volume_up_button.bind("<Leave>", self.volumeUpUnhover)

    def invertPauseAndStop(self, img_path):
        self.__pause_tkimg = getImg(self.__pause_button, img_path, self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )
        if "start.jpg" in img_path:
            self.__pause_button.bind("<Enter>", self.startHover)
            self.__pause_button.bind("<Leave>", self.startUnhover)
        else:
            self.__pause_button.bind("<Enter>", self.pauseHover)
            self.__pause_button.bind("<Leave>", self.pauseUnhover)

    def rewindHover(self, event):
        self.__rewind_tkimg = getImg(self.__rewind_button, "config/fig/rewind_hover.jpg", self.__button_width, self.__button_height)
        self.__rewind_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__rewind_tkimg,
            tags = "rewind"
        )

    def rewindUnhover(self, event):
        self.__rewind_tkimg = getImg(self.__rewind_button, "config/fig/rewind.jpg", self.__button_width, self.__button_height)
        self.__rewind_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__rewind_tkimg,
            tags = "rewind"
        )

    def startHover(self, event):
        self.__pause_tkimg = getImg(self.__pause_button, "config/fig/start_hover.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )

    def startUnhover(self, event):
        self.__pause_tkimg = getImg(self.__pause_button, "config/fig/start.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )

    def pauseHover(self, event):
        self.__pause_tkimg = getImg(self.__pause_button, "config/fig/pause_hover.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )

    def pauseUnhover(self, event):
        self.__pause_tkimg = getImg(self.__pause_button, "config/fig/pause.jpg", self.__button_width, self.__button_height)
        self.__pause_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__pause_tkimg,
            tags = "pause"
        )

    def fastforwardHover(self, event):
        self.__fast_forward_tkimg = getImg(self.__fast_forward_button, "config/fig/fastforward_hover.jpg", self.__button_width, self.__button_height)
        self.__fast_forward_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__fast_forward_tkimg,
            tags = "fastforward"
        )

    def fastforwardUnhover(self, event):
        self.__fast_forward_tkimg = getImg(self.__fast_forward_button, "config/fig/fastforward.jpg", self.__button_width, self.__button_height)
        self.__fast_forward_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__fast_forward_tkimg,
            tags = "fastforward"
        )

    def volumeDownHover(self, event):
        self.__audio_volume_down_tkimg = getImg(self.__audio_volume_down_button, "config/fig/volume_down_hover.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_down_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_down_tkimg,
            tags = "volume_down"
        )

    def volumeDownUnhover(self, event):
        self.__audio_volume_down_tkimg = getImg(self.__audio_volume_down_button, "config/fig/volume_down.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_down_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_down_tkimg,
            tags = "volume_down"
        )

    def volumeUpHover(self, event):
        self.__audio_volume_up_tkimg = getImg(self.__audio_volume_up_button, "config/fig/volume_up_hover.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_up_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_up_tkimg,
            tags = "volume_up"
        )

    def volumeUpUnhover(self, event):
        self.__audio_volume_up_tkimg = getImg(self.__audio_volume_up_button, "config/fig/volume_up.jpg", self.__button_width, self.__button_height)
        self.__audio_volume_up_button.create_image(
            int(self.__button_width / 2),
            int(self.__button_height / 2),
            image = self.__audio_volume_up_tkimg,
            tags = "volume_up"
        )
