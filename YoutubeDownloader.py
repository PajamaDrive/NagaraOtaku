import subprocess
import re
import pathlib

class YoutubeDownloader:
    def __init__(self):
        self.__download_url = ""
        #1080p:137, 720p:136, 480p:135, 360p:134, 240p:133, 144p:160
        self.__video_format = "136"
        self.__audio_format = "140"
        self.__download_format = "mp4"
        self.__download_flag = True
        self.__proc = None

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

    @property
    def quality_list(self):
        return self.__quality_list

    @property
    def downloadable(self):
        return self.__downloadable

    @property
    def is_error(self):
        return self.__is_error

    @property
    def proc(self):
        return self.__proc

    def downloadVideo(self):
        self.__confirm_command = (
            "youtube-dl",
            self.__download_url,
            "--list-format"
        )
        proc = subprocess.Popen(self.__confirm_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        res = proc.stdout.read().decode()
        self.__quality_list = re.findall("^137|^136|^135|^134|^133|^160", res, re.MULTILINE)
        if self.__video_format in self.__quality_list:
            self.__downloadable = True
            self.__is_error = False
            path = pathlib.Path("video")
            if not path.exists():
                path.mkdir()
            self.__dl_command = (
                "youtube-dl",
                "--format",
                self.__video_format + "+" + self.__audio_format,
                "--merge-output-format",
                self.__download_format,
                "--output",
                "video/%(title)s_%(height)sp.%(ext)s",
                self.__download_url
            )
            self.__proc = subprocess.Popen(self.__dl_command)
        else:
            self.__downloadable = False
            if len(proc.stderr.read().decode()) != 0:
                self.__is_error = True
            else:
                self.__is_error = False
