# targetCreator.py
# Created by Stephen White
# Date: 7/30/2017
# Purpose: This program will initialize the Target Directory structure by generating the collected_repos.txt file, and
#          populating the Target directory with the proper folders for each repository

from termcolor import colored
import github
import targetManager
import os

REPO_CAP = 200


def create_populated_target_structure():
    # Set up the Target structure that is needed to complete the research
    if not targetManager.target_tree_exists(targetManager.get_subdirectories()):
        print(colored("\n\n~Creating file structure~", 'blue'))
        targetManager.create_target_directory_structure()
        github.get_repositories(REPO_CAP)

    repo_path = os.path.join(targetManager.get_collected_repos_path(), "collected_repos.txt")

    # open the collected repos text file for parsing
    repo_lines = list(
        map(str.strip, open(repo_path, 'r').readlines()))  # strip all \n and place each line in a list

    # Ensure that all repos have been properly collected
    if not repo_lines[0] == repo_lines[-1]:
        # noinspection PyTypeChecker
        quit("\n**Not all repositories collected. Program terminated**")
    else:
        for repo in repo_lines:
            if not repo.startswith("/"):
                continue
            else:
                targetManager.create_repo_subdirectories(repo)
