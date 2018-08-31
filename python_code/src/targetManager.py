# targetManager.py
# Concept by Stephen White & James Todd
# Written by Stephen White
# Date: 7/1/2017
#
# Purpose: To assist in the creation & management of generated/downloaded files that are essential to our Undergraduate
#          research for Marco Gerosa and Igor Steinmacher

import shutil
import os

CSV_FILES = "csv_files"
JSON_FILES = "json_files"
TEXT_FILES = "text_files"
OPEN = "open"
MERGED = "closed-merged"
UNMERGED = "closed-unmerged"
COMMIT_LEVEL = "commit-level"
GITHUB_USERS = "github-users"
PULL_REQUEST_LEVEL = "pull-request-level"
PULL_REQUESTS = "pull_requests"
MAIN_PULL_JSON = "main_pull.json"

class TargetManager:
    def __init__(self, home_path):
        self.HOME_PATH = home_path
        self.TARGET_PATH = os.path.join(self.HOME_PATH, "Target")
        self.JSON_FILES_PATH = TargetManager.join_path(self.TARGET_PATH, JSON_FILES)
        self.TEXT_FILES_PATH = TargetManager.join_path(self.TARGET_PATH, TEXT_FILES)
        self.CSV_FILES_PATH = TargetManager.join_path(self.TARGET_PATH, CSV_FILES)

    @staticmethod
    def get_full_subdirectory_paths_list_from(path):
        path = os.path.abspath(path)
        return [f.path for f in os.scandir(path) if f.is_dir()]

    @staticmethod
    def join_path(path_01, path_02):
        if path_02.startswith("/"):
            path_02 = TargetManager.strip_slashes_from_repository_string(path_02)
        return os.path.join(path_01, path_02)

    def set_home_path(self, home_path):
        self.HOME_PATH = home_path

    def set_target_path(self, target_path):
        self.TARGET_PATH = target_path

    def set_json_files_path(self, json_files_path):
        self.JSON_FILES_PATH = json_files_path

    def set_text_files_path(self, text_files_path):
        self.TEXT_FILES_PATH = text_files_path

    def set_csv_files_path(self, csv_files_path):
        self.CSV_FILES_PATH = csv_files_path

    def get_home_path(self):
        return self.HOME_PATH

    def get_target_path(self):
        return self.TARGET_PATH

    def get_json_files_path(self):
        return self.JSON_FILES_PATH

    def get_text_files_path(self):
        return self.TEXT_FILES_PATH

    def get_csv_files_path(self):
        return self.CSV_FILES_PATH

    def create_target_directory_structure(self):
        TargetManager.create_main_target_directories(self)
        TargetManager.populate_main_target_subdirectories(self)
        print("Target directory tree has been successfully created!")

    def create_main_target_directories(self):
        TargetManager.create_target_folder(self)
        TargetManager.create_json_text_and_csv_directories(self)

    def populate_main_target_subdirectories(self):
        TargetManager.populate_text_files_directory_with_subdirectories(self)
        TargetManager.populate_csv_files_directory_with_subdirectories(self)
        TargetManager.populate_json_files_directory_with_subdirectories(self)

    def create_target_folder(self):
        try:
            os.chdir(self.HOME_PATH)
            os.mkdir("Target")
        except FileExistsError:
            return

    def create_json_text_and_csv_directories(self):
        os.chdir(self.TARGET_PATH)
        TargetManager.create_json_directory()
        TargetManager.create_text_directory()
        TargetManager.create_csv_directory()

    @staticmethod
    def create_json_directory():
        try:
            os.mkdir(JSON_FILES)
        except FileExistsError:
            return

    @staticmethod
    def create_text_directory():
        try:
            os.mkdir(TEXT_FILES)
        except FileExistsError:
            return

    @staticmethod
    def create_csv_directory():
        try:
            os.mkdir(CSV_FILES)
        except FileExistsError:
            return

    def populate_text_files_directory_with_subdirectories(self):
        os.chdir(self.TEXT_FILES_PATH)
        TargetManager.create_collected_repos_directory()
        TargetManager.create_important_text_files_directory()

    @staticmethod
    def create_collected_repos_directory():
        try:
            os.mkdir("_collected-repos")
        except FileExistsError:
            return

    @staticmethod
    def create_important_text_files_directory():
        try:
            os.mkdir("_important-text-files")
        except FileExistsError:
            return

    def populate_csv_files_directory_with_subdirectories(self):
            try:
                os.chdir(self.CSV_FILES_PATH)
                os.mkdir("_important-csv-files")
            except FileExistsError:
                return

    def populate_json_files_directory_with_subdirectories(self):
        try:
            os.chdir(self.JSON_FILES_PATH)
            os.mkdir("_important-json-files")
        except FileExistsError:
            return

    def delete_entire_target_directory_tree(self):
        if TargetManager.target_tree_exists(self):
            shutil.rmtree(TargetManager.get_target_path(self))
            print("Target directory tree has been erased!")

    def target_tree_exists(self):
        return TargetManager.path_exists(self.TARGET_PATH)

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)

    def delete_specific_repository_from_target_structure(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        if TargetManager.repo_exists_in_target_structure(self, repo):
            TargetManager.delete_entire_repository_subdirectory_tree_for(self, repo)
            print("Repository '%s' has been removed from the Target structure." % repo)
        else:
            print("Repository %s does not exist within Target Structure" % repo)

    @staticmethod
    def strip_slashes_from_repository_string(repo):
        if str(repo).startswith("/"):
            return repo.split("/")[1] + "-" + repo.split("/")[2]
        return repo

    def repo_exists_in_target_structure(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        csv_repo_path_exists = TargetManager._csv_repo_path_exists_in_target_structure_for(self, repo)
        json_repo_path_exists = TargetManager._json_repo_path_exists_in_target_structure_for(self, repo)
        text_repo_path_exists = TargetManager._text_repo_path_exists_in_target_structure_for(self, repo)
        if not (csv_repo_path_exists and json_repo_path_exists and text_repo_path_exists):
            return False
        else:
            return True

    def _csv_repo_path_exists_in_target_structure_for(self, repo):
        csv_repo_path = TargetManager.join_path(self.CSV_FILES_PATH, repo)
        return TargetManager.path_exists(csv_repo_path)

    def _json_repo_path_exists_in_target_structure_for(self, repo):
        json_repo_path = TargetManager.join_path(self.JSON_FILES_PATH, repo)
        return TargetManager.path_exists(json_repo_path)

    def _text_repo_path_exists_in_target_structure_for(self, repo):
        text_repo_path = TargetManager.join_path(self.TEXT_FILES_PATH, repo)
        return TargetManager.path_exists(text_repo_path)

    def delete_entire_repository_subdirectory_tree_for(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        TargetManager.delete_csv_directory_tree_belonging_to(self, repo)
        TargetManager.delete_json_directory_tree_belonging_to(self, repo)
        TargetManager.delete_text_directory_tree_belonging_to(self, repo)

    def delete_csv_directory_tree_belonging_to(self, repo):
        csv_repo_path = TargetManager.get_csv_file_path_to(self, repo)
        shutil.rmtree(csv_repo_path)

    def delete_json_directory_tree_belonging_to(self, repo):
        json_repo_path = TargetManager.get_json_file_path_to(self, repo)
        shutil.rmtree(json_repo_path)

    def delete_text_directory_tree_belonging_to(self, repo):
        text_repo_path = TargetManager.get_text_file_path_to(self, repo)
        shutil.rmtree(text_repo_path)

    def get_csv_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(self.CSV_FILES_PATH, repo)

    def get_json_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(self.JSON_FILES_PATH, repo)

    def get_text_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(self.TEXT_FILES_PATH, repo)

    def get_important_csv_files_path(self):
        return TargetManager.join_path(self.CSV_FILES_PATH, "_important-csv-files")

    def get_important_json_files_path(self):
        return TargetManager.join_path(self.JSON_FILES_PATH, "_important-json-files")

    def get_important_text_files_path(self):
        return TargetManager.join_path(self.TEXT_FILES_PATH, "_important-text-files")

    def get_collected_repos_path(self):
        return TargetManager.join_path(self.TEXT_FILES_PATH, "_collected-repos")

    def get_json_commits_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_file_path_to(self, repo), "commits")

    def get_json_commits_merged_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_commits_file_path_to(self, repo), MERGED)

    def get_json_commits_unmerged_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_commits_file_path_to(self, repo), UNMERGED)

    def get_json_commits_open_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_commits_file_path_to(self, repo), OPEN)

    def get_json_pulls_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_file_path_to(self, repo), "pull_requests")

    def get_json_pulls_merged_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_pulls_file_path_to(self, repo), MERGED)

    def get_json_pulls_unmerged_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_pulls_file_path_to(self, repo), UNMERGED)

    def get_json_pulls_open_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_pulls_file_path_to(self, repo), OPEN)

    def get_json_github_users_file_path_to(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        return TargetManager.join_path(TargetManager.get_json_file_path_to(self, repo), GITHUB_USERS)

    @staticmethod
    def get_subdirectories_in(directory_path):
        return [dI for dI in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, dI))]

    def get_merged_pull_id_file_path_to(self, repo, merged_pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        merged_pull_id_path_to_repo = TargetManager.get_json_pulls_merged_file_path_to(self, repo)
        if merged_pull_id in TargetManager.get_subdirectories_in(merged_pull_id_path_to_repo):
            return TargetManager.join_path(merged_pull_id_path_to_repo, merged_pull_id)

    def get_unmerged_pull_id_file_path_to(self, repo, unmerged_pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        unmerged_pull_id_path_to_repo = TargetManager.get_json_pulls_unmerged_file_path_to(self, repo)
        if unmerged_pull_id in TargetManager.get_subdirectories_in(unmerged_pull_id_path_to_repo):
            return TargetManager.join_path(unmerged_pull_id_path_to_repo, unmerged_pull_id)

    def get_open_pull_id_file_path_to(self, repo, open_pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        open_pull_id_path_to_repo = TargetManager.get_json_pulls_open_file_path_to(self, repo)
        if open_pull_id in TargetManager.get_subdirectories_in(open_pull_id_path_to_repo):
            return TargetManager.join_path(open_pull_id_path_to_repo, open_pull_id)

    def delete_all_open_pull_id_subdirectories_for(self, repo):
        json_pulls_open_file_path = TargetManager.get_json_pulls_open_file_path_to(self, repo)
        for pull_id in TargetManager.get_full_subdirectory_paths_list_from(json_pulls_open_file_path):
            shutil.rmtree(os.path.abspath(pull_id))

    def get_open_pull_id_main_json_file_path_for(self, repo, open_pull_id):
        open_pull_id_file_path = TargetManager.get_open_pull_id_file_path_to(self, repo, open_pull_id)
        return TargetManager.join_path(open_pull_id_file_path, MAIN_PULL_JSON)

    def get_unmerged_pull_id_main_json_file_path_for(self, repo, unmerged_pull_id):
        unmerged_pull_id_file_path = TargetManager.get_unmerged_pull_id_file_path_to(self, repo, unmerged_pull_id)
        return TargetManager.join_path(unmerged_pull_id_file_path, MAIN_PULL_JSON)

    def get_merged_pull_id_main_json_file_path_for(self, repo, merged_pull_id):
        merged_pull_id_file_path = TargetManager.get_merged_pull_id_file_path_to(self, repo, merged_pull_id)
        return TargetManager.join_path(merged_pull_id_file_path, MAIN_PULL_JSON)

    def create_repo_subdirectories_for(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        TargetManager._make_repo_directory_in_each_target_subdirectory(self, repo)
        TargetManager._create_json_repo_subdirectory_tree_for(self, repo)
        TargetManager.create_csv_subdirectory_tree_for(self, repo)

    def _make_repo_directory_in_each_target_subdirectory(self, repo):
        TargetManager.create_repo_csv_directory_for(self, repo)
        TargetManager.create_repo_json_directory_for(self, repo)
        TargetManager.create_repo_text_directory_for(self, repo)

    def create_repo_csv_directory_for(self, repo):
        os.chdir(TargetManager.get_csv_files_path(self))
        try:
            os.mkdir(repo)
        except FileExistsError:
            return

    def create_repo_json_directory_for(self, repo):
        os.chdir(TargetManager.get_json_files_path(self))
        try:
            os.mkdir(repo)
        except FileExistsError:
            return

    def create_repo_text_directory_for(self, repo):
        os.chdir(TargetManager.get_text_files_path(self))
        try:
            os.mkdir(repo)
        except FileExistsError:
            return

    def _create_json_repo_subdirectory_tree_for(self, repo):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        TargetManager._create_github_users_and_pull_request_directories_for(self, repo)
        TargetManager._create_merged_unmerged_and_open_pull_request_directories_for(self, repo)
        TargetManager._create_merged_unmerged_and_open_commit_directories_for(self, repo)
        return

    def _create_github_users_and_pull_request_directories_for(self, repo): # and commits!
        os.chdir(TargetManager.get_json_file_path_to(self, repo))
        TargetManager._create_github_users_directory_for_this_repo()
        TargetManager._create_pull_requests_directory_for_this_repo()
        TargetManager._create_commits_directory_for_this_repo()

    @staticmethod
    def _create_commits_directory_for_this_repo():
        try:
            os.mkdir("commits")
        except FileExistsError:
            return

    @staticmethod
    def _create_github_users_directory_for_this_repo():
        try:
            os.mkdir(GITHUB_USERS)
        except FileExistsError:
            return

    @staticmethod
    def _create_pull_requests_directory_for_this_repo():
        try:
            os.mkdir(PULL_REQUESTS)
        except FileExistsError:
            return

    def _create_merged_unmerged_and_open_pull_request_directories_for(self, repo):
        os.chdir(TargetManager.get_json_pulls_file_path_to(self, repo))
        TargetManager._create_merged_pull_request_directory_for_this_repo()
        TargetManager._create_unmerged_pull_request_directory_for_this_repo()
        TargetManager._create_open_pull_request_directory_for_this_repo()

    def _create_merged_unmerged_and_open_commit_directories_for(self, repo):
        os.chdir(TargetManager.get_json_commits_file_path_to(self, repo))
        TargetManager._create_merged_pull_request_directory_for_this_repo()
        TargetManager._create_unmerged_pull_request_directory_for_this_repo()
        TargetManager._create_open_pull_request_directory_for_this_repo()

    @staticmethod
    def _create_merged_pull_request_directory_for_this_repo():
        try:
            os.mkdir(MERGED)
        except FileExistsError:
            return

    @staticmethod
    def _create_unmerged_pull_request_directory_for_this_repo():
        try:
            os.mkdir(UNMERGED)
        except FileExistsError:
            return

    @staticmethod
    def _create_open_pull_request_directory_for_this_repo():
        try:
            os.mkdir(OPEN)
        except FileExistsError:
            return

    def create_repo_merged_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_merged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_unmerged_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_unmerged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_open_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_open_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_merged_commit_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_commits_merged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_unmerged_commit_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_commits_unmerged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_open_commit_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_commits_open_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return


    def create_csv_subdirectory_tree_for(self, repo):
        TargetManager.create_commit_level_csv_subdirectory_for(self, repo)
        TargetManager.create_github_users_csv_subdirectory_for(self, repo)
        TargetManager.create_pull_request_level_csv_subdirectory_for(self, repo)
        TargetManager.create_pull_request_level_csv_subdirectory_tree_for(self, repo)

    def create_commit_level_csv_subdirectory_for(self, repo):
        TargetManager.setup_commit_level_csv_subdirectory_for_creation_for(self, repo)
        try:
            os.mkdir(COMMIT_LEVEL)
        except FileExistsError:
            return

    def setup_commit_level_csv_subdirectory_for_creation_for(self, repo):
        path_to_repo_csv_file_path = TargetManager.get_csv_file_path_to(self, repo)
        os.chdir(path_to_repo_csv_file_path)

    def create_github_users_csv_subdirectory_for(self, repo):
        TargetManager.setup_github_users_csv_subdirectory_for_creation_for(self, repo)
        try:
            os.mkdir(GITHUB_USERS)
        except FileExistsError:
            return

    def setup_github_users_csv_subdirectory_for_creation_for(self, repo):
        path_to_repo_csv_file_path = TargetManager.get_csv_file_path_to(self, repo)
        os.chdir(path_to_repo_csv_file_path)

    def create_pull_request_level_csv_subdirectory_tree_for(self, repo):
        TargetManager.create_pull_request_level_csv_subdirectory_for(self, repo)
        TargetManager.setup_inner_pull_request_level_subdirectory_tree_for(self, repo)
        TargetManager.create_unmerged_pull_request_level_subdirectory_for_this_repo()
        TargetManager.create_merged_pull_request_level_subdirectory_for_this_repo()
        TargetManager.create_open_pull_request_level_subdirectory_for_this_repo()

    def create_pull_request_level_csv_subdirectory_for(self, repo):
        TargetManager.setup_pull_request_level_subdirectory_for_creation_for(self, repo)
        try:
            os.mkdir(PULL_REQUEST_LEVEL)
        except FileExistsError:
            return

    def setup_inner_pull_request_level_subdirectory_tree_for(self, repo):
        os.chdir(TargetManager.get_pull_request_level_csv_subdirectory_for(self, repo))

    @staticmethod
    def create_unmerged_pull_request_level_subdirectory_for_this_repo():
        try:
            os.mkdir(UNMERGED)
        except FileExistsError:
            return

    @staticmethod
    def create_merged_pull_request_level_subdirectory_for_this_repo():
        try:
            os.mkdir(MERGED)
        except FileExistsError:
            return

    @staticmethod
    def create_open_pull_request_level_subdirectory_for_this_repo():
        try:
            os.mkdir(OPEN)
        except FileExistsError:
            return

    def get_unmerged_pull_request_level_subdirectory_for(self, repo):
        return TargetManager.join_path(TargetManager.get_pull_request_level_csv_subdirectory_for(self, repo), UNMERGED)

    def get_merged_pull_request_level_subdirectory_for(self, repo):
        return TargetManager.join_path(TargetManager.get_pull_request_level_csv_subdirectory_for(self, repo), MERGED)

    def get_open_pull_request_level_subdirectory_for(self, repo):
        return TargetManager.join_path(TargetManager.get_pull_request_level_csv_subdirectory_for(self, repo), OPEN)

    def setup_pull_request_level_subdirectory_for_creation_for(self, repo):
        path_to_repo_csv_file_path = TargetManager.get_csv_file_path_to(self, repo)
        os.chdir(path_to_repo_csv_file_path)

    def get_commit_level_csv_subdirectory_path_for(self, repo):
        return TargetManager.join_path(TargetManager.get_csv_file_path_to(self, repo), COMMIT_LEVEL)

    def get_github_users_csv_subdirectory_for(self, repo):
        return TargetManager.join_path(TargetManager.get_csv_file_path_to(self, repo), GITHUB_USERS)

    def get_pull_request_level_csv_subdirectory_for(self, repo):
        return TargetManager.join_path(TargetManager.get_csv_file_path_to(self, repo), PULL_REQUEST_LEVEL)


    def create_repo_merged_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_merged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_unmerged_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_unmerged_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return

    def create_repo_open_pull_id_directory_for(self, repo, pull_id):
        repo = TargetManager.strip_slashes_from_repository_string(repo)
        try:
            os.chdir(TargetManager.get_json_pulls_open_file_path_to(self, repo))
            os.mkdir(pull_id)
        except FileExistsError:
            return