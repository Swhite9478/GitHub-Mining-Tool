import datetime
import os
from targetManager import TargetManager
HOME_PATH = os.getcwd()
targetManager = TargetManager(HOME_PATH)

class Logger:
    def __init__(self, home_path, log_name, log_level):
        self.HOME_PATH = str(home_path)
        self.LOG_NAME = str(log_name) + "_" + str(datetime.date.today())
        self.LOG_LEVEL = str(log_level)
        self.OLD_DIRECTORY = str()

    def set_up_log_file(self):
        Logger._change_to_log_location(self)
        file = open(str(self.LOG_NAME) + ".log", 'w')
        file.close()
        Logger._change_back_to_calling_directory(self)

    def _change_to_log_location(self):
        self.OLD_DIRECTORY = os.getcwd()
        os.chdir(self.HOME_PATH)


    def _change_back_to_calling_directory(self):
        os.chdir(self.OLD_DIRECTORY)

    def write_to_log(self, message):
        Logger._change_to_log_location(self)
        Logger._write_log_message(self, message)
        Logger._change_back_to_calling_directory(self)

    def _write_log_message(self, message):
        file = open(self.LOG_NAME + ".log", 'a')
        file.write(self.LOG_LEVEL + ": " + message + "\n")
        file.close()

    @staticmethod
    def add_tabs(number_of_tabs):
        returning_string = str()
        for step in range(number_of_tabs):
            returning_string = returning_string + "\t"
        return returning_string