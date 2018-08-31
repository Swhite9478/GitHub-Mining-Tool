#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gitHub.py
# Created by Stephen White
# Date: 7/30/2017
# Purpose: This class is a wrapper which will provide the necessary functionality to download json files
#          from GitHub's api.

from requests.auth import HTTPBasicAuth
from termcolor import colored
from targetManager import TargetManager
import requests
import json
import os
import threading
from queue import Queue
import time
from logger import Logger

# Each valid account allows us access to 5,000 requests per hour. Total requests per hour permitted: 30,000
targetManager = TargetManager(os.getcwd())
IMPORTANT_TEXT_PATH = targetManager.get_important_text_files_path()
ERROR_LOGGER = Logger(IMPORTANT_TEXT_PATH, "ERROR_LOG", "ERROR")
github_accounts = {
        0: ['Githubfake01', '5RNsya*z#&aA'],
        1: ['GithubFake02', '9dJeg^Bp^g63'],
	    2: ['Github-Fake03', '2A$p3$zy%aaD'],
	    3: ['GithubFake04', '4Yg3&MQN9x%F'],
        4: ['GithubFake05', 'Cm82$$bFa!xb'],
        5: ['GithubFake06', '2t*u2Y8P^tTk'],
        6: ['GithubFake07', 'Hk1233**012'],
        7: ['GithubFake08', 'PO11sd*^%$']}

num_accounts = len(github_accounts)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

proxies = {'http': 'http://<username>:<password>@107.182....:<port>'}

payload = {'page': '1', 'per_page': '100'}
pull_payload = {'page': '1', 'per_page': '100','sort': 'created', 'order': 'desc'}

REQUEST_URL = "https://api.github.com/search/repositories?q=stars:%3E=15000"


def get_repositories(REPO_CAP):
    git_user = 0
    request = check_rate_limit(REQUEST_URL, git_user, payload)
    num_repos = request.json()["total_count"]
    num_pages = get_number_of_pages(num_repos)
    write_collected_repos(REPO_CAP, num_pages, git_user)
    return

def write_collected_repos(REPO_CAP, num_pages, git_user):
    target = open(os.path.join(targetManager.get_collected_repos_path(), 'collected_repos2.txt'), 'w')
    target.write("%d" % REPO_CAP + "\n")
    collected_repos = 0
    for page in range(1, num_pages+1):
        if collected_repos == REPO_CAP:
            break
        payload["page"] = str(page)

        request = check_rate_limit(REQUEST_URL, git_user, payload)

        for repo in request.json()["items"]:
            if collected_repos == REPO_CAP:
                break
            target.write("/" + str(repo["full_name"]) + "\n")
            collected_repos += 1

    target.write("%d" % collected_repos)
    target.close()
    return

