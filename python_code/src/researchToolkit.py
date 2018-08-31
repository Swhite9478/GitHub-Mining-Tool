# researchToolkit.py
# Concept by Stephen White
# Written by Stephen White
# Contributor James Todd
# Date: 6/29/2017
#
# Purpose: Create a toolkit that will allow for assistance in undergraduate research.

from operator import itemgetter
from bs4 import BeautifulSoup
import requests
import shutil
import json
import time
import csv
import os
from targetManager import TargetManager
from logger import Logger

targetManager = TargetManager(os.getcwd())
IMPORTANT_TEXT_PATH = targetManager.get_important_text_files_path()
INFO_LOGGER = Logger(IMPORTANT_TEXT_PATH, "INFO_LOG", "INFO")
ERROR_LOGGER = Logger(IMPORTANT_TEXT_PATH, "ERROR_LOG", "ERROR")

GH_USER = "Githubfake01"  # your github username
GH_PASSWD = "5RNsya*z#&aA"  # your github passwd

MERGED = "closed_merged"
UNMERGED = "closed_unmerged"
OPEN = "open"

FIRST = 0
SECOND = 1
THIRD = 2
ONE = 1

# -------------------------------------------------------------------------------------------------------------------- #
''' This section of code is responsible for finding all relevant info on COMMIT NUMBERS of a given repo.'''


# determine how many total commits comprise a given repository
def calculate_number_of_total_commits(repo_text):
    url = "https://github.com%s" % repo_text
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)  # get the webpage information
    soup = BeautifulSoup(page.content, 'html.parser')  # We are now going to parse the html of this page
    print("PAGE STATUS CODE: %s" % page.status_code)
    time.sleep(2)  # Force the program to slow execution as to avoid being "mistaken" for a bot

    # Find the number of commits from the website, and remove all whitespace, tabs, and new lines to create an int
    for item in soup.find('span', class_="num text-emphasized"):
        num_commits = int("".join(str(item.split('\n')[1]).strip(" ").split(',')))
    return num_commits


# determine how many pages of commits need to be parsed through to get all commits
def calculate_number_of_commit_pages(commit_number):
    commit_pages = abs(-commit_number // 100)
    return int(commit_pages)


# -------------------------------------------------------------------------------------------------------------------- #
''' This section of code is responsible for finding the total number of CONTRIBUTORS to a project.'''


# determine the total number of contributors that comprise a given repository
def calculate_number_of_total_contributors(repo_text):
    url = "https://github.com%s" % repo_text
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)  # get the webpage information
    soup = BeautifulSoup(page.content, 'html.parser')  # We are now going to parse the html of this page
    print("PAGE STATUS CODE: %s" % page.status_code)
    time.sleep(2)  # Force the program to slow execution as to avoid being "mistaken" for a bot

    # Find the number of commits from the website, and remove all whitespace, tabs, and new lines to create an int
    for item in soup.find_all('span', class_="num text-emphasized")[3]:
        num_contrib = int("".join(str(item.split('\n')[1]).strip(" ").split(',')))
    return num_contrib


# -------------------------------------------------------------------------------------------------------------------- #
''' This section of code is responsible for managing this toolkit's COMMIT DICTIONARIES.'''


# Search through ONE GitHub JSON page and collect only new commits, but also count the number of commits each
# person has made so we can filter later
def gather_author_dictionary(author_dict, file_name):
    # Open the json file for reading so we can access its information
    with open(file_name, 'r') as file:
        data = json.load(file)
        keys = author_dict.keys()  # Obtain every key in this dictionary for comparison

        for item in data:  # Look for repos we have already found, only add new repos
            count = 1
            author = str(item["commit"]["author"]["name"]).lower()
            email = str(item["commit"]["author"]["email"]).lower()

            # in the event that an author does not have an associated id, set it equal to None
            try:
                author_id = item["author"]["id"]
            except Exception as e:
                author_id = None

            my_list = [author, author_id, count]  # Save relevant information in association with this email address
            if email not in keys:
                author_dict.update({email: my_list})  # Add any new repos
            else:
                author_dict[email][2] = (author_dict[email][2] + 1)  # otherwise, keep track of each commit
                continue

    return author_dict  # Return the dictionary with pertinent information


