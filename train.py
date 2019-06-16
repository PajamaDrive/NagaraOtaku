import cv2
import glob
import os
import numpy as np
from PIL import Image
from create_train_data import getCharacter

def getImageAndLabel(characters, mode):
    images = []
    characters, new_characters = getCharacter()
    character_dictionary = getCharacterDictionary()

    for character_name in characters:
        for img_path in [p for p in glob.glob("../result/" + mode + "/" + character_name + "/*") if os.path.isfile(p)]:
            img = np.array(Image.open(img_path).convert("L"), "uint8")
            images.append(img)
    return images, [character_dictionary[character_name] for i in range(len(images))]

def getCharacterDictionary():
    characters, new_characters = getCharacter()
    character_dictionary = {}
    index = 0
    #キャラクター名とラベルの辞書を初期化
    for character_name in characters:
        character_dictionary[character_name] = index
        index += 1
    return character_dictionary

if __name__ == "__main__":
    characters, new_characters = getCharacter()
    #訓練データの取得
    train_images, train_labels = getImageAndLabel(characters = characters, mode = "train")
    print("Now training...")
    #訓練データで学習を行う
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(train_images, np.array(train_labels))
    print("Finish")
    #学習済みの識別器を保存
    classifier.save("classifier.xml")
