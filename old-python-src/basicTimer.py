class BasicTimer:
    def __init__(self, reset_val):
        self.__resetTo = reset_val
        self.__value = self.__resetTo
        self.__active = False

    def start(self):
        self.reset()
        self.__active = True

    def reset(self):
        self.__value = self.__resetTo

    def is_started(self):
        return self.__active

    def value_in_seconds(self):
        return self.__value / 1000.0

    def tick(self, delta):
        if not self.__active:
            return
        self.__value -= delta
        if self.__value <= 0:
            self.__active = False