# Refine a commit dictionary passed into this method, and return a dictionary that only contains drive by commits
def refine_commit_dictionary(old_commit_dict):
    new_dict = dict()
    for email in old_commit_dict:
        if old_commit_dict[email][2] == 1:  # Check the commit count for this author, only accept "1"
            new_dict.update({email: old_commit_dict[email]})
        else:
            continue
    return new_dict


# Take in a commit dictionary and create a csv file to a given location
def create_commit_dictionary_csv_file(file_path, dictionary):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')

        # Loop through the dictionary and appropriately add each key and value in on row, separated by columns
        for email in dictionary:
            name = str(dictionary[email][0])
            git_id = str(dictionary[email][1])
            commits = str(dictionary[email][2])
            string = str(email) + "," + name + "," + git_id + "," + commits
            writer.writerow([string])

    return  # Nothing to return here


def create_pull_id_dictionary_csv_file(file_path, pull_ids):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')

        # Loop through the dictionary and appropriately add each key and value in on row, separated by columns
        for pull_id in pull_ids:
            writer.writerow(str(pull_id))

    return  # Nothing to return here


# -------------------------------------------------------------------------------------------------------------------- #
''' This section of code is responsible for managing this toolkit's PULL REQUEST DICTIONARIES.'''


def create_pull_request_id_folders(repo, pull_ids, pull_type):
    print("\nCreating %s Pull ID folders. This may take a few moments..." % str(
        pull_type).upper())  # Let the user know what is happening
    targetManager.delete_all_open_pull_id_subdirectories_for(repo)

    # Write every id we have collected as a folder
    for pull_id in range(len(pull_ids) - 1, -1, -1):
        if pull_type == "closed_merged":
            targetManager.create_repo_merged_pull_id_directory_for(repo, str(pull_ids[pull_id]))

        elif pull_type == "closed_unmerged":
            targetManager.create_repo_unmerged_pull_id_directory_for(repo, str(pull_ids[pull_id]))

        else:
            targetManager.create_repo_open_pull_id_directory_for(repo, str(pull_ids[pull_id]))
    print("%s Pull ID folders successfully created." % str(pull_type).upper())  # Let the user know what is happening


# Pass in the repo and return a dictionary whose keys are the pull request type (merged, unmerged, & open) and whose
# values are dictionaries that contain
def get_pull_request_dictionary_stage_01(repo):
    print("\n\nGetting stage_01 pull request dictionary")
    open_list = []
    merged_list = []
    unmerged_list = []
    pull_request_dictionary = {OPEN: open_list,
                               MERGED: merged_list,
                               UNMERGED: unmerged_list
                               }
    get_open_pull_id_list_for_pull_id_dictionary(repo, open_list)
    get_merged_pull_id_list_for_pull_id_dictionary(repo, merged_list)
    get_unmerged_pull_id_list_for_pull_id_dictionary(repo, unmerged_list)
    print("Stage_01 pull request dictionary obtained")
    print(open_list)
    print(merged_list)
    print(unmerged_list)
    return pull_request_dictionary


def get_open_pull_id_list_for_pull_id_dictionary(repo, open_list):
    open_pull_id_subdirectories = targetManager.get_full_subdirectory_paths_list_from(
        targetManager.get_json_pulls_open_file_path_to(repo))
    stripped_repo = targetManager.strip_slashes_from_repository_string(repo)
    for open_pull_id in open_pull_id_subdirectories:
        with open(os.path.join(open_pull_id, "main_pull.json"), 'r') as open_pull_id_main_json_file:
            data = json.load(open_pull_id_main_json_file)
            pull_list = [data["user"]["login"], data["user"]["id"], stripped_repo, data["number"], data["state"],
                         data["created_at"], data["closed_at"], data["review_comments"], data["commits"],
                         data["additions"], data["deletions"], data["changed_files"]]
            open_list.append(pull_list)
            open_pull_id_main_json_file.close()


