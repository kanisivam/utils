import os
import ConfigParser


class Singleton(type):
    """
    This singleton class can be used , to mark an another class as singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class ConfigReader(object):
    """
    Reads the config file for configurable parameters..
    Config file path can be taken from user input or from
    current directory.
    """
    __metaclass__ = Singleton  ### make it singleton class

    def __init__(self, ini_files):
        """
        One or more ini_files to be read
        :param ini_files: config input file
        """
        self.ini_files = ini_files
        if not os.path.exists(ini_files):
            raise Exception(ini_files + " doesn't exists.")
        self.all_config = {}
        self.read()

    def read(self):
        """
        Read all the *.ini files available in the given path or current directory
        :raise: Exception while parsing the config file
        """
        if os.path.isfile(self.ini_files):
            self.all_config = self.readfile(self.ini_files)
        elif os.path.isdir(self.ini_files):
            for ini_file in os.listdir(self.ini_files):
                if ini_file.endswith(".ini"):
                    try:
                        current_configs = self.readfile(os.path.join(os.path.abspath(self.ini_files), ini_file))
                        self.all_config.update(current_configs)
                    except Exception as e:
                        print e
        else:
            raise Exception("invalid input neither directory nor files")
        if len(self.all_config) == 0:
            raise Exception(self.ini_files + ", doesn't have proper inputs")

    @staticmethod
    def readfile(ini_file):
        """
        Read the config file for configurable parameters.
        Read Config from the given path.
        :param ini_file:configuration input file for script
        :return: inputs - sections values pair
        """
        config = ConfigParser.ConfigParser()
        config.read(ini_file)
        inputs = {}
        for section in config.sections():
            inputs[section] = {}
            for option, value in config.items(section):
                inputs[section][option] = value
        return inputs

    def get_config(self, section):
        """
        get name value for the given section from the config file
        :param section: - pass section to get name value pair
        :return: name value pair for the given section
        """
        if section in self.all_config:
            return self.all_config[section]



