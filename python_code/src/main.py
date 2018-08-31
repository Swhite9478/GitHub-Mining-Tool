# main.py
# Created by Stephen White
# Date: 7/30/2017
# Purpose: Once this script is run, the end goal is to to have all relevant information be placed in the Target
#          file structure for analysis. This program will make use of any and all tool kits/scripts created by
#          the research group.
import os
import time
import pullRequestCollector
from targetManager import TargetManager
from logger import Logger
import usersCollector
import combineAllPullRequestCSVs as csvCombiner
import commitCollector

HOME_PATH = os.getcwd()
targetManager = TargetManager(HOME_PATH)
targetManager.create_target_directory_structure()
collected_repos_path = os.path.join(targetManager.get_collected_repos_path(), "collected_repos.txt")
IMPORTANT_TEXT_PATH = targetManager.get_important_text_files_path()

INFO_LOGGER = Logger(IMPORTANT_TEXT_PATH, "INFO_LOG", "INFO")
INFO_LOGGER.set_up_log_file()

ERROR_LOGGER = Logger(IMPORTANT_TEXT_PATH, "ERROR_LOG", "ERROR")
ERROR_LOGGER.set_up_log_file()

start = time.time()
timeList = []

# open the collected repos text file for parsing
repo_lines = list(
    map(str.strip, open(collected_repos_path, 'r').readlines()))  # strip all \n and place each line in a list

# Ensure that all repos have been properly collected
for repo in repo_lines:
    innerStart = time.time()
    try:
        if not repo.startswith("/"):
            continue
        else:
            INFO_LOGGER.write_to_log("Starting REPO (Pull requests) " + Logger.add_tabs(1) + repo)
            targetManager.create_repo_subdirectories_for(repo)
            pullRequestCollector.run_collector(repo)
            usersCollector.run_collector(repo)
            commitCollector.run_collector(repo)
            INFO_LOGGER.write_to_log(Logger.add_tabs(1) +"The REPO finished (Pull requests)   " +
                                     str(format(float((time.time() - innerStart)), "0.4f")) + " (sec)   " + str(format(float((time.time() - innerStart) / 60), "0.4f") + " (min)\n"))
    except Exception as error:
        ERROR_LOGGER.write_to_log("This REPO " + str(repo) + " has this error " + str(error) + " THE METHOD CALLER IS MAIN")
# csvCombiner.combine_all_pr_csvs()