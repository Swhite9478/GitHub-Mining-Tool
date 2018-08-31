# usersCollector.py
# Created by James Todd
# Date: 8/5/2018
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
        # Set up dictionaries that will store the urls of the pull requests collected
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to gather commit ids" + get_time_string(start_time))
        open_list, merged_list, unmerged_list = researchToolkit.get_IDs_for_repo_pull_request(repo)
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished gathering commit ids" + get_time_string(start_time))

        # Generate the id folders from the requested pull_ids
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to make id folders" + get_time_string(start_time))
        researchToolkit.create_commit_id_folders(repo, open_list, OPEN)
        researchToolkit.create_commit_id_folders(repo, merged_list, MERGED)
        researchToolkit.create_commit_id_folders(repo, unmerged_list, UNMERGED)
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished making id folders" + get_time_string(start_time))

        # set up and call the threads
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to download JSON" + get_time_string(start_time))
        github.download_commit_level_jsons(repo)
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished downloading JSON" + get_time_string(start_time))

        # Parse the downloaded main_pull.json files and create a pull_request dictionary, then refine it.
        INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to make the CSVs" + get_time_string(start_time))

        '''
            step 3 download the commits
        '''

        '''
            step 4, make csvs
        '''

        '''
            log every thing 
        '''


        return
    except Exception as error:
        ERROR_LOGGER.write_to_log("commitCollector had an error " + str(error) + " with this repo " + str(repo))


#run_collector("/php/php-src")
def get_time_string(start_time):
    return "   " + str(format(float((time.time() - start_time)), "0.4f") + " (sec)   ") + str(format(float((time.time() - start_time) / 60), "0.4f")) + " (min)"
