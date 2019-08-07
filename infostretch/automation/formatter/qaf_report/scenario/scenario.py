import json
import os


class Scenario:
    def __init__(self, file_name):
        path_to_write = os.getenv('CURRENT_SCENARIO_DIR')
        self.__scenario_file_path = os.path.join(path_to_write, file_name + '.json')

        if os.path.exists(self.__scenario_file_path):
            with open(self.__scenario_file_path) as f:
                _dict = json.load(f)

            self.seleniumLog = _dict['seleniumLog']
            self.__checkPoints = _dict['checkPoints']
            self.errorTrace = _dict['errorTrace']
        else:
            self.seleniumLog = []
            self.__checkPoints = []
            self.errorTrace = ''

    @property
    def seleniumLog(self):
        return self.__seleniumLog

    @seleniumLog.setter
    def seleniumLog(self, value):
        self.__seleniumLog = value
        self.__dump_to_json()

    @property
    def checkPoints(self):
        return self.__checkPoints

    def add_checkPoints(self, value):
        self.__checkPoints.append(value.to_json_dict())
        self.__dump_to_json()

    @property
    def errorTrace(self):
        return self.__errorTrace

    @errorTrace.setter
    def errorTrace(self, value):
        self.__errorTrace = "\n".join(value) if isinstance(value, list) else value
        self.__dump_to_json()

    def __dump_to_json(self):
        try:
            _dict = {
                "seleniumLog": self.seleniumLog,
                "checkPoints": self.checkPoints,
                "errorTrace": self.errorTrace,
            }
            with open(self.__scenario_file_path, 'w') as fp:
                json.dump(_dict, fp, sort_keys=True, indent=4)
        except:
            pass