def get_number_of_pages(num_repos):
    if num_repos >= 1000:  # Set a maximum cap of 1,000 repositories
        num_repos = 1000
    return abs(int(-num_repos//100))

def _get_request_url(git_user, api_url,params):
    r = requests.get(api_url, auth=HTTPBasicAuth( github_accounts[git_user][0], github_accounts[git_user][1]),
                    proxies=proxies, headers=headers, params=params)
    return r

def check_rate_limit(api_url, git_user, params):
    try:
        request = _get_request_url(git_user, api_url, params)
        while int(request.headers['X-RateLimit-Remaining']) <= 1: # <=1 because we have more requests to do still
            git_user = (git_user + 1) % num_accounts
            request = _get_request_url(git_user, api_url, params)
        return request
    except KeyError:
        if not threading.current_thread().isDaemon():
            print("==========================================================================\n\n")
            print(" X Rate-Limit Reached. MAIN THREAD is waiting for the Rate-Limit to reset.")
            print("\n\n==========================================================================")
        time.sleep(60)
        return check_rate_limit(api_url, git_user, params)

def get_api_page(api_url, page_number):
    payload["page"] = str(page_number)
    git_user = 0
    request = check_rate_limit(api_url, git_user, payload)
    if request.status_code != 200:
        ERROR_LOGGER.write_to_log("This API_URL " + str(api_url) + " with page number " + str(page_number) + " has this error " + str(request.status_code) + " THE METHOD CALLER IS GET_API_PAGE")
        print(colored("CODE: " + str(request.status_code), "red"))
        tempJson = {"ERROR": request.status_code}
        print(tempJson)
        request.json(json.dumps(tempJson))
        print(request.json())
    return request

def download_api_page_json(api_url, page_number, output_name):
    with open(output_name, 'w', encoding='utf-8') as f:
        request = (get_api_page(api_url, page_number))
        data = request.json()
        json.dump(data, f,sort_keys=True)
        f.close()
    return request.status_code

# Return the number of pull requests that are closed, and merged in a given repository
def get_closed_merged_pull_nums(repo_info):
    git_user = 0
    url = 'https://api.github.com/search/issues?q=is:pr+is:closed+is:merged+repo:' + repo_info[1:]
    request = check_rate_limit(url,git_user, payload)
    return int(request.json()["total_count"])

# Return the number of pull requests that are closed, and unmerged in a given repository
def get_closed_unmerged_pull_nums(repo_info):
    git_user = 0
    url = 'https://api.github.com/search/issues?q=is:pr+is:closed+is:unmerged+repo:' + repo_info[1:]
    request = check_rate_limit(url, git_user, payload)
    return int(request.json()["total_count"])

# Return the number of pull requests that are closed and open in a given repository
def get_open_pull_nums(repo_info):
    git_user = 0
    url = 'https://api.github.com/search/issues?q=is:pr+is:open+repo:' + repo_info[1:]
    request = check_rate_limit(url, git_user, payload)
    return int(request.json()["total_count"])

def git_pull_ids_open(repo):
    print("\nCollecting OPEN Pull IDs From Github API. This may take a few minutes...")
    original_url = "https://api.github.com/search/issues?q=is:pr+is:open+repo:" + repo[1:]
    pulls_num = get_open_pull_nums(repo)
    return _get_pull_ids(original_url, pulls_num)

def git_pull_ids_merged(repo):
    print("\nCollecting MERGED Pull IDs From Github API. This may take a few minutes...")
    original_url = "https://api.github.com/search/issues?q=is:pr+is:closed+is:merged+repo:" + repo[1:]
    pulls_num = get_closed_merged_pull_nums(repo)
    return _get_pull_ids(original_url, pulls_num)

def git_pull_ids_unmerged(repo):
    print("\nCollecting UNMERGED Pull IDs From Github API. This may take a few minutes...")
    original_url = "https://api.github.com/search/issues?q=is:pr+is:closed+is:unmerged+repo:" + repo[1:]
    pulls_num = get_closed_unmerged_pull_nums(repo)
    return _get_pull_ids(original_url, pulls_num)

def _get_pull_ids(url,pulls_num):
    original_url = url
    pull_ids = []
    git_user = 0
    collected_ids = 0
    num_pages = abs(pulls_num // (-100))
    page_num = 1
    for page in range(1, num_pages + 1):
        if page_num > 10:
            page_num = 1
        pull_payload["page"] = str(page_num)
        page_num += 1
        request = check_rate_limit(url, git_user, pull_payload)
        request = request.json()
        for pull_request in request["items"]:
            pull_ids.append(str(pull_request["url"]).split("/")[-1])
            collected_ids += 1
            if collected_ids % 1000 == 0:
                url = original_url
                url += ("+created:<" + pull_request["created_at"])
    print("Finished Collecting IDs From Github API.")
    return pull_ids
 
def get_pull_ids_list_from_repo(repo):
    complete_pull_ids = list()
    pull_paths = list()
    open_pulls_path = targetManager.get_json_pulls_open_file_path_to(repo)
    merged_pulls_path = targetManager.get_json_pulls_merged_file_path_to(repo)
    unmerged_pulls_path = targetManager.get_json_pulls_unmerged_file_path_to(repo)
    pull_paths.append(open_pulls_path)
    pull_paths.append(merged_pulls_path)
    pull_paths.append(unmerged_pulls_path)
    for pull_state_path in pull_paths:
        pull_ids = [dI for dI in os.listdir(pull_state_path) if os.path.isdir(os.path.join(pull_state_path, dI))]
        for pull_id in pull_ids:
            complete_pull_ids.append([pull_state_path, pull_id])
    return complete_pull_ids

# Pass in the associated repository and pull request state (OPEN, MERGED, or UNMERGED) to download each PR's json file.
# NOTE: THIS FUNCTION MUST BE CALLED ONLY AFTER targetManager.create_pull_request_id_folders() HAS BEEN CALLED
def download_pull_requests(repo):
    PULL_REQUEST_QUEUE = Queue()
    pull_request_level_thread_list = []
    pill2kill = threading.Event()
    pull_ids = get_pull_ids_list_from_repo(repo)

    for pull_info in pull_ids:
        PULL_REQUEST_QUEUE.put(pull_info)

    for newThread in range(100):
        thread = threading.Thread(target = kickoff_pull_request_level_thread_queue, args = [[repo, PULL_REQUEST_QUEUE, pill2kill]])
        thread.daemon = True
        pull_request_level_thread_list.append(thread)
        thread.start()

    PULL_REQUEST_QUEUE.join()

    time.sleep(1)
    for thread in pull_request_level_thread_list:
        thread.join()
    return

def kickoff_pull_request_level_thread_queue(data):
    while True: # this looks like it can brake everything omg
        if data[1].empty():
            return
        pull_info = data[1].get()
        pull_request_level_thread_job(pull_info, data[0], data[1])
        data[1].task_done()

def pull_request_level_thread_job(pull_info, repo, PULL_REQUEST_QUEUE):
    try:
        original_url = "\nhttps://api.github.com/repos" + repo + "/pulls/" + pull_info[1]
        output_path = os.path.join(pull_info[0], pull_info[1])
        output_name = os.path.join(output_path, "main_pull.json")
        download_api_page_json(original_url, 1, output_name)
        print("Downloaded [%s json..." % (str(pull_info).split("\\")[-1].upper()))
    except Exception as e:
        print(e)
        PULL_REQUEST_QUEUE.put(pull_info)

def download_commit_level_jsons(repo):
    COMMIT_LEVEL_QUEUE = Queue()
    commit_level_thread_list = []
    pill2kill = threading.Event()

    pull_ids = get_pull_ids_list_from_repo(repo)

    for pull_info in pull_ids:
        COMMIT_LEVEL_QUEUE.put(pull_info)

    for newThread in range(100):
        commit_level_thread = threading.Thread(target=kickoff_commit_level_thread_queue,
                                  args=[[repo, COMMIT_LEVEL_QUEUE, pill2kill]])
        commit_level_thread.daemon = True
        commit_level_thread_list.append(commit_level_thread)
        commit_level_thread.start()

    COMMIT_LEVEL_QUEUE.join()

    time.sleep(1)
    for commit_level_thread in commit_level_thread_list:
        commit_level_thread.join()
    return

def kickoff_commit_level_thread_queue(data):
    while True:
        if data[1].empty():
            return
        pull_info = data[1].get()
        commit_level_thread_job(pull_info, data[0], data[1])
        data[1].task_done()

def commit_level_thread_job(pull_info, repo, COMMIT_LEVEL_QUEUE):
    try:
        original_url = "\nhttps://api.github.com/repos" + repo + "/pulls/" + pull_info[1] + "/commits"
        output_path = os.path.join(pull_info[0], pull_info[1])
        output_name = os.path.join(output_path, "commit_level.json")
        output_name = _make_commit_output_name(output_name)
        download_api_page_json(original_url, 1, output_name)
        print("Downloaded [%s json..." % (str(pull_info).split("\\")[-1].upper()))
    except Exception as error:
        print(error)
        COMMIT_LEVEL_QUEUE.put(pull_info)


def _make_commit_output_name(old_output_name):
    try:
        new_path = _make_commit_output_name_mac_version(old_output_name)
    except Exception:
        new_path = _make_commit_output_name_windows_version(old_output_name)

    return new_path


def _make_commit_output_name_mac_version(old_output_name):
    new_path = str()
    temp_str = str(old_output_name).split("/")
    temp_index = 0
    for element in temp_str:
        if element == 'pull_requests':
            break
        else:
            temp_index = temp_index + 1
    temp_str[temp_index] = 'commits'

    for element in temp_str:
        new_path = os.path.join(new_path, element)

    return "/" + new_path



def _make_commit_output_name_windows_version(old_output_name):
    temp_str = str(old_output_name).split("\\")
    temp_index = 0
    for element in temp_str:
        if element == 'pull_requests':
            break
        else:
            temp_index = temp_index + 1
    temp_str[temp_index] = 'commits'
    new_path = temp_str[0] + "\\"
    for index in range(1, len(temp_str)):
        new_path = os.path.join(new_path, temp_str[index])
    return new_path



def download_user_data(users_set,repo):
    PULL_REQUEST_QUEUE = Queue()
    pull_request_level_thread_list = []

    for user in users_set:
        PULL_REQUEST_QUEUE.put(user)

    for newThread in range(100):
        thread = threading.Thread(target = _kickoff_user_thread_queue, args = [[PULL_REQUEST_QUEUE, repo]])
        thread.daemon = True
        pull_request_level_thread_list.append(thread)
        thread.start()

    PULL_REQUEST_QUEUE.join()

    time.sleep(1)
    for thread in pull_request_level_thread_list:
        thread.join()
    return


def _kickoff_user_thread_queue(data):
    while True:
        if data[0].empty():
            return
        user_ID = data[0].get()
        _pull_user_thread_job(user_ID, data[0],data[1])
        data[0].task_done()


def _pull_user_thread_job(user_ID, PULL_REQUEST_QUEUE,repo):
    try:
        original_url = "https://api.github.com/user/"
        output_path = os.path.join(targetManager.get_json_github_users_file_path_to(repo))
        output_name = os.path.join(output_path, str(user_ID) + "_user.json")
        request = download_api_page_json(original_url + str(user_ID), 1, output_name)
        if request != 200:
            PULL_REQUEST_QUEUE.put(user_ID)

        print("Downloaded %s json..." % (str(user_ID).upper()))
    except Exception:
        PULL_REQUEST_QUEUE.put(user_ID)

if __name__ == '__main__':
    REPO = "/freeCodeCamp/freeCodeCamp"
    download_commit_level_jsons(REPO)