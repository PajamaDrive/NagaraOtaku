import cv2
import pathlib
import numpy as np
import zipfile
import shutil

def getCharacter():
    character_path = pathlib.Path("config/characters.txt")
    characters = []
    if character_path.exists():
        with character_path.open() as f:
            for line in f:
                characters.append(line.strip())
    else:
        character_path.touch()
    return characters

def addCharacter(character_name):
    character_path = "config/characters.txt"
    characters = getCharacter()
    if not character_name in characters:
        with open(character_path, mode = "a") as f:
            f.write(character_name)
            f.write("\n")

def createTrainData(video_path, character_name, each_video_data_num = 1000):
    #カスケード分類器の特徴量を取得する
    cascade_path = "../lbpcascade_animeface/lbpcascade_animeface.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    average_square = (3, 3)
    row, col, ch= (128, 128, 3)
    mean = 0
    sigma = 15
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    # ルックアップテーブルの生成
    min_table = 50
    max_table = 205
    diff_table = max_table - min_table

    lut_hc = np.arange(256, dtype = 'uint8' )
    lut_lc = np.arange(256, dtype = 'uint8' )

    # ハイコントラストLUT作成
    for i in range(0, min_table):
        lut_hc[i] = 0
    for i in range(min_table, max_table):
        lut_hc[i] = 255 * (i - min_table) / diff_table
    for i in range(max_table, 255):
        lut_hc[i] = 255

    # ローコントラストLUT作成
    for i in range(256):
        lut_lc[i] = min_table + i * (diff_table) / 255

    v_path = pathlib.Path(video_path)
    out_img_dir = pathlib.Path("tmp/train/" + character_name)
    if not out_img_dir.exists() :
        out_img_dir.mkdir(parents = True)

    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    img_cnt = 1
    # フレームごとの処理
    while(cap.isOpened()):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if (ret == False):
            break
        if frame_num % 200 == 0:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(75, 75))
            if len(facerect) > 0:
                #検出した顔を囲む矩形の作成
                for (x,y,w,h) in facerect:
                    out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                    face_image = frame[y:y + h, x:x + w]
                    face_image = cv2.resize(face_image, (128, 128))
                    cv2.imwrite(out_img_path, face_image)
                    img_cnt += 1
                    #平滑化
                    out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                    blur_image = cv2.blur(face_image, average_square)
                    cv2.imwrite(out_img_path, blur_image)
                    img_cnt += 1
                    #ノイズ
                    out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                    gauss_image = face_image + gauss
                    cv2.imwrite(out_img_path, gauss_image)
                    img_cnt += 1
                    #コントラスト調整
                    out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                    high_cont_image = cv2.LUT(face_image, lut_hc)
                    cv2.imwrite(out_img_path, high_cont_image)
                    img_cnt += 1
                    out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                    low_cont_image = cv2.LUT(face_image, lut_lc)
                    cv2.imwrite(out_img_path, low_cont_image)
                    img_cnt += 1
                    face_height = face_image.shape[0]
                    face_width = face_image.shape[1]
                    face_center = (int(face_width / 2), int(face_height / 2))
                    for i in range(3) :
                        out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                        angle = 90 * (i + 1)
                        scale = 1.0
                        #getRotationMatrix2D関数を使用
                        trans = cv2.getRotationMatrix2D(face_center, angle, scale)
                        #アフィン変換
                        rotate_image = cv2.warpAffine(face_image, trans, (face_width, face_height))
                        cv2.imwrite(out_img_path, rotate_image)
                        img_cnt += 1
                        #平滑化
                        out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                        blur_image = cv2.blur(rotate_image, average_square)
                        cv2.imwrite(out_img_path, blur_image)
                        img_cnt += 1
                        #ノイズ
                        out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                        gauss_image = rotate_image + gauss
                        cv2.imwrite(out_img_path, gauss_image)
                        img_cnt += 1
                        #コントラスト調整
                        out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                        high_cont_image = cv2.LUT(rotate_image, lut_hc)
                        cv2.imwrite(out_img_path, high_cont_image)
                        img_cnt += 1
                        out_img_path = str(out_img_dir) + "/" + v_path.stem + "_" + str(img_cnt) + ".jpg"
                        low_cont_image = cv2.LUT(rotate_image, lut_lc)
                        cv2.imwrite(out_img_path, low_cont_image)
                        img_cnt += 1
        if img_cnt >= each_video_data_num:
            break;
        frame_num += 200

    cap.release()
    cv2.destroyAllWindows()
    with zipfile.ZipFile("tmp/train/" + character_name + ".zip", "a", compression = zipfile.ZIP_DEFLATED) as train_zip:
        for image in pathlib.Path("tmp/train/" + character_name + "/").glob("*.jpg"):
            train_zip.write(str(image), arcname = str(pathlib.Path(image).name))
    shutil.rmtree("tmp/train/" + character_name)

def getTestData(img):
    #カスケード分類器の特徴量を取得する
    cascade_path = "../lbpcascade_animeface/lbpcascade_animeface.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    facerect = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    images = []
    cnt = 1
    if len(facerect) > 0:
        #検出した顔を囲む矩形の作成
        for (x,y,w,h) in facerect:
            face_image = img_gray[y:y + h, x:x + w]
            face_image = cv2.resize(face_image, (128, 128))
            images.append(face_image)
            cnt += 1

    return images

if __name__ == "__main__" :
    #キャラクター一覧を取得
    characters, new_characters = getCharacter()
    #訓練データの作成
    createData(characters = characters, mode = "train", each_video_data_num = 200)
