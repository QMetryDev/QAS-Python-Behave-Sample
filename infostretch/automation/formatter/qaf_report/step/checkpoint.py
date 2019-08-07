class CheckPoint:
    def __init__(self):
        self.message = ''
        self.type = ''
        self.duration = 0
        self.threshold = 0
        self.screenshot = ''
        self.subCheckPoints = []

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = int(value)

    @property
    def threshold(self):
        return self.__threshold

    @threshold.setter
    def threshold(self, value):
        self.__threshold = value

    @property
    def screenshot(self):
        return self.__screenshot

    @screenshot.setter
    def screenshot(self, value):
        self.__screenshot = value

    @property
    def subCheckPoints(self):
        return self.__subCheckPoints

    @subCheckPoints.setter
    def subCheckPoints(self, value):
        self.__subCheckPoints = value

    def to_json_dict(self):
        _dict = {
            "message": self.message,
            "type": self.type,
            "duration": self.duration,
            "threshold": self.threshold,
            "screenshot": self.screenshot,
            "subCheckPoints": self.subCheckPoints,
        }
        return _dict