def get_merged_pull_id_list_for_pull_id_dictionary(repo, merged_list):
    merged_pull_id_subdirectories = targetManager.get_full_subdirectory_paths_list_from(
        targetManager.get_json_pulls_merged_file_path_to(repo))
    stripped_repo = targetManager.strip_slashes_from_repository_string(repo)
    for merged_pull_id in merged_pull_id_subdirectories:
        with open(os.path.join(merged_pull_id, "main_pull.json"), 'r') as merged_pull_id_main_json_file:
            data = json.load(merged_pull_id_main_json_file)
            pull_list = [data["user"]["login"], data["user"]["id"], stripped_repo, data["number"], (data["state"] + "-merged"),
                         data["created_at"], data["closed_at"], data["review_comments"], data["commits"],
                         data["additions"], data["deletions"], data["changed_files"]]
            merged_list.append(pull_list)
            merged_pull_id_main_json_file.close()


def get_unmerged_pull_id_list_for_pull_id_dictionary(repo, unmerged_list):
    unmerged_pull_id_subdirectories = targetManager.get_full_subdirectory_paths_list_from(
        targetManager.get_json_pulls_unmerged_file_path_to(repo))
    stripped_repo = targetManager.strip_slashes_from_repository_string(repo)
    for unmerged_pull_id in unmerged_pull_id_subdirectories:  # unmerged_pull_id)
        with open(os.path.join(unmerged_pull_id, "main_pull.json"), 'r') as unmerged_pull_id_main_json_file:
            data = json.load(unmerged_pull_id_main_json_file)
            pull_list = [data["user"]["login"], data["user"]["id"], stripped_repo, data["number"], (data["state"] + "-unmerged"),
                         data["created_at"], data["closed_at"], data["review_comments"], data["commits"],
                         data["additions"], data["deletions"], data["changed_files"]]
            unmerged_list.append(pull_list)
            unmerged_pull_id_main_json_file.close()


# Pass in the generalized dictionary, and refine it to see each person's PR status ONLY ONCE
def get_pull_request_dictionary_stage_02(pr_dict_stage_01):
    print("\nGetting stage_02 pull request dictionary")
    # Update all of the PR lists through the use of a helper method
    open_list = get_refined_list_for_pull_request_dictionary_stage_02(pr_dict_stage_01, OPEN)
    merged_list = get_refined_list_for_pull_request_dictionary_stage_02(pr_dict_stage_01, MERGED)
    unmerged_list = get_refined_list_for_pull_request_dictionary_stage_02(pr_dict_stage_01, UNMERGED)

    pr_dict_stage_02 = {OPEN: open_list,
                        MERGED: merged_list,
                        UNMERGED: unmerged_list
                        }
    print("Stage_02 pull request dictionary obtained")
    return pr_dict_stage_02


# Final refinement method for pull request dictionary. Shrink down the previously refined dictionary into data that
# displays what number of developers have made how many of each type of pull request. (EX: 1 dev has 222 PR's, etc.)
def get_pull_request_dictionary_stage_03(pr_dict_stage_02):
    print("\nGetting stage_03 pull request dictionary")
    open_list = refine_pull_list_to_stage_03(pr_dict_stage_02[OPEN])
    merged_list = refine_pull_list_to_stage_03(pr_dict_stage_02[MERGED])
    unmerged_list = refine_pull_list_to_stage_03(pr_dict_stage_02[UNMERGED])

    final_dict = {OPEN: open_list,
                  MERGED: merged_list,
                  UNMERGED: unmerged_list
                  }
    print("Stage_03 pull request dictionary obtained")
    return final_dict


