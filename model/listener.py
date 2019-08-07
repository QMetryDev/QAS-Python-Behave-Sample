from infostretch.automation.core.message_type import MessageType
from infostretch.automation.core.reporter import Reporter
from infostretch.automation.ui.webdriver.abstract_listener import DriverListener


class Listener(DriverListener):
    def before_command(self, driver, command_tracker):
        pass

    def after_command(self, driver, command_tracker):
        pass

    def on_exception(self, driver, command_tracker):
        command_tracker.retry = True


class ElementListener(DriverListener):
    def before_command(self, driver, command_tracker):
        pass

    def after_command(self, driver, command_tracker):
        pass

    def on_exception(self, driver, command_tracker):
        command_tracker.retry = True
