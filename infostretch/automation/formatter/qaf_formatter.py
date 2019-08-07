import os
from collections import deque

import six
from behave.formatter.base import Formatter
from behave.model_core import Status

from infostretch.automation.formatter.qaf_report.behave_before_all import before_all
from infostretch.automation.formatter.qaf_report.execution_meta_info import ExecutionMetaInfo
from infostretch.automation.formatter.qaf_report.feature.feature_overview import FeatureOverView
from infostretch.automation.formatter.qaf_report.scenario.scenario import Scenario
from infostretch.automation.formatter.qaf_report.scenario.scenario_meta_info import ScenarioMetaInfo, MetaData
from infostretch.automation.formatter.qaf_report.step.step import Step
from infostretch.automation.util.datetime_util import current_timestamp, date_time
from infostretch.automation.util.directory_util import create_directory

OUTPUT_TEST_RESULTS_DIR = 'test-results'


class QAFFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super(QAFFormatter, self).__init__(stream_opener, config)

        self.split_text_into_lines = True

        root_directory = os.path.join(OUTPUT_TEST_RESULTS_DIR, date_time())
        create_directory(root_directory)
        os.environ['REPORT_DIR'] = root_directory

        self.__current_feature = None
        self.__current_scenario = None

        self.__obj_scenario_meta_info = None
        self.__steps = deque()
        before_all()

    # Before Methods
    def feature(self, feature):
        self.finish_current_feature()

        self.__current_feature = feature

        current_feature_directory = os.path.join(os.getenv('REPORT_DIR'), 'json', feature.name)
        create_directory(current_feature_directory)
        os.environ['CURRENT_FEATURE_DIR'] = current_feature_directory

        ExecutionMetaInfo().add_test(feature.name)

        FeatureOverView().startTime = current_timestamp()
        FeatureOverView().add_class('Scenario')

    def scenario(self, scenario):
        self.finish_current_scenario()

        self.__current_scenario = scenario

        current_scenario_directory = os.path.join(os.getenv('CURRENT_FEATURE_DIR'), 'Scenario')
        create_directory(current_scenario_directory)
        os.environ['CURRENT_SCENARIO_DIR'] = current_scenario_directory

        Scenario(file_name=self.__current_scenario.name).errorTrace = ''

        self.__obj_scenario_meta_info = ScenarioMetaInfo()
        self.__obj_scenario_meta_info.startTime = current_timestamp()

    def step(self, step):
        self.__steps.append(step)

    def result(self, result):
        if result.error_message and result.result == Status.failed:
            error_message = result.error_message
            if self.split_text_into_lines and "\n" in error_message:
                error_message = error_message.splitlines()
                Scenario(file_name=self.__current_scenario.name).error_message = error_message

    # After Methods

    def flush_steps(self):
        while self.__steps:
            step = self.__steps.popleft()
            obj_step = Step()
            obj_step.start_behave_step(step)
            obj_step.stop_behave_step(step)
            Scenario(file_name=self.__current_scenario.name).add_checkPoints(obj_step.obj_check_point)
            del obj_step

    def finish_current_scenario(self):
        if self.__current_scenario:
            self.flush_steps()

            status_name = self.__current_scenario.status.name

            ExecutionMetaInfo().update_status(status_name)
            FeatureOverView().update_status(status_name)

            self.__obj_scenario_meta_info.duration = -1
            self.__obj_scenario_meta_info.result = status_name

            obj_meta_data = MetaData()
            obj_meta_data.name = self.__current_scenario.name
            if self.__current_scenario.description:
                obj_meta_data.description = self.__current_scenario.description
            obj_meta_data.reference = six.text_type(self.__current_scenario.location)

            self.__obj_scenario_meta_info.metaData = obj_meta_data.to_json_dict()
            self.__obj_scenario_meta_info.close()

            del self.__obj_scenario_meta_info
            self.__obj_scenario_meta_info = None

            del self.__current_scenario
            self.__current_scenario = None

    def finish_current_feature(self):
        if self.__current_feature:
            FeatureOverView().endTime = current_timestamp()

            del self.__current_feature
            self.__current_feature = None

    # After Feature complete
    def eof(self):
        self.finish_current_scenario()
        self.finish_current_feature()

    # After All
    def close(self):
        ExecutionMetaInfo().endTime = current_timestamp()
