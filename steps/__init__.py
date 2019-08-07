
import os
from behave import *
from model.home_page import HomePage
from infostretch.automation.core.configurations_manager import ConfigurationsManager
from infostretch.automation.core.resources_manager import ResourcesManager

use_step_matcher("re")
import importlib


def load_class(full_class_string):
	class_data = full_class_string.split(".")
	module_path = ".".join(class_data[:-1])
	class_str = class_data[-1]
	module_name = importlib.import_module(module_path)
	return getattr(module_name, class_str)()

resourcesManager = ResourcesManager()
resourcesManager.set_up()
platform = ConfigurationsManager().get_str_for_key("platform")
stepdir='stepdefs/'+str(platform)
for dir_name, subdir_list, file_list in os.walk(stepdir):
	for name in file_list:
		if name.endswith('.py'):
			module_path = dir_name.replace('/','.') + '.' + name.replace('.py','');
			importlib.import_module(module_path)
# load_class(class_name)