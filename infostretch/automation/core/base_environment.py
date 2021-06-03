from behave.model_core import Status
import os
import platform
import json
import six
import re
from infostretch.automation.core.message_type import MessageType
from infostretch.automation.ui.webdriver.base_driver import BaseDriver

from infostretch.automation.core.project_environment import ProjectEnvironment
from infostretch.automation.formatter.qaf_report.behave_before_all import before_all
from infostretch.automation.formatter.qaf_report.scenario.scenario_meta_info import ScenarioMetaInfo, MetaData
from infostretch.automation.formatter.qaf_report.scenario.scenario import Scenario
from infostretch.automation.formatter.qaf_report.feature.feature_overview import FeatureOverView
from infostretch.automation.formatter.qaf_report.execution_meta_info import ExecutionMetaInfo
from infostretch.automation.formatter.qaf_report.scenario.selenium_log import SeleniumLogStack
from infostretch.automation.formatter.qaf_report.step.step import Step
from infostretch.automation.util.datetime_util import date_time, current_timestamp
from infostretch.automation.util.directory_util import create_directory
from infostretch.automation.core.configurations_manager import ConfigurationsManager

OUTPUT_TEST_RESULTS_DIR = 'test-results'


class BaseEnvironment:

    def __init__(self):
        self.current_feature = None
        self.current_scenario = None
        self.current_step = None
        self.obj_scenario_meta_info = None

    def before_all(self, context):
        ProjectEnvironment.set_up()

        root_directory = os.path.join(OUTPUT_TEST_RESULTS_DIR, date_time())
        create_directory(root_directory)
        os.environ['REPORT_DIR'] = root_directory

        before_all()

    def after_all(self, context):
        ExecutionMetaInfo().endTime = current_timestamp()
        BaseDriver().stop_driver()

    def before_feature(self, context, feature):
        envInfoDetails={"browser-desired-capabilities": {},"browser-actual-capabilities": {},"isfw-build-info": {},"run-parameters": {},"execution-env-info": {}}
        current_feature_directory = os.path.join(os.getenv('REPORT_DIR'), 'json', re.sub(
            '[^A-Za-z0-9]+', ' - ', re.sub('.feature', '', feature.filename)))
        create_directory(current_feature_directory)
        os.environ['CURRENT_FEATURE_DIR'] = current_feature_directory

        ExecutionMetaInfo().add_test(
            re.sub('[^A-Za-z0-9]+', ' - ', re.sub('.feature', '', feature.filename)))

        FeatureOverView().startTime = current_timestamp()
        FeatureOverView().add_class(feature.name)
        # driver_name = str(ConfigurationsManager().get_str_for_key('driver.name'))
        # driver_name[:str(driver_name).lower().index('driver')]
        envInfoDetails["browser-desired-capabilities"]["browserName"] = BaseDriver().get_driver().capabilities['browserName']
        envInfoDetails["browser-desired-capabilities"]["cssSelectorsEnabled"]= "true"
        envInfoDetails["browser-desired-capabilities"]["javascriptEnabled"]= "true"
        envInfoDetails["browser-desired-capabilities"]["takesScreenshot"]= "true"
        envInfoDetails["browser-desired-capabilities"]["platform"] = str(ConfigurationsManager().get_str_for_key('platform'))
        envInfoDetails["browser-desired-capabilities"]["version"] = BaseDriver().get_driver().capabilities['browserVersion']
        json_object = BaseDriver().get_driver().capabilities
        pairs = json_object.items()
        for key, value in pairs:
            # print(str(value))
            envInfoDetails["browser-actual-capabilities"][key]= str(value)

        envInfoDetails["isfw-build-info"]["qaf-Type"] = "core"
        envInfoDetails["isfw-build-info"]["qaf-Build-Time"] = current_timestamp()
        envInfoDetails["isfw-build-info"]["qaf-Version"] = "3.0"

        envInfoDetails["run-parameters"]["resources"] = str(ConfigurationsManager().get_str_for_key('env.resources'))
        envInfoDetails["run-parameters"]["file.feature"] = "feature/"+ str(ConfigurationsManager().get_str_for_key('platform'))
        envInfoDetails["run-parameters"]["baseurl"] = str(ConfigurationsManager().get_str_for_key('env.baseurl'))
        
        # envInfoDetails["execution-env-info"]["java.arch"] = "64"
        # envInfoDetails["execution-env-info"]["java.vendor"] = "Oracle Corporation 22"
        envInfoDetails["execution-env-info"]["python.version"] = platform.python_version()
        envInfoDetails["execution-env-info"]["os.arch"] = platform.processor()
        envInfoDetails["execution-env-info"]["host"] = platform.node()
        envInfoDetails["execution-env-info"]["os.name"] = platform.platform()
        envInfoDetails["execution-env-info"]["user.name"] = os.getlogin()
        envInfoDetails["execution-env-info"]["os.version"] = platform.version()

        # drivercap = json.loads(BaseDriver.__driver.capabilities)
        # print(BaseDriver().get_driver().capabilities['browserName'])
        FeatureOverView().add_envInfo(envInfoDetails)


    def after_feature(self, context, feature):
        FeatureOverView().endTime = current_timestamp()

    def before_scenario(self, context, scenario):
        self.current_scenario = scenario
        current_scenario_directory = os.path.join(
            os.getenv('CURRENT_FEATURE_DIR'), scenario.feature.name)
        create_directory(current_scenario_directory)
        os.environ['CURRENT_SCENARIO_DIR'] = current_scenario_directory

        self.obj_scenario_meta_info = ScenarioMetaInfo()
        self.obj_scenario_meta_info.startTime = current_timestamp()

    def after_scenario(self, context, scenario):
        status_name = scenario.status.name
        if "##" in scenario.name:
            x=(scenario.name).split("##")
            scenario.name=x[0]
            scenario.description=x[1]
 
        if "##" in self.current_scenario.name:
            x=(self.current_scenario.name).split("##")
            self.current_scenario.name=x[0]
            self.current_scenario.description=x[1]
        
        if scenario.status == Status.failed:
            steps = scenario.steps
            for step in steps:
                if step.status == Status.failed:
                    error_message = step.error_message
                    error_message = error_message.splitlines()

                    Scenario(file_name=scenario.name).errorTrace = error_message
                elif step.status == Status.skipped or step.status == Status.untested:
                    obj_step = Step()
                    obj_step.start_behave_step(step)
                    obj_step.stop_behave_step(step)
                    Scenario(file_name=self.current_scenario.name).add_checkPoints(
                        obj_step.obj_check_point)
                    del obj_step
        else:
            checkPoints = Scenario(
                file_name=self.current_scenario.name).checkPoints
            for checkPoint in checkPoints:
                if checkPoint['type'] == MessageType.TestStepFail:
                    status_name = 'failed'
                    break

        ExecutionMetaInfo().update_status(status_name)
        FeatureOverView().update_status(status_name)

        self.obj_scenario_meta_info.duration = scenario.duration * 1000
        self.obj_scenario_meta_info.result = status_name

        obj_meta_data = MetaData()
        obj_meta_data.name = scenario.name
        obj_meta_data.resultFileName = scenario.name
        if scenario.description:
            obj_meta_data.description = scenario.description
        obj_meta_data.reference = six.text_type(scenario.location)
        obj_meta_data.referece = six.text_type(scenario.location)
        obj_meta_data.groups = scenario.effective_tags
        self.obj_scenario_meta_info.metaData = obj_meta_data.to_json_dict()
        self.obj_scenario_meta_info.close()

        del self.obj_scenario_meta_info
        self.obj_scenario_meta_info = None
        Scenario(file_name=scenario.name).seleniumLog = SeleniumLogStack(
        ).get_all_selenium_log()


    BaseDriver().stop_driver()


    def before_step(self, context, step):
        self.current_step = step


    def after_step(self, context, step):
        obj_step = Step()
        obj_step.start_behave_step(step)
        obj_step.stop_behave_step(step)
        Scenario(file_name=self.current_scenario.name).add_checkPoints(
            obj_step.obj_check_point)
        del obj_step
