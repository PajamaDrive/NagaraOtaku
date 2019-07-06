class VideoTime:
    def __init__(self):
        self.__hour = 0
        self.__min = 0
        self.__sec = 0

    @property
    def hour(self):
        return self.__hour

    @property
    def min(self):
        return self.__min

    @property
    def sec(self):
        return self.__sec

    def setTime(self, time):
        temp = time
        self.__hour = int(temp // 3600)
        temp %= 3600
        self.__min = int(temp // 60)
        temp %= 60
        self.__sec = int(temp)

    def getTime(self):
        return self.__hour, self.__min, self.__sec

    def getWholeSecond(self):
        return self.__hour * 3600 + self.__min * 60 + self.__sec
