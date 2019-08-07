import uuid
from infostretch.automation.formatter.qaf_report.step.checkpoint import CheckPoint
import os
from infostretch.automation.formatter.qaf_report.step.sub_check_points import SubCheckPoints
from infostretch.automation.ui.webdriver import base_driver
from infostretch.automation.core.message_type import MessageType


class Reporter:
    """
    This class will handle log event
    """

    def add_check_point(self, message, message_type, screen_shot=''):
        check_point = CheckPoint()
        check_point.message = message
        check_point.type = message_type
        check_point.screenshot = screen_shot
        SubCheckPoints().add_check_point(check_point)

    @staticmethod
    def log(message, message_type=MessageType.Info):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log
            message_type (int): Message type

        Returns:
            None
        """
        Reporter().add_check_point(message, message_type)

    @staticmethod
    def info(message):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log

        Returns:
            None
        """
        Reporter().add_check_point(message, MessageType.Info)

    @staticmethod
    def debug(message):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log

        Returns:
            None
        """
        Reporter().add_check_point(message, MessageType.Info)

    @staticmethod
    def error(message):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log

        Returns:
            None
        """
        Reporter().add_check_point(message, MessageType.Fail)

    @staticmethod
    def critical(message):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log

        Returns:
            None
        """
        Reporter().add_check_point(message, MessageType.Warn)

    @staticmethod
    def warn(message):
        """
        Log message into log file.

        Args:
            message (str): Message needs to be log

        Returns:
            None
        """
        Reporter().add_check_point(message, MessageType.Warn)

    @staticmethod
    def log_with_screenshot(message, message_type=MessageType.Info):
        filename = os.path.join(os.getenv('REPORT_DIR'), 'img', str(uuid.uuid4()) + '.png')
        base_driver.BaseDriver().get_driver().save_screenshot(filename=filename)
        Reporter().add_check_point(message, message_type, screen_shot=filename)
