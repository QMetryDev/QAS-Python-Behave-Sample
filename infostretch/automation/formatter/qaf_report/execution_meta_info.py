import json
import os


class ExecutionMetaInfo:
    def __init__(self):
        path_to_write = os.path.join(os.getenv('REPORT_DIR'), 'json')
        self.__meta_info_file_path = os.path.join(path_to_write, 'meta-info.json')

        if os.path.exists(self.__meta_info_file_path):
            with open(self.__meta_info_file_path) as f:
                _dict = json.load(f)

            self.name = str(_dict['name'])
            self.status = str(_dict['status'])
            self.__tests = _dict['tests']
            self.total_count = int(_dict['total'])
            self.pass_count = int(_dict['pass'])
            self.fail_count = int(_dict['fail'])
            self.skip_count = int(_dict['skip'])
            self.startTime = _dict['startTime']
            self.endTime = _dict['endTime']

        else:
            self.name = 'Features'
            self.status = ''
            self.__tests = []
            self.total_count = 0
            self.pass_count = 0
            self.fail_count = 0
            self.skip_count = 0
            self.startTime = ''
            self.endTime = ''

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def tests(self):
        return self.__tests

    def add_test(self, test_name):
        self.__tests.append(test_name)
        self._close()

    @property
    def total_count(self):
        return self.__total_count

    @total_count.setter
    def total_count(self, value):
        self.__total_count = value

    @property
    def pass_count(self):
        return self.__pass_count

    @pass_count.setter
    def pass_count(self, value):
        self.__pass_count = value

    @property
    def fail_count(self):
        return self.__fail_count

    @fail_count.setter
    def fail_count(self, value):
        self.__fail_count = value

    @property
    def skip_count(self):
        return self.__skip_count

    @skip_count.setter
    def skip_count(self, value):
        self.__skip_count = value

    @property
    def startTime(self):
        return self.__startTime

    @startTime.setter
    def startTime(self, value):
        self.__startTime = value
        self._close()

    @property
    def endTime(self):
        return self.__endTime

    @endTime.setter
    def endTime(self, value):
        self.__endTime = value
        self._close()

    def _close(self):
        self.__dump_into_json()

    def __dump_into_json(self):
        try:
            _dict = {
                "name": self.name,
                "status": self.status,
                "tests": self.tests,
                "total": self.total_count,
                "pass": self.pass_count,
                "fail": self.fail_count,
                "skip": self.skip_count,
                "startTime": self.startTime,
                "endTime": self.endTime
            }
            with open(self.__meta_info_file_path, 'w') as fp:
                json.dump(_dict, fp, sort_keys=True, indent=4)
        except:
            pass

    def update_status(self, scenario_status):
        if scenario_status.lower() == 'passed':
            self.pass_count += 1
        elif scenario_status.lower() == 'failed':
            self.fail_count += 1
        else:
            self.skip_count += 1

        self.total_count += 1

        if self.fail_count > 0:
            self.status = 'fail'
        else:
            self.status = 'pass'

        self._close()
