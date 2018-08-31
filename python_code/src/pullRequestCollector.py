# pullRequestCollector.py
# Created by Stephen White
# Contributor James Todd
# Date: 7/31/2017
# Purpose: This class will contain all of the tools necessary to collect a given repository's pull request data

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
MERGED = "closed_merged"
UNMERGED = "closed_unmerged"
OPEN = "open"

'''Program entry point'''
def run_collector(repo):
    start_time = time.time()
    # Set up dictionaries that will store the urls of the pull requests collected
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to gather pull ids" + get_time_string(start_time))
    closed_merged_pull_ids = github.git_pull_ids_merged(repo)
    closed_unmerged_pull_ids = github.git_pull_ids_unmerged(repo)
    open_pull_ids = github.git_pull_ids_open(repo)
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished gathering pull ids" + get_time_string(start_time))

    # Generate the id folders from the requested pull_ids
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to make id folders" + get_time_string(start_time))
    researchToolkit.create_pull_request_id_folders(repo, closed_merged_pull_ids, MERGED)
    researchToolkit.create_pull_request_id_folders(repo, closed_unmerged_pull_ids, UNMERGED)
    researchToolkit.create_pull_request_id_folders(repo, open_pull_ids, OPEN)
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished making id folders" + get_time_string(start_time))

    #set up and call the threads
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to download JSON" + get_time_string(start_time))
    github.download_pull_requests(repo)
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished downloading JSON" + get_time_string(start_time))

    # Parse the downloaded main_pull.json files and create a pull_request dictionary, then refine it.
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to make the CSVs" + get_time_string(start_time))
    pr_dict_stage_01 = researchToolkit.get_pull_request_dictionary_stage_01(repo)
    pr_dict_stage_02 = researchToolkit.get_pull_request_dictionary_stage_02(pr_dict_stage_01)
    pr_dict_stage_03 = researchToolkit.get_pull_request_dictionary_stage_03(pr_dict_stage_02)
    pr_dict_drive_by_author = researchToolkit.get_drive_by_author_dictionary(pr_dict_stage_02)
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished making the CSVs" + get_time_string(start_time))

    # Write all parsed information into three separate csv files, so no data is lost
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Starting to write the CSVs files" + get_time_string(start_time))
    researchToolkit.write_all_stage_01_pr_dictionary_csv_files(repo, pr_dict_stage_01)
    researchToolkit.write_all_stage_02_pr_dictionary_csv_files(repo, pr_dict_stage_02)
    researchToolkit.write_all_stage_03_pr_dictionary_csv_files(repo, pr_dict_stage_03)
    researchToolkit.write_all_drive_by_pr_dictionary_csv_files(repo, pr_dict_drive_by_author)
    INFO_LOGGER.write_to_log(Logger.add_tabs(1) + "Finished writing the CSVs files" + get_time_string(start_time))
    return

def print_dict(pr_dict, pull_state):
    print("========================================")
    print(pull_state + ":")
    for item in pr_dict[pull_state]:
        print("\t" + str(item))
    print("========================================")

def get_time_string(start_time):
    return "   " + str(format(float((time.time() - start_time)), "0.4f") + " (sec)   ") + str(format(float((time.time() - start_time) / 60), "0.4f")) + " (min)"