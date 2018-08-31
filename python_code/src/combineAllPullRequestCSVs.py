# combineAllPullRequestCSVs.py
# Created by Stephen White
# Date: 9/8/2017
# Purpose: Comb through separated Pull Request CSV files that exist in the Target Structure, and combine
#          them into one amalgamated CSV file containing all relevant raw Pull Request Data

from targetManager import TargetManager
import csv
import os

targetManager = TargetManager(os.getcwd())
collected_repos_path = os.path.join(targetManager.get_collected_repos_path(), "collected_repos.txt")

def initialize_combined_csvs_file():
    massive_csv_file_path = get_combined_csvs_file_path()
    with open(massive_csv_file_path, "w", newline="", encoding="utf-8") as big_csv_file:
        writer = csv.writer(big_csv_file, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        descriptors = "GITHUB USERNAME,GITHUB ID,REPO,PR#,PR STATE,DATE CREATED,DATE CLOSED,# REVIEW COMMENTS," \
                      "# COMMITS,# ADDITIONS,# DELETIONS,# FILES CHANGED"
        writer.writerow([descriptors])
        big_csv_file.close()
    return

def get_combined_csvs_file_path():
    return os.path.join(targetManager.get_important_csv_files_path(), "combined_pull_request_data.csv")

def combine_pull_csvs_into_one(repo):
    csv_merged_path = targetManager.join_path(targetManager.get_merged_pull_request_level_subdirectory_for(repo),
                                     "stage_01_pull_requests_closed_merged.csv")
    csv_unmerged_path = targetManager.join_path(targetManager.get_unmerged_pull_request_level_subdirectory_for(repo),
                                    "stage_01_pull_requests_closed_unmerged.csv")
    csv_open_path = targetManager.join_path(targetManager.get_open_pull_request_level_subdirectory_for(repo),
                                    "stage_01_pull_requests_open.csv")
    csv_path_list = [csv_merged_path, csv_unmerged_path, csv_open_path]
    csv_content_list = list()
    for csv_path in csv_path_list:
        with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for line_list in reader:
                csv_content_list.append(line_list)
            csv_file.close()

    massive_csv_file_path = get_combined_csvs_file_path()
    with open(massive_csv_file_path, "a", newline="", encoding="utf-8") as big_csv_file:
        writer = csv.writer(big_csv_file, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='', escapechar='\\')
        for pull_request_data_list in csv_content_list:
            string = ""
            for pull_request_data in pull_request_data_list:
                string += (str(pull_request_data) + ",")
            writer.writerow([string])

    return

# Ensure that all repos have been properly collected
def combine_all_pr_csvs():
    initialize_combined_csvs_file()
    repo_lines = list(
        map(str.strip, open(collected_repos_path, 'r').readlines()))  # strip all \n and place each line in a list

    for repo in repo_lines:
        try:
            print("combining PRs from " + repo + "...")
            if not repo.startswith("/"):
                continue
            else:
                combine_pull_csvs_into_one(repo)
        except Exception:
            print(repo)
        print("\nCombination of repos into singular CSV file complete!")
