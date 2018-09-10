import requests


def validate_repos(repo_list):
    error_list = list()

    for repo in repo_list:
        url: str = repo.url  # TODO: Not sure how to grab the repos url yet
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            error_list.append(repo)

    if error_list.__sizeof__() == 0:
        return True  # is valid
    else:
        return False  # is invalid, make main terminate the program!
