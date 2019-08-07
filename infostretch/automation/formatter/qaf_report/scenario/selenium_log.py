from collections import deque

from infostretch.automation.core.singleton import Singleton


class SeleniumLog:
    def __init__(self):
        self.commandName = ''
        self.args = {}
        self.result = ''
        self.__subLogs = []
        self.duration = 0

    @property
    def commandName(self):
        return self.__commandName

    @commandName.setter
    def commandName(self, value):
        self.__commandName = value

    @property
    def args(self):
        return self.__args

    @args.setter
    def args(self, value):
        self.__args = value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value

    @property
    def subLogs(self):
        return self.__subLogs

    def add_subLogs(self, sub_log):
        self.__subLogs.append(sub_log)

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value

    def to_json_dict(self):
        args_array = []
        for key, value in self.args.items():
            args_array.append(str(key) + ':' + str(value))

        _dict = {
            "commandName": self.commandName,
            "args": args_array,
            "result": self.result,
            "subLogs": self.subLogs,
            "duration": self.duration,
        }
        return _dict

    def to_string(self):
        string = 'Command: ' + self.commandName
        for key, value in self.args.items():
            string = string + ' ' + str(key) + ':' + str(value)
        string = string + str(self.result)
        return string


class SeleniumLogStack(metaclass=Singleton):
    def __init__(self):
        self.__selenium_log_stack = deque()

    def add_selenium_log(self, selenium_log):
        self.__selenium_log_stack.append(selenium_log.to_json_dict())

    def get_all_selenium_log(self):
        arr_selenium_log = []
        while self.__selenium_log_stack:
            selenium_log = self.__selenium_log_stack.popleft()
            arr_selenium_log.append(selenium_log)
        return arr_selenium_log
