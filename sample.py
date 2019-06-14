import cv2
from pytube import YouTube

video = YouTube('https://www.youtube.com/watch?v=sLONUJjNz1g')
for itag_list in video.streams.all():
    print(itag_list)
stream = video.streams.get_by_itag(160)
stream.download()

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
