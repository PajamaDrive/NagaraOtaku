import cv2
import pathlib
import numpy as np
from PIL import Image
from create_train_data import getCharacter
import zipfile
import shutil

def getImageAndLabel(mode):
    images = []
    labels = []
    character_dictionary = getCharacterDictionary()
    for character in getCharacter():
        if pathlib.Path("tmp/train/" + character + ".zip").exists():
            with zipfile.ZipFile("tmp/train/" + character + ".zip", "r") as train_zip:
                dir_path = pathlib.Path("tmp/train/" + character)
                if not dir_path.exists():
                    dir_path.mkdir()
                train_zip.extractall("tmp/train/" + character)
        for img_path in [p for p in pathlib.Path("tmp/train/" + character + "/").glob("*.jpg") if pathlib.Path.is_file(p)]:
            img = np.array(Image.open(img_path).convert("L"), "uint8")
            images.append(img)
            labels.append(character_dictionary[character])
    return images, labels

def getCharacterDictionary():
    characters = getCharacter()
    character_dictionary = {}
    index = 0
    #キャラクター名とラベルの辞書を初期化
    for character_name in characters:
        character_dictionary[character_name] = index
        index += 1
    return character_dictionary

def trainCharacter(mode = False):
    train_images, train_labels = getImageAndLabel(mode = "train")
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(train_images, np.array(train_labels))
    classifier.save("config/classifier.xml")
    for character in getCharacter():
        shutil.rmtree("tmp/train/" + character)

if __name__ == "__main__":
    trainCharacter()
