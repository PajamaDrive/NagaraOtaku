from create_train_data import getCharacter
from create_train_data import createData

if __name__ == "__main__":
    #キャラクター一覧を取得
    characters, new_characters = getCharacter()
    #テストデータの作成
    createData(characters = characters, mode = "test", each_video_data_num = 10)
