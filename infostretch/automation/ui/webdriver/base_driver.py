from appium import webdriver as appium_webdriver
from infostretch.automation.core.load_class import load_class
import json
from infostretch.automation.ui.webdriver import paf_web_driver as pafwebdriver
from infostretch.automation.core.configurations_manager import ConfigurationsManager
from infostretch.automation.keys.application_properties import ApplicationProperties


class BaseDriver:
    __driver = None

    def start_driver(self):
        """
        Start web driver session by referring driver capabilities for AUT.

        Returns:
            None
        """
        if BaseDriver.__driver is not None:
            self.stop_driver()


        default_browser = ConfigurationsManager().get_str_for_key(ApplicationProperties.DRIVER_NAME)
        if 'appium' in default_browser.lower():
            self.__start_appium_webdriver()
        else:
            self.__start_webdriver()

    def __start_appium_webdriver(self):
        driver_capabilities = ConfigurationsManager().get_dict_for_key('appium.additional.capabilities')
        selenium_server = ConfigurationsManager().get_str_for_key(ApplicationProperties.REMOTE_SERVER)
        selenium_port = ConfigurationsManager().get_str_for_key(ApplicationProperties.REMOTE_PORT)
        driver_capabilities["browserName"]=""
        driver = appium_webdriver.Remote(selenium_server + selenium_port + "/wd/hub", driver_capabilities)
        BaseDriver.__driver = pafwebdriver.PAFAppiumWebDriver(driver)
        BaseDriver.__driver.implicitly_wait(ConfigurationsManager().get_str_for_key(ApplicationProperties.SELENIUM_WAIT_TIMEOUT))

    def __start_webdriver(self):
        driver_name = ConfigurationsManager().get_str_for_key(ApplicationProperties.DRIVER_NAME)
        driver_name = str(driver_name).lower()
        driver_capabilities = ConfigurationsManager().get_str_for_key(
            driver_name[:driver_name.index('driver')]+'.additional.capabilities')

        if driver_capabilities is not None and 'driverClass' in driver_capabilities:
            class_name = driver_capabilities['driverClass']
        else:
            class_name = 'selenium.webdriver.{driver_name}.webdriver.WebDriver'. \
                format(driver_name=driver_name[:driver_name.index('driver')])
        #print("driver class" + class_name)
        selenium_server = ConfigurationsManager().get_str_for_key(ApplicationProperties.REMOTE_SERVER)
        selenium_port = ConfigurationsManager().get_str_for_key(ApplicationProperties.REMOTE_PORT)
        command_executor = selenium_server + selenium_port + "/wd/hub"

        if driver_capabilities is None:
            driver_class = load_class(class_name)()
        elif "remote" in ConfigurationsManager().get_str_for_key(ApplicationProperties.DRIVER_NAME).lower():
            driver_class = load_class(class_name)(command_executor=command_executor,
                desired_capabilities=json.loads(driver_capabilities))
        else:
            driver_class = load_class(class_name)(
                desired_capabilities=json.loads(driver_capabilities))
        env_base_url = ConfigurationsManager().get_str_for_key(
            ApplicationProperties.SELENIUM_BASE_URL)
        BaseDriver.__driver = pafwebdriver.PAFWebDriver(driver_class)
        BaseDriver.__driver.get(env_base_url)
        BaseDriver.__driver.implicitly_wait(ConfigurationsManager().get_str_for_key(ApplicationProperties.SELENIUM_WAIT_TIMEOUT))

    def stop_driver(self):
        """
        Stop web driver session.

        Returns:
            None
        """
        if BaseDriver.__driver is not None:
            BaseDriver.__driver.quit()
            BaseDriver.__driver = None

    def get_driver(self):
        """
        Returns web driver object.

        Returns:
            webdriver: Returns web driver object.
        """
        if BaseDriver.__driver is None:
            self.start_driver()

        return BaseDriver.__driver
