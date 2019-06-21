import tkinter as tk
import tkinter.font as font
import os
import cv2
import re
import ffmpeg
import pygame
import time
from PIL import Image, ImageTk
from mutagen.mp3 import MP3 as mp3

path = "../video/NagaraOtaku/suzuka.mp3"
pygame.mixer.init()
pygame.mixer.music.load(path)
pygame.mixer.music.play(-1)
mp3_length = mp3(path).info.length
time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
pygame.mixer.music.stop()

#YouTube("https://www.youtube.com/watch?v=Bw_uE7JAFlg")
'''
yt = YouTube("https://www.youtube.com/watch?v=Bw_uE7JAFlg")
# ダウンロードできる形式を表示
for video in yt.get_videos():
    print(video)
print('-' * 10)
# ファイル名を表示
print(yt.filename)
print('-' * 10)
# ダウンロードしたい形式を選択
video = yt.get('mp4', '720p')
# ダウンロードするファイル名を指定
yt.set_filename('download_pytube')
# ダウンロード実行
video.download('./')
'''
'''
# 入力画像のロード
img = cv2.imread('ChrSiro_Angry.jpg')

cv2.namedWindow('input')
cv2.imshow("input", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