# get the drive by author dictionary from the stage 2 data for OPEN, MERGED, and UNMERGED
def get_drive_by_author_dictionary(pr_dict_stage_02):
    print("\nGetting drive by pull request dictionary")
    open_list = get_refined_drive_by_author_dictionary(pr_dict_stage_02[OPEN])
    merged_list = get_refined_drive_by_author_dictionary(pr_dict_stage_02[MERGED])
    unmerged_list = get_refined_drive_by_author_dictionary(pr_dict_stage_02[UNMERGED])

    drive_by_dict = {OPEN: open_list,
                     MERGED: merged_list,
                     UNMERGED: unmerged_list
                     }
    print("Drive by pull request dictionary obtained")
    return drive_by_dict


# HELPER METHOD this helper method will me a list of a list.  The inner lists will have two
#               values, author name and author ID respectively.
def get_refined_drive_by_author_dictionary(dictionary):
    refine_list = []

    for value in dictionary:
        if value[THIRD] == ONE:
            refine_list.append([value[FIRST], value[SECOND]])

    return refine_list


# HELPER METHOD to Pass in the generalized_dict and pull type to shrink the massive pull request dictionary down to
#               simply each contributor's name once, and the number of PR's they have of that state
def get_refined_list_for_pull_request_dictionary_stage_02(pr_dict_stage_01, pull_type):
    generic_list = list()
    list_name = []
    for author in pr_dict_stage_01[pull_type]:
        generic_list.append(author[0] + ":" + str(author[1]))
    generic_list = list(set(generic_list))
    temp_dict = {}
    for item in generic_list:
        temp_dict.update({item.split(":")[0]: [int(item.split(":")[1]), 0]})

    d_keys = temp_dict.keys()
    for author in pr_dict_stage_01[pull_type]:
        if author[0] in d_keys:
            temp_dict[author[0]][1] += 1

    for key in temp_dict:
        sub_list = [key]
        for value in temp_dict[key]:
            sub_list.append(value)
        list_name.append(sub_list)

    return sorted(list_name, key=itemgetter(2, 0, 1), reverse=True)


# HELPER METHOD to assist in the final refinement of the pull request dictionary structure
def refine_pull_list_to_stage_03(refined_list):
    final_dict = {}
    final_list = []

    for element in refined_list:
        final_dict.update({element[2]: 0})

    for element in refined_list:
        final_dict[element[2]] += 1

    for element in final_dict:
        final_list.append([final_dict[element], element])

    return sorted(final_list, key=itemgetter(0))


# Method which will write the contents of the generic PR author dictionary to a csv file
def write_single_stage_01_pr_dictionary_as_csv(repo, pr_dict_stage_01, pull_state):
    # file_path = targetManager.get_pull_request_level_csv_subdirectory_for(repo)
    if pull_state == MERGED:
        file_path = targetManager.join_path(targetManager.get_merged_pull_request_level_subdirectory_for(repo),
                    ("stage_01_pull_requests_" + pull_state + ".csv"))
    elif pull_state == UNMERGED:
        file_path = targetManager.join_path(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo),
                    ("stage_01_pull_requests_" + pull_state + ".csv"))
    else:
        file_path = targetManager.join_path(targetManager.get_open_pull_request_level_subdirectory_for(repo),
                    ("stage_01_pull_requests_" + pull_state + ".csv"))

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        descriptors = "GITHUB USERNAME,GITHUB ID,REPO,PR#,PR STATE,DATE CREATED,DATE CLOSED,# REVIEW COMMENTS," \
                      "# COMMITS,# ADDITIONS,# DELETIONS,# FILES CHANGED"
        writer.writerow([descriptors])

        for element in pr_dict_stage_01[pull_state]:
            string = ""
            for pull_request_info in element:
                string += (str(pull_request_info) + ",")
            writer.writerow([string])

    csvfile.close()
    return

