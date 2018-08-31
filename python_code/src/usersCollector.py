# usersCollector.py
# Created by James Todd
# Date: 9/16/2017
# Purpose: This class will contain all of the tools necessary to collect a given repository's users data

import os
import time
import github
import researchToolkit
from logger import Logger
from targetManager import TargetManager

HOME_PATH = os.getcwd()
targetManager = TargetManager(HOME_PATH)
IMPORTANT_TEXT_PATH = targetManager.get_important_text_files_path()
INFO_LOGGER = Logger(IMPORTANT_TEXT_PATH, "INFO_LOG", "INFO")
ERROR_LOGGER = Logger(IMPORTANT_TEXT_PATH, "ERROR_LOG", "ERROR")

MERGED = "closed_merged"
UNMERGED = "closed_unmerged"
OPEN = "open"


def run_collector(repo):
    try:
        start_time = time.time()
        # get the users of a repo in to a set!!

        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to gather User data from pull request data" +
                                 get_time_string(start_time))
        user_ID_set = researchToolkit.get_user_ID_set_from_repo(repo)

        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished to gather User data from pull request data" +
                                 get_time_string(start_time))

        INFO_LOGGER.write_to_log(
            Logger.add_tabs(1) + "Starting to gather User data from Github. There are " +
            str(len(user_ID_set)) + " users" + get_time_string(start_time))

        github.download_user_data(user_ID_set, repo)

        INFO_LOGGER.write_to_log(
            Logger.add_tabs(1) + "Finished gathering User data from Github" + get_time_string(start_time))
        # once in the set down lode them in to that repos jsons users folder

        INFO_LOGGER.write_to_log(
            Logger.add_tabs(1) + "Starting to write User CSV for the REPO" + get_time_string(start_time))
        user_CSV_data = researchToolkit.get_user_data_CSV_file_for(user_ID_set, repo)

        researchToolkit.write_user_data_as_csv(user_CSV_data, repo)

        INFO_LOGGER.write_to_log(
            Logger.add_tabs(1) + "Finished to write User CSV for the REPO" + get_time_string(start_time))
        # make the user CSV for that repo where it needs to go!3
        return
    except Exception as error:
        ERROR_LOGGER.write_to_log("UserCollector had an error " + str(error) + " with this repo " + str(repo))



#run_collector("/php/php-src")
def get_time_string(start_time):
    return "   " + str(format(float((time.time() - start_time)), "0.4f") + " (sec)   ") + str(format(float((time.time() - start_time) / 60), "0.4f")) + " (min)"
