import cv2
import sys
import os
from create_train_data import getCharacter
from train import getCharacterDictionary
from PIL import Image

def characterDetectFromVideo(object_characters, str_frequency, str_alert_confidence, video_name):
    frequency = int(str_frequency)
    alert_confidence = float(str_alert_confidence)
    #カスケード分類器の特徴量を取得する
    cascade_path = "../lbpcascade_animeface/lbpcascade_animeface.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    #識別器のロード
    print("Loading...")
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.read("classifier.xml")
    print("Finish")

    characters, new_characters = getCharacter()
    object_label = [getCharacterDictionary()[name] for name in object_characters]

    #for character_name in object_characters:
    #動画のパス
    in_video_path = "../video/NagaraOtaku/" + video_name
    if not os.path.isfile(in_video_path):
        print("ファイルが開けません")
    cap = cv2.VideoCapture(in_video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frame_rate = int(cap.get(5))
    cv2.namedWindow('Video',  cv2.WINDOW_AUTOSIZE)
    frame_num = 0
    # フレームごとの処理
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (ret == False):
            break
        cv2.waitKey(frame_rate)
        cv2.imshow("Video", frame)

        if frame_num % (frequency * frame_rate) == 0:
            print("frame : %d" % frame_num)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(75, 75))

            if len(facerect) > 0:
                #検出した顔を囲む矩形の作成
                for (x,y,w,h) in facerect:
                    face_image = frame_gray[y:y + h, x:x + w]
                    face_image = cv2.resize(face_image, (128, 128))
                    label, confidence = classifier.predict(face_image)
                    print("Test Image:, Predicted Label: {}, Confidence: {}".format( label, confidence))
                    if confidence < alert_confidence:
                        print("Character : {}".format(characters[label]))

        frame_num += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("引数が不正です")
        sys.exit(0)
    else:
        characterDetectFromVideo(sys.argv[1:len(sys.argv) - 3], sys.argv[-3], sys.argv[-2], sys.argv[-1])