# HELPER METHOD: will write the contents of a refined PR author dictionary to a csv file
def write_single_stage_02_pr_dictionary_as_csv(repo, pr_dict_stage_02, pull_state):
    if pull_state == MERGED:
        title = ",MERGED PRs"
        file_path = targetManager.join_path(targetManager.get_merged_pull_request_level_subdirectory_for(repo),
                    ("stage_02_pull_requests_" + pull_state + ".csv"))
    elif pull_state == UNMERGED:
        title = ",UNMERGED PRs"
        file_path = targetManager.join_path(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo),
                    ("stage_02_pull_requests_" + pull_state + ".csv"))
    else:
        title = ",OPEN PRs"
        file_path = targetManager.join_path(targetManager.get_open_pull_request_level_subdirectory_for(repo),
                    ("stage_02_pull_requests_" + pull_state + ".csv"))

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        writer.writerow([title])
        descriptors = "DEVELOPER,,GITHUB ID,,#PULLS"
        writer.writerow([descriptors])

        for element in pr_dict_stage_02[pull_state]:
            string = str(element[0]) + ",," + str(element[1]) + ",," + str(element[2])
            writer.writerow([string])

    csvfile.close()
    return


# HELPER METHOD: will write the contents of a final PR dictionary key to a csv file
def write_single_stage_03_pr_dictionary_as_csv(repo, pr_dict_stage_03, pull_state):
    if pull_state == MERGED:
        title = ",MERGED PRs"
        file_path = targetManager.join_path(targetManager.get_merged_pull_request_level_subdirectory_for(repo),
                    ("stage_03_pull_requests_" + pull_state + ".csv"))
    elif pull_state == UNMERGED:
        title = ",UNMERGED PRs"
        file_path = targetManager.join_path(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo),
                    ("stage_03_pull_requests_" + pull_state + ".csv"))
    else:
        title = ",OPEN PRs"
        file_path = targetManager.join_path(targetManager.get_open_pull_request_level_subdirectory_for(repo),
                    ("stage_03_pull_requests_" + pull_state + ".csv"))

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        writer.writerow([title])
        descriptors = "#Devs,,#PULLS"
        writer.writerow([descriptors])

        for element in pr_dict_stage_03[pull_state]:
            string = str(element[0]) + ",," + str(element[1])
            writer.writerow([string])

    csvfile.close()
    return


# HELPER METHOD: will write the contents of a final PR dictionary key to a csv file
def write_single_drive_by_pr_dictionary_as_csv(repo, pr_dict_drive_by_author, pull_state):
    if pull_state == MERGED:
        title = ",MERGED PRs"
        file_path = targetManager.join_path(targetManager.get_merged_pull_request_level_subdirectory_for(repo),
                    ("drive_by_pull_requests_" + pull_state + ".csv"))
    elif pull_state == UNMERGED:
        title = ",UNMERGED PRs"
        file_path = targetManager.join_path(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo),
                    ("drive_by_pull_requests_" + pull_state + ".csv"))
    else:
        title = ",OPEN PRs"
        file_path = targetManager.join_path(targetManager.get_open_pull_request_level_subdirectory_for(repo),
                    ("drive_by_pull_requests_" + pull_state + ".csv"))
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        writer.writerow([title])
        descriptors = "#Devs,,ID_Number"
        writer.writerow([descriptors])

        for element in pr_dict_drive_by_author[pull_state]:
            string = str(element[FIRST]) + ",," + str(element[SECOND])
            writer.writerow([string])

    csvfile.close()
    return


# Write every pull state of the pr_dict_stage_01 to separate CSV files all in one method call
def write_all_stage_01_pr_dictionary_csv_files(repo, pr_dict_stage_01):
    print("\n\nWriting stage_01 pull request dictionary to csv files...")
    if len(pr_dict_stage_01[OPEN]) != 0:
        write_single_stage_01_pr_dictionary_as_csv(repo, pr_dict_stage_01, OPEN)
    if len(pr_dict_stage_01[MERGED]) != 0:
        write_single_stage_01_pr_dictionary_as_csv(repo, pr_dict_stage_01, MERGED)
    if len(pr_dict_stage_01[UNMERGED]) != 0:
        write_single_stage_01_pr_dictionary_as_csv(repo, pr_dict_stage_01, UNMERGED)
    print("Stage_01 csv files complete")


