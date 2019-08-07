from infostretch.automation.core.base_environment import BaseEnvironment
from infostretch.automation.core.configurations_manager import ConfigurationsManager
from infostretch.automation.core.resources_manager import ResourcesManager
from infostretch.automation.util.qmetry_util import UploadResult
resourcesManager = ResourcesManager()
resourcesManager.set_up()

base_environment = BaseEnvironment()


def before_all(context):
    print(context)
    base_environment.before_all(context)


def before_feature(context, feature):
    base_environment.before_feature(context, feature)


def before_scenario(context, scenario):
    base_environment.before_scenario(context, scenario)


def before_step(context, step):
    base_environment.before_step(context, step)


def after_step(context, step):
    base_environment.after_step(context, step)


def after_scenario(context, scenario):
    base_environment.after_scenario(context, scenario)


def after_feature(context, feature):
    base_environment.after_feature(context, feature)


def after_all(context):
    base_environment.after_all(context)
    is_integration_enabled = ConfigurationsManager().get_str_for_key(
            "automation.qmetry.enabled", "false")
    if str(is_integration_enabled).lower() == "true" or str(is_integration_enabled).lower() == "yes":
        upload_result = UploadResult()
        upload_result.uploadFile();
