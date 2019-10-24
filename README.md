# GitHub-Mining-Tool

The purpose of this repository is to facilitate research for Marco Gerosa and Igor Steinmacher regarding drive by commits and pull requests. It allows for the collection of pooled data in a resulting .csv format, for further analysis in any statistical based language.

This tool is written in the Python programming language, and leverages the GitHub API to mine/download information in the form of JSON files, on provided repositories of interest chosen by Marco Gerosa and Igor Steinmacher (@igorsteinmacher).

This project uses [GitHub API v3](https://developer.github.com/v3/). Contributions to make it work with the [API v4](https://developer.github.com/v4/) and optimize it are more than welcome!

All relevant information about the project is presented below, but if you have any suggestions, or would like to contribute and have a question, feel free to reach out to the project's owners and main contributors: Stephen White, or James Todd.

Stephen White: SteveWhite.dev@gmail.com

James Todd: JamesToddNau95@gmail.com

***Requires python 3.6.0 interpreter or higher to successfully run.***

***This program currently works on Windows 10 & macOS High Sierra Version 10.13.6 at least. Other versions are untested.***

---

# How to get this Software: #

### Initial Repository Install ###
* Download/fork repository onto your local machine

   * ***Via command line (SSH):*** wherever you would like to clone the repository, type the following...:
   ```
   $ git clone git@github.com:Swhite9478/GitHub-Mining-Tool.git
   ```

   * ***Via Command Line (HTTPS):*** Wherever you would like to clone the repository, type the following...
   ```
   $ git clone https://github.com/Swhite9478/GitHub-Mining-Tool.git  
   ```

   * ***Via GitHub:*** Click "Clone or Download" -> "Download Zip File"
      * Extract zip folder to wherever you deem fit on your machine.


   * The repository is now on your local machine!

### Getting/Setting Up PyCharm ###
   * If you don't already have it, [install PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows).

   * Upon successful installation, Open PyCharm
      * If asked which Python interpreter you would like to use, follow the on screen instructions, and select python 3.6.0 or higher!
      * Click *File -> Open -> .../GitHub-Mining-Tool*
      * Click *Ok*
      * Click the dropdown arrow on the folder *python_code*
      * Right Click *src -> Mark Directory as -> root*

---

# Running The Program: #

### Initial Run
   * Right click on *main.py -> Run 'main'*

   * The program will create a Directory named *'Target'* and will fail initially.
      * **This is normal, and only occurs when 'Target' does not exist yet.**


   * Upon initial termination of the program perform the following steps:
      1. click the drop down arrows for *Target -> text_files*  
      2. Within the *src* folder, right click *collected_repos.txt -> copy*
      3. Under *'Target' -> 'text_files' -> '_collected_repos,'* right click -> *paste*
         * Now collected_repos.txt should be in *'Target' -> 'text_files' -> '_collected_repos'*

### Future Runs ###
   * Upon successful initialization of the *'Target'* Directory, right click *main.py -> Run 'main'*

   * Every repository within *collected_repos.txt* will now be analyzed, and data will be collected on every pull request, commit, and user that has contributed to the repo!

### I Ran main.py... What Happens Now? ###
   * All of raw information exists in the form of JSON files when requested from GitHub's API, and those files will be stored on your local machine within *'Target' -> 'json_files'*

   * These local JSON files will then be parsed by scripts, and each repo will generate a corresponding .csv file within *'Target' -> 'csv_files' -> REPO_NAME* that is comprised of information of interest.

   * In order to place all of the data we would like to analyze in one location, a script is responsible for traversing the Target directory structure, and combining all relevant .csv files into one singular .csv file located under *'Target' -> 'csv_files' -> '_important_csv_files'*

   * From here these CSV Files can be opened in the R programming language, or any other statistical based language to be analyzed.

---


# File Descriptions #

### main.py ###
   * This is the program entry point. Once this script is run, all relevant information regarding a repository will be collected, and CSV files containing the mined data will be available to the user.

### combineAllPullRequests.py
   * This script is responsible for combing through 'separated' Pull Request CSV files that exist in the Target Structure, and combine them into one amalgamated CSV file containing all relevant raw Pull Request Data.

### commitCollector.py
   * This script is responsible for collecting information on each commit that has been contributed to the set of repositories in *collected_repos.txt.*

### github.py
   * This class is a wrapper which will provide the necessary functionality to download JSON files from GitHub's API.

### logger.py
   * This class is responsible for housing the functionality of a LOGGER. See Q&A below for more information on the INFO_LOGGER & ERROR_LOGGER.

### pullRequestCollector.py
   * This script is responsible for calling necessary functions from research toolkit that will download pull request data from GitHub's API, and create the corresponding CSV files for each repo.

### researchToolkit.py
   * Contains helper methods for obtaining GitHub data, refining said data, and generating CSV files from the downloaded JSON files.

### targetCreator.py
   * This script will initialize the Target Directory structure by generating the Target directory, and populating it with the proper folders for each repository listed in *collected_repos.txt.*

### targetManager.py
   * A library created to allow for the easy creation and traversal of the Target Directory Structure. Through this class, the placing, and locating of files is abstracted to allow the developer to get more done in regard to file manipulation, with as little hassle as possible.  

### UsersCollector.py
   * This script is responsible for collecting information on each user that has contributed to the set of repositories in *collected_repos.txt.*

---

# Frequently Asked Questions #

### How long does main.py take to run?
   * Due to the massive amount of information we are collecting and GitHub's request rate, main.py may take up to a day to collect all 300 repos! If you want main to take less time, collect less repos!

### How exactly are you collecting data? ###
   * GitHub's API allows us to make requests to download information in the form of JSON files. Using HTTPS Basic [Authentication](https://developer.github.com/v3/auth/) (with fake github accounts that we made) we are allotted more requests per hour to the API. Cycling through these accounts in a dictionary, allows us to make the most out of the hourly request rate limit.

### Wouldn't OAuth work just as well??? #
   * You are right! It just so happens that at the time of the initial development of this tool, we had no idea that this form of authentication was a thing! We would like to move away from HTTPS Basic Authentication and on to OAuth to help speed up the collection of repository data

### What does [X Rate-Limit Reached] mean when I run main.py??? ###
   * Due to the [Rate Limit](https://developer.github.com/v3/rate_limit/) that GitHub enforces, we wrote some code that allows you to know when main.py is being halted & waiting for the request rate to be refreshed. We can only ping their server so many times a minute, so when you see this message, just be patient, data collection will continue soon.

### Is there any way to make data collection faster??? ###
   * Yes there is! As mentioned previously, each authenticated call to the GitHub API allows us a specific amount of requests per minute/hour. This means that the bottleneck for speed on the collection of repository data, is how many authenticated calls we can make! Herein lies the motivation to move away from HTTPS Basic Authentication and toward OAuth, so we will not need to take in anyone's User Name & Password, and can just use a token to authenticate a call! The more authenticated accounts calling the API, the more requests we can make per minute/hour, the faster the data will be collected!

   * If you would like to assist in this endeavor, send either Stephen or James an email!

### I don't like looking at the console for output, can I see the tool's progress in any other way??? ###
   * Yes you can! As the program is running, we have designed two separate logging systems that will update you on the status of the repository collection! This is the INFO_LOGGER and the ERROR_LOGGER, both contained within *'Target' -> 'text_files' -> '_important_text_files'*

   * The **INFO_LOGGER** will be updated dynamically to show you how long the program has been running, what repository it is currently collecting data on, and where in the collection process the tool is at with the given repo. Check this file if you would like a new view on the status of the tool!

   * The **ERROR_LOGGER** is exactly what it sounds like. Because there are so many moving parts to this tool, something may go wrong for any number of reasons. In the event that an error is thrown, it will be logged here, will state the repo, the function call it occurred in, and the status of the error.
