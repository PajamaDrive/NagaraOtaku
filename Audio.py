import subprocess
import ffmpeg
import pygame
import platform
from pydub.utils import mediainfo

class Audio:
    def __init__(self):
        self.__frequency = 44100
        self.__ar = "44.1k"
        self.__proc = None
        self.__volume = 1.0
        self.__pre_audio_pos = 0

    @property
    def volume(self):
        return self.__volume

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, rate):
        self.__frequency = rate
        if self.__frequency % 1000 == 0:
            self.__ar = self.__frequency // 1000
        else:
            self.__ar = self.__frequency / 1000
        self.__ar = str(self.__ar) + "k"

    @property
    def audio_title(self):
        return self.__audio_title

    @audio_title.setter
    def audio_title(self, title):
        self.__audio_title = title

    @property
    def audio_path(self):
        return self.__audio_path

    @audio_path.setter
    def audio_path(self, path):
        self.__audio_path = path

    @property
    def proc(self):
        return self.__proc

    def createMP3BackGround(self, cv):
        #self.__audio_title = cv.video_title + ".mp3"
        #self.__audio_path = cv.parent_directory + "/" + self.__audio_title
        #if not os.path.isfile(self.__audio_path):
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
        self.__proc = subprocess.Popen(self.__command)

    def createMP3ForeGround(self, cv):
        #self.__audio_title = cv.video_title + ".mp3"
        #self.__audio_path = cv.parent_directory + "/" + self.__audio_title
        #if not os.path.isfile(self.__audio_path):
        out, _ = (
            ffmpeg
            .input(cv.video_path)
            .output(self.__audio_path, acodec='mp3', ac=2, ar=self.__ar)
            .overwrite_output()
            .run(capture_stdout=True)
        )

    def initAudio(self):
        if not pygame.mixer.get_init() is None:
            pygame.mixer.quit()
        pygame.mixer.init(frequency = int(mediainfo(self.__audio_path)["sample_rate"]) // 2)
        pygame.mixer.music.load(self.__audio_path) #音源を読み込み
        pygame.mixer.music.set_volume(0.5)
        self.__volume = pygame.mixer.music.get_volume()

    def startAudio(self, second):
        pygame.mixer.music.play(loops = 0, start = second + 0.1)
        self.__pre_audio_pos = second * 1000

    def stopAudio(self):
        pygame.mixer.music.rewind()
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

    def getCurrentPos(self):
        return self.__pre_audio_pos + pygame.mixer.music.get_pos()

    def quitAudio(self):
        if not pygame.mixer.get_init() is None:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