# Write every pull state of the pr_dict_stage_02 to separate CSV files all in one method call
def write_all_stage_02_pr_dictionary_csv_files(repo, pr_dict_stage_02):
    print("\nWriting stage_02 pull request dictionary to csv files...")
    if len(pr_dict_stage_02[OPEN]) != 0:
        write_single_stage_02_pr_dictionary_as_csv(repo, pr_dict_stage_02, OPEN)
    if len(pr_dict_stage_02[MERGED]) != 0:
        write_single_stage_02_pr_dictionary_as_csv(repo, pr_dict_stage_02, MERGED)
    if len(pr_dict_stage_02[UNMERGED]) != 0:
        write_single_stage_02_pr_dictionary_as_csv(repo, pr_dict_stage_02, UNMERGED)
    print("Stage_02 csv files complete")


# Write every pull state of the pr_dict_stage_03 to separate CSV files all in one method call
def write_all_stage_03_pr_dictionary_csv_files(repo, pr_dict_stage_03):
    print("\nWriting stage_03 pull request dictionary to csv files...")
    if len(pr_dict_stage_03[OPEN]) != 0:
        write_single_stage_03_pr_dictionary_as_csv(repo, pr_dict_stage_03, OPEN)
    if len(pr_dict_stage_03[MERGED]) != 0:
        write_single_stage_03_pr_dictionary_as_csv(repo, pr_dict_stage_03, MERGED)
    if len(pr_dict_stage_03[UNMERGED]) != 0:
        write_single_stage_03_pr_dictionary_as_csv(repo, pr_dict_stage_03, UNMERGED)
    print("Stage_03 csv files complete")


# Write every pull state of the pr_drive_by_author to separate CSV files all in one method call
def write_all_drive_by_pr_dictionary_csv_files(repo, pr_dict_drive_by_author):
    print("\nWriting drive by pull request dictionary to csv files...")
    if len(pr_dict_drive_by_author[OPEN]) != 0:
        write_single_drive_by_pr_dictionary_as_csv(repo, pr_dict_drive_by_author, OPEN)
    if len(pr_dict_drive_by_author[MERGED]) != 0:
        write_single_drive_by_pr_dictionary_as_csv(repo, pr_dict_drive_by_author, MERGED)
    if len(pr_dict_drive_by_author[UNMERGED]) != 0:
        write_single_drive_by_pr_dictionary_as_csv(repo, pr_dict_drive_by_author, UNMERGED)
    print("Drive by csv files complete")


def get_user_ID_set_from_repo(repo):
    user_ID_set_open = _get_user_ID_set_from_open(repo)
    user_ID_set_merged = _get_user_ID_set_from_merged(repo)
    user_ID_set_unmerged = _get_user_ID_set_from_unmerged(repo)
    return _the_combination_of_the_sets(user_ID_set_open, user_ID_set_merged, user_ID_set_unmerged)


def _get_user_ID_set_from_open(repo):
    try:
        os.chdir(targetManager.get_open_pull_request_level_subdirectory_for(repo))
        csv_file = open("stage_01_pull_requests_open.csv", 'r')
        return _clean_data_in_csv(csv_file)
    except Exception as error:
        ERROR_LOGGER.write_to_log(
            "researchToolkit.py had an error " + str(error) + " with the method _get_user_ID_set_from_open with open")
        return set()


def _get_user_ID_set_from_merged(repo):
    try:
        os.chdir(targetManager.get_merged_pull_request_level_subdirectory_for(repo))
        csv_file = open("stage_01_pull_requests_closed_merged.csv", 'r')
        return _clean_data_in_csv(csv_file)
    except Exception as error:
        ERROR_LOGGER.write_to_log(
            "researchToolkit.py had an error " + str(error) + " with the method _get_user_ID_set_from_merged with merged")
        return set()

