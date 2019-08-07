import os
import plistlib
from configparser import ConfigParser, ExtendedInterpolation
from infostretch.automation.core.configurations_manager import ConfigurationsManager
import configparser


class ResourcesManager:
    defaultLanguage = None
    """
    This class will load application properties and save values in configurations manager.
    """
    def set_up(self):
        """
        Load Application Properties

        Returns:
            None
        """
        if os.path.exists('resources/application.properties'):
            self.__load_properties_file(self, 'resources/application.properties')
            # config = ConfigParser(interpolation=ExtendedInterpolation())
            # config.read('application.properties')

            # for each_section in config.sections():
            #   for each_key, each_val in config.items(each_section):
            #     ConfigurationsManager().set_object_for_key(value=each_val, key=each_key)
            if ResourcesManager.defaultLanguage is None and ConfigurationsManager().get_str_for_key('env.default.locale') is not None:
                ResourcesManager.defaultLanguage = str(
                    ConfigurationsManager().get_str_for_key('env.default.locale'))
            envResources = str(
                ConfigurationsManager().get_str_for_key('env.resources'))
            commaSeparatedValues = envResources.split(';')
            self.__load_resources(commaSeparatedValues)

    def __load_resources(self, default_browser):
        # #print("channel_list::"+de )
        print("Will load >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",ResourcesManager.defaultLanguage)
        for x in default_browser:
            for dirpath, dirs, files in os.walk(x):
                for file in files:
                    fname = os.path.join(dirpath, file)
                    extension = os.path.splitext(fname)[1]
                    if extension == '.properties':
                        self.__load_properties_file(
                            self, fname)
                    elif extension == '.loc':
                        self.__load_properties_file(
                            self, fname)
                    elif extension == '.wsc':
                        self.__load_properties_file(
                            self, fname)
                    elif ResourcesManager.defaultLanguage is not None and extension == '.'+ResourcesManager.defaultLanguage:
                         self.__load_properties_file(
                             self, fname)

    def load_directory(self, default_browser):
        # #print("channel_list::"+de )
        default_lang="."+str(defaultLanguage)
        for x in default_browser:
            for dirpath, dirs, files in os.walk(x):
                for file in files:
                    fname = os.path.join(dirpath, file)
                    extension = os.path.splitext(fname)[1]
                    if extension == '.properties':
                        #print("fileName:"+fname)
                        self.__load_properties_file(
                            self, fname)
                    elif extension == '.loc':
                        #print("fileName:"+fname)
                        self.__load_properties_file(
                            self, fname)
                    elif extension == '.wsc':
                        #print("fileName:"+fname)
                        self.__load_properties_file(
                            self, fname)
                    elif ResourcesManager.defaultLanguage is not None and extension == '.'+ResourcesManager.defaultLanguage:
                         self.__load_properties_file(
                             self, fname)

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
                ConfigurationsManager().set_object_for_key(key=key, value=value)

    @staticmethod
    def load_properties(filepath, sep='=', comment_char='#'):
        props = {}
        with open(filepath, "rt",encoding="UTF-8") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props

    # @staticmethod
    # def loads_props(filepath):
    #    return H = dict(line.strip().split('=') for line in open(filepath))

    @staticmethod
    def __load_properties_file(self, file_path):
        """
        This method will load key-value pairs store in plist file and stores them in configuration manager.

        Args:
            file_path(str): Path of plist file.

        Returns:
            None
        """
        #print("inside __load_properties_file()")
        _dict = self.load_properties(file_path, "=", "#")

        for key, value in _dict.items():
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
