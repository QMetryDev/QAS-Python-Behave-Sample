from re import split

from behave import *
from golem.actions import maximize_window
from pluggy import manager

from infostretch.automation.core.configurations_manager import \
    ConfigurationsManager
from infostretch.automation.ui.webdriver.base_driver import BaseDriver
from infostretch.automation.ui.webdriver.base_test_page import BaseTestPage
from infostretch.automation.ui.webdriver.paf_web_element import PAFWebElement
from model.home_page import HomePage

use_step_matcher("re")

@then('maximize window')
def step_impl(context):
    BaseDriver().get_driver().maximize_window()

@then('verify "(.*)" has been credited to "(\S+)"')
def step_impl(context,amount, loc):
    currentBalance = str(ConfigurationsManager().get_object_for_key('lastStepResult')).split(" ")[1]
    updated_amount = int(currentBalance) + int(amount)
    text = "$ " + str(updated_amount)
    PAFWebElement(loc).verify_text(text)

@then('verify "(.*)" has been debited from "(\S+)"')
def step_impl(context,amount, loc):
    currentBalance = str(ConfigurationsManager().get_object_for_key('lastStepResult')).split(" ")[1]
    updated_amount = int(currentBalance) - int(amount)
    text = "$ " + str(updated_amount)
    PAFWebElement(loc).verify_text(text)