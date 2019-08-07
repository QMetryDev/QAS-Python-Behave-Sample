import os
import plistlib
from configparser import ConfigParser, ExtendedInterpolation
from infostretch.automation.core.configurations_manager import ConfigurationsManager


class LocatorUtil:
    """
    This class will load all locators stored in ini of plist files as per the channel name
    and save key-value pairs in configurations manager.
    """

    def load_locators(self):
        """
        This method will load ini and plist file as per the channel name.

        Returns:
            None
        """
        if ConfigurationsManager().contains_key('channel'):
            channel = ConfigurationsManager().get_str_for_key('channel')
            resource_dir_path = os.path.join('resources', channel)

            if os.path.exists(resource_dir_path):
                for root, dirs, files in os.walk(resource_dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        extension = os.path.splitext(file)[1]
                        if extension == '.ini':
                            self.__load_ini_file(file_path)
                        elif extension == '.plist':
                            self.__load_plist_file(file_path)

    @staticmethod
    def __load_ini_file(file_path):
        """
        This method will load key-value pairs store in ini file and stores them in configuration manager.

        Args:
            file_path(str): Path of ini file.

        Returns:
            None
        """
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(file_path)

        for each_section in config.sections():
            for key, value in config.items(each_section):
                ConfigurationsManager().set_object_for_key(value=value, key=key)

    @staticmethod
    def __load_plist_file(file_path):
        """
        This method will load key-value pairs store in plist file and stores them in configuration manager.

        Args:
            file_path(str): Path of plist file.

        Returns:
            None
        """
        with open(file_path, 'rb') as fp:
            _dict = plistlib.load(fp)

        for key, value in _dict.items():
            ConfigurationsManager().set_object_for_key(value=value, key=key)