def _get_user_ID_set_from_unmerged(repo):
    try:
        os.chdir(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo))
        csv_file = open("stage_01_pull_requests_closed_unmerged.csv", 'r')
        return _clean_data_in_csv(csv_file)
    except Exception as error:
        ERROR_LOGGER.write_to_log(
            "researchToolkit.py had an error " + str(error) + " with the method get_user_ID_set_from_unmerged with unmerged")
        return set()

def _clean_data_in_csv(csv_file):
    users = []
    for user in csv_file:
        users.append(user.split(','))
    return _read_data_for_users(users)

def _read_data_for_users(users):
    users_set = set()
    for user in users:
        users_set.add(str(user[1]))  # this is the spot where the ID is in the CSV, if it changes so does this
    users_set.remove("GITHUB ID")
    return users_set

def _the_combination_of_the_sets(set_open, set_merged, set_unmerged): # making a fix now, can clean it later.  time to test it. or clean it
    master_set = set()
    try:
        master_set.update(set_open)
    except Exception as error:
        INFO_LOGGER.write_to_log("researchToolkit.py had an error " + str(error) + " with the method _the_combination_of_the_sets wit the open set" )
    try:
        master_set.update(set_merged)
    except Exception as error:
        INFO_LOGGER.write_to_log("researchToolkit.py had an error " + str(error) + " with the method _the_combination_of_the_sets wit the merged set")
    try:
        master_set.update(set_unmerged)
    except Exception as error:
        INFO_LOGGER.write_to_log("researchToolkit.py had an error " + str(error) + " with the method _the_combination_of_the_sets wit the unmerged set")


    return master_set

def get_user_data_CSV_file_for(user_set, repo):
    user_CSV_data = []
    os.chdir(targetManager.get_json_github_users_file_path_to(repo))
    for user in user_set:
        try:
            with open(str(user) + "_user.json", 'r') as user_file:
                data = json.load(user_file)
                pull_list = [data["login"], data["id"], data["public_repos"], data["public_gists"], data["followers"], data["following"], data["created_at"]]
                user_CSV_data.append(pull_list)
                user_file.close()
        except Exception as error:
            print("This user: " + str(user) + " had this error " + str(error))
    return user_CSV_data


def write_user_data_as_csv(user_CSV_data, repo):
    os.chdir(targetManager.get_github_users_csv_subdirectory_for(repo))
    with open("users_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        descriptors = "GITHUB USERNAME,GITHUB ID,# OF PUBLIC REPOS,# OF PUBLIC GISTS,# OF FOLLOWERS,# OF USER IS FOLLOWING,CREATED DATE,"
        writer.writerow([descriptors])
        for element in user_CSV_data:
            string = ""
            for pull_request_info in element:
                string += (str(pull_request_info) + ",")
            writer.writerow([string])

    csvfile.close()
    return

def get_IDs_for_repo_pull_request(repo):
    open_list = os.listdir(targetManager.get_json_pulls_open_file_path_to(repo))
    merged_list = os.listdir(targetManager.get_json_pulls_merged_file_path_to(repo))
    unmerged_list = os.listdir(targetManager.get_json_pulls_unmerged_file_path_to(repo))
    return open_list, merged_list, unmerged_list

def create_commit_id_folders(repo, commit_ids, pull_type):
    print("\nCreating %s commit ID folders. This may take a few moments..." % str(
        pull_type).upper())  # Let the user know what is happening

    # Write every id we have collected as a folder
    for id in commit_ids:
        if pull_type == "closed_merged":
            targetManager.create_repo_merged_commit_id_directory_for(repo, str(id))

        elif pull_type == "closed_unmerged":
            targetManager.create_repo_unmerged_commit_id_directory_for(repo,  str(id))

        else:
            targetManager.create_repo_open_commit_id_directory_for(repo,  str(id))
    print("%s commit ID folders successfully created." % str(pull_type).upper())  # Let the user know what is happening

