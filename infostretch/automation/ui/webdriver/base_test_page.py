from infostretch.automation.ui.webdriver.base_driver import BaseDriver
from infostretch.automation.ui.webdriver.paf_web_driver import PAFWebDriver


class BaseTestPage:
    @property
    def driver(self):
        return PAFWebDriver(BaseDriver().get_driver())
