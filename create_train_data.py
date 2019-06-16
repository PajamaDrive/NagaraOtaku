import cv2
import glob
import os
import sys

def getCharacter():
    character_path = "characters.txt"

    characters = []
    if os.path.isfile(character_path):
        with open(character_path) as f:
            for line in f:
                characters.append(line.strip())

    new_characters = []
    for character in sys.argv[1:len(sys.argv)]:
        characters.append(character)
        new_characters.append(character)
    return characters, new_characters

def createData(characters, mode, each_video_data_num):
    #カスケード分類器の特徴量を取得する
    cascade_path = "../lbpcascade_animeface/lbpcascade_animeface.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    for character_name in characters:
        #動画のパス
        in_all_video_path = [p for p in glob.glob("../video/" + mode + "/" + character_name + "*") if os.path.isfile(p)]
        #out_all_video_path = "../video/tsukino_ditect.mp4"

        img_cnt = 1
        for in_video_path in in_all_video_path:
            out_img_dir = "../result/" + mode + "/" + character_name

            if not os.path.isdir(out_img_dir) :
                os.mkdir(out_img_dir)

            cap = cv2.VideoCapture(in_video_path)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            frame_num = 0
            video_img_cnt = 1
            # フレームごとの処理
            while(cap.isOpened()):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if (ret == False):
                    break

                if frame_num % 200 == 0:
                    print("frame : %d" % frame_num)
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(75, 75))

                    if len(facerect) > 0:
                        #検出した顔を囲む矩形の作成
                        print(img_cnt)
                        for (x,y,w,h) in facerect:
                            out_img_path = out_img_dir + "/" + str(img_cnt) + ".jpg"
                            face_image = frame[y:y + h, x:x + w]
                            face_image = cv2.resize(face_image, (128, 128))
                            cv2.imwrite(out_img_path, face_image)
                            img_cnt += 1
                            video_img_cnt += 1
                            face_height = face_image.shape[0]
                            face_width = face_image.shape[1]
                            face_center = (int(face_width / 2), int(face_height / 2))
                            for i in range(3) :
                                out_img_path = out_img_dir + "/" + str(img_cnt) + ".jpg"
                                angle = 90 * (i + 1)
                                scale = 1.0
                                #getRotationMatrix2D関数を使用
                                trans = cv2.getRotationMatrix2D(face_center, angle, scale)
                                #アフィン変換
                                rotate_image = cv2.warpAffine(face_image, trans, (face_width, face_height))
                                cv2.imwrite(out_img_path, rotate_image)
                                img_cnt += 1
                                video_img_cnt += 1
                if video_img_cnt >= each_video_data_num:
                    break;
                frame_num += 200

            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__" :
    #キャラクター一覧を取得
    characters, new_characters = getCharacter()
    #訓練データの作成
    createData(characters = characters, mode = "train", each_video_data_num = 200)

    character_path = "characters.txt"
    if len(new_characters) != 0:
        with open(character_path, mode = "a") as f:
            for character in new_characters :
                f.write("\n")
                f.write(character)
