import VideoTime as vt
import os
import cv2
from PIL import Image, ImageTk
from create_train_data import addCharacter, createData
from train import trainCharacter

class CV:
    def __init__(self, video_path = None):
        self.__disp_img_width = 800
        self.__disp_img_height = 450
        self.__current_time = vt.VideoTime()
        self.__whole_time = vt.VideoTime()
        self.__video_path = video_path if video_path else ""
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

    def trainData(self, character):
        addCharacter(character)
        createData(self.__video_path, character)
        trainCharacter(character)
