import json
import os

from infostretch.automation.formatter.qaf_report.util.utils import scenario_status


class ScenarioMetaInfo:
    def __init__(self):
        path_to_write = os.getenv('CURRENT_SCENARIO_DIR')
        self.__meta_info_file_path = os.path.join(path_to_write, 'meta-info.json')

        self.index = 1
        self.type = 'test'
        self.__args = []
        self.metaData = {}
        self.dependsOn = []
        self.startTime = 0
        self.duration = 0
        self.result = ''
        self.passPer = 0.0

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        self.__index = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def args(self):
        return self.__args

    def add_args(self, arg):
        self.__args.append(arg)

    @property
    def metaData(self):
        return self.__metaData

    @metaData.setter
    def metaData(self, value):
        self.__metaData = value

    @property
    def dependsOn(self):
        return self.__dependsOn

    @dependsOn.setter
    def dependsOn(self, value):
        self.__dependsOn = value

    @property
    def startTime(self):
        return self.__startTime

    @startTime.setter
    def startTime(self, value):
        self.__startTime = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = int(value)

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = scenario_status(value)

    @property
    def passPer(self):
        return self.__passPer

    @passPer.setter
    def passPer(self, value):
        self.__passPer = value

    def __dump_into_json(self):
        _dict = {
            "index": self.index,
            "type": self.type,
            "args": self.args,
            "metaData": self.metaData,
            "dependsOn": self.dependsOn,
            "startTime": self.startTime,
            "duration": self.duration,
            "result": self.result,
            "passPer": self.passPer
        }

        if os.path.exists(self.__meta_info_file_path):
            with open(self.__meta_info_file_path, "r") as jsonFile:
                data = json.load(jsonFile)
                methods = data['methods']
        else:
            methods = []
        methods.append(_dict)
        final_data = {'methods': methods}

        with open(self.__meta_info_file_path, 'w') as fp:
            json.dump(final_data, fp, sort_keys=True, indent=4)

    def close(self):
        try:
            self.__dump_into_json()
        except:
            pass


class MetaData:
    def __init__(self):
        self.description = ''
        self.groups = []
        self.lineNo = 0
        self.name = ''
        self.referece = ''
        self.sign = ''
        self.resultFileName = ''

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def resultFileName(self):
        return self.__resultFileName

    @resultFileName.setter
    def resultFileName(self, value):
        self.__resultFileName = value 

    @property
    def groups(self):
        return self.__groups

    @groups.setter
    def groups(self, value):
        self.__groups = value

    @property
    def lineNo(self):
        return self.__lineNo

    @lineNo.setter
    def lineNo(self, value):
        self.__lineNo = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def referece(self):
        return self.__referece

    @referece.setter
    def referece(self, value):
        self.__referece = value

    @property
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, value):
        self.__sign = value

    def to_json_dict(self):
        _dict = {
            "description": self.description,
            "groups": self.groups,
            "lineNo": self.lineNo,
            "name": self.name,
            "referece": self.referece,
            "resultFileName": self.resultFileName,
            "sign": self.sign
        }
        return _dict
