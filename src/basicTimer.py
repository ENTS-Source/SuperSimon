from communication.utils import *

class Timer:
    def __init__(self, resetVal):
        self.__resetTo = resetVal
        self.__value = self.__resetTo
        self.__active = False

    def start(self):
        self.__active = True
        self.__value = self.__resetTo

    def isStarted(self):
        return self.__active

    def valueSeconds(self):
        return self.__value / 1000.0

    def tick(self, delta):
        if not self.__active: return
        self.__value -= delta
        if self.__value <= 0:
            self.__active = False
