from infostretch.automation.core.reporter import Reporter
from infostretch.automation.ui.webdriver.base_test_page import BaseTestPage
from infostretch.automation.ui.webdriver.paf_web_element import PAFWebElement


class HomePage(BaseTestPage):
    def __init__(self):
        self.sign_in_button = PAFWebElement('home.login.button')
        self.register_button = PAFWebElement('home.register.button')

    def enter_text(self, value, key):
        element = PAFWebElement(key)
        Reporter.log('Enter ' + value + ' for ' + key)
        element.wait_for_present()
        element.verify_present()
        element.send_keys(value)

    def clicks_on_button(self, key):
        Reporter.log_with_screenshot('Login Page is verified')
        element = PAFWebElement(key)
        element.click()

    def verify_page(self):
        self.sign_in_button.assert_present()
        self.register_button.assert_present()
