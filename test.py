import cv2
from train import getImageAndLabel
from create_train_data import getCharacter

if __name__ == "__main__":
    print("Loading...")
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.read("classifier.xml")
    print("Finish")
    characters, new_characters = getCharacter()
    #createTrainData(characters = characters, mode = "test")
    test_images, test_labels = getImageAndLabel(characters = characters, mode = "test")

    i = 0
    while i < len(test_labels):
        # テスト画像に対して予測実施
        label, confidence = classifier.predict(test_images[i])
        # 予測結果をコンソール出力
        print("Test Image:, Predicted Label: {}, Confidence: {}".format( label, confidence))
        # テスト画像を表示
        cv2.imshow("test image", test_images[i])
        cv2.waitKey(300)
        i += 1

    # 終了処理
    cv2.destroyAllWindows()
