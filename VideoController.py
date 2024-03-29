import CV
import Audio
import YoutubeDownloader as yd
import time
import pathlib
import re
import sys

class VideoController:
    def __init__(self):
        self.__cv = CV.CV()
        self.__audio = Audio.Audio()
        self.__downloader = yd.YoutubeDownloader()
        self.__play_flag = False

    @property
    def cv(self):
        return self.__cv

    @property
    def downloader(self):
        return self.__downloader

    @property
    def play_flag(self):
        return self.__play_flag

    @property
    def audio(self):
        return self.__audio

    def loadVideo(self):
        self.__cv.loadVideo()
        self.__audio.audio_title = str(re.sub("_[0-9]{3,4}p$", "", self.__cv.video_title)) + ".mp3"
        current_path = pathlib.Path(sys.argv[0])
        dirpath = pathlib.Path(__file__).parent if current_path.suffix == ".py" else current_path.parent
        audio_path = pathlib.Path(str(dirpath) + "/audio")
        if not audio_path.exists():
            audio_path.mkdir()
        self.__audio.audio_path = str(audio_path) + "/" + self.__audio.audio_title
        self.__play_flag = False

    def deniedPlayVideo(self):
        self.__play_flag = False

    def videoStopOrStart(self):
        self.__play_flag = not self.__play_flag
        if self.__play_flag:
            self.__audio.startAudio(self.__cv.cap.get(0) / 1000)
        else:
            self.__audio.stopAudio()

    def setVideoPosition(self, frame_pos):
        self.__cv.cap.set(1, frame_pos)
        self.__audio.stopAudio()
        if self.__play_flag:
            self.__audio.startAudio(frame_pos / self.__cv.video_fps)

    def fetchImg(self):
        self.__cv.getFrameImage()
        #動画の秒数の表示
        self.__cv.current_time.setTime(int(self.__cv.cap.get(1) / self.__cv.video_fps))

    def downloadVideo(self, dir_path):
        self.__downloader.downloadVideo(dir_path)

    def adjustVideoAndAudio(self):
        self.__cv.cap.set(1, int(self.__cv.video_fps * self.__audio.getCurrentPos() / 1000))
