from infostretch.automation.core.resources_manager import ResourcesManager
from infostretch.automation.util.locator_util import LocatorUtil


class ProjectEnvironment:
    """
    This class will set up application properties, locators, etc.
    """

    @staticmethod
    def set_up():
        """
        This method will initialise the application properties and locators storage file.

        Returns:
            None
        """
        ResourcesManager().set_up()
        LocatorUtil().load_locators()
