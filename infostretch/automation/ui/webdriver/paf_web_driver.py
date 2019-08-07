from selenium.webdriver.support.wait import WebDriverWait

from infostretch.automation.ui import js_toolkit
from infostretch.automation.ui.util.paf_wd_expected_conditions import WaitForAjax
from infostretch.automation.ui.webdriver.paf_find_by import get_find_by
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from appium.webdriver.webdriver import WebDriver as AppiumRemoteWebDriver

from infostretch.automation.core.configurations_manager import ConfigurationsManager
from infostretch.automation.core.load_class import load_class
from infostretch.automation.keys.application_properties import ApplicationProperties
from infostretch.automation.ui.webdriver.command_tracker import CommandTracker
from infostretch.automation.ui.webdriver import paf_web_element as pafwebelement, base_driver
from infostretch.automation.ui.webdriver.paf_webdriver_listener import PAFWebDriverListener


class PAFWebDriver(RemoteWebDriver):

    def __init__(self, driver, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None):
        command_executor = driver.command_executor
        self.__driver = driver
        self.w3c = False

        self.__listeners = []
        self.__listeners.append(PAFWebDriverListener())

        RemoteWebDriver.__init__(self, command_executor=command_executor,
                                 desired_capabilities=driver.desired_capabilities,
                                 browser_profile=browser_profile,
                                 proxy=proxy,
                                 keep_alive=keep_alive, file_detector=file_detector, options=options)

        if ConfigurationsManager().contains_key(ApplicationProperties.WEBDRIVER_COMMAND_LISTENERS):
            class_name = ConfigurationsManager().get_str_for_key(ApplicationProperties.WEBDRIVER_COMMAND_LISTENERS)
            self.__listeners.append(load_class(class_name)())

    def start_session(self, capabilities, browser_profile=None):
        self.command_executor = self.__driver.command_executor
        self.capabilities = self.__driver.capabilities
        if hasattr(self.command_executor, 'w3c') and self.command_executor.w3c:
            self.w3c = self.command_executor.w3c is None
        self.w3c = self.__driver.w3c
        self.session_id = self.__driver.session_id
        self._is_remote = self.__driver._is_remote

    def find_element(self, by=By.ID, value=None, key=None):
        if key is not None and len(key) > 0:
            value = ConfigurationsManager().get_str_for_key(key, default_value=key)
            by, value = get_find_by(value)

        web_element = super(PAFWebDriver, self).find_element(by=by, value=value)
        paf_web_element = pafwebelement.PAFWebElement.create_instance_using_webelement(web_element)
        paf_web_element._parent = self
        paf_web_element.by = by
        paf_web_element.locator = value
        paf_web_element.description = value
        return paf_web_element

    def find_elements(self, by=By.ID, value=None, key=None):
        if key is not None and len(key) > 0:
            value = ConfigurationsManager().get_str_for_key(key, default_value=key)
            by, value = get_find_by(value)

        web_elements = super(PAFWebDriver, self).find_elements(by=by, value=value)
        paf_web_elements = []
        for web_element in web_elements:
            paf_web_element = pafwebelement.PAFWebElement.create_instance_using_webelement(web_element)
            paf_web_element._parent = self
            paf_web_element.by = by
            paf_web_element.locator = value
            paf_web_element.description = value
            paf_web_elements.append(paf_web_element)
        return paf_web_elements

    def wait_for_ajax(self, jstoolkit=js_toolkit.GLOBAL_WAIT_CONDITION, wait_time=0):
        wait_time_out = ConfigurationsManager().get_int_for_key(ApplicationProperties.SELENIUM_WAIT_TIMEOUT) \
            if wait_time == 0 else wait_time
        message = 'Wait time out for ajax to complete'
        return WebDriverWait(base_driver.BaseDriver().get_driver(), wait_time_out).until(
            WaitForAjax(jstoolkit), message
        )

    def execute(self, driver_command, params=None):
        command_tracker = CommandTracker(driver_command, params)
        self.before_command(command_tracker)

        try:
            if command_tracker.response is None:
                response = super(PAFWebDriver, self).execute(command_tracker.command,
                                                             command_tracker.parameters)
                command_tracker.response = response
        except Exception as e:
            self.on_exception(command_tracker)
            command_tracker.exception = e

        if command_tracker.has_exception():
            if command_tracker.retry:
                response = super(PAFWebDriver, self).execute(command_tracker.command,
                                                             command_tracker.parameters)
                command_tracker.response = response
                command_tracker.exception = None
            else:
                raise command_tracker.exception

        self.after_command(command_tracker)
        return command_tracker.response

    # Listener methods
    def before_command(self, command_tracker):
        if self.__listeners is not None:
            for listener in self.__listeners:
                listener.before_command(self, command_tracker)

    def after_command(self, command_tracker):
        if self.__listeners is not None:
            for listener in self.__listeners:
                listener.after_command(self, command_tracker)

    def on_exception(self, command_tracker):
        if self.__listeners is not None:
            for listener in self.__listeners:
                listener.on_exception(self, command_tracker)


class PAFAppiumWebDriver(AppiumRemoteWebDriver, PAFWebDriver):
    pass
