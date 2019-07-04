import cv2
import pathlib
import numpy as np
from PIL import Image
from create_train_data import getCharacter

def getImageAndLabel(character, mode):
    images = []
    character_dictionary = getCharacterDictionary()
    for img_path in [p for p in pathlib.Path("tmp/train/" + character + "/").glob("*.jpg") if pathlib.Path.is_file(p)]:
        img = np.array(Image.open(img_path).convert("L"), "uint8")
        images.append(img)

    return images, [character_dictionary[character] for i in range(len(images))]

def getCharacterDictionary():
    characters = getCharacter()
    character_dictionary = {}
    index = 0
    #キャラクター名とラベルの辞書を初期化
    for character_name in characters:
        character_dictionary[character_name] = index
        index += 1
    return character_dictionary

def trainCharacter(character, mode = False):
    train_images, train_labels = getImageAndLabel(character, mode = "train")
    classifier = cv2.face.LBPHFaceRecognizer_create()
    if mode == False and pathlib.Path("config/classifier.xml").exists():
        classifier.read("config/classifier.xml")

    classifier.train(train_images, np.array(train_labels))
    classifier.save("config/classifier.xml")
