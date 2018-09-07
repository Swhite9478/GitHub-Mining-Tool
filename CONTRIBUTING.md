# Contributing to the GitHub-Mining-Tool

The following is a set of guidelines for contributing to the [GitHub-Mining-Tool](https://github.com/Swhite9478/GitHub-Mining-Tool) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

**If you don't want to read the entire contents of this file, rather, you have a question, feel free to reach out to the project's main contributors:**

* *Stephen White: SteveWhite.dev@gmail.com*

* *James Todd: JamesToddNau95@gmail.com*


# Table of Contents #

   [How Can I Contribute?](#how-can-i-contribute)

   * [Community Standards](#community-standards)

   * [I Don't have a personal branch Yet](#i-dont-have-a-personal-branch-yet)

   * [Branches and Contribution Flow](#branches-and-contribution-flow)

   * [Suggesting Enhancements](#suggesting-enhancements)


   [Style Guides](#style-guides)

   * [How to Properly Commit](#how-to-properly-commit)

   * [Python Code](#python-code)


---

# How Can I Contribute?

## Community Standards
   * The purpose of an open source project is to get new ideas from the general population so that a project can grow into something we would all be proud to use. If this is your first taste of an open source project, feel free to check out [The Cathedral and the Bazaar](http://www.catb.org/esr/writings/cathedral-bazaar/cathedral-bazaar/) by Eric Raymond. Here he explains where this crazy kind of workflow originated, and how it is useful!

   * If you disagree with someone's implementation, politely provide constructive criticism, along with an example of how it could be fixed. The goal is not to berate someone for making a mistake, we are all human.

   * ***Overall, be nice to one another, and respectful of other people's ideas. We wish to be a welcoming community, and are proud to help each other out. Anyone that exhibits toxic behavior may be blocked from the project.***

## I Don't have a personal branch Yet
   * Ensure that you have read the README to understand how to obtain the project and ensure that it is in working order.

   * From the command line, type in the following (substituting "john" with your desired branch name) and hit enter:
   ```
   $ git checkout -b "john" develop
   ```
   Now have created a branch off of develop, and it exists on your local machine. In order to ensure that your changes are present on GitHub, type the following (substituting "john" with the name of the branch you just created):
   ```
   $ git push origin "john"
   ```

   Congrats! You now have a branch in the repository!

## Branches and Contribution Flow
   * The repository is set up in the following manner in regard to branches:
      * ***master:***

      Houses the current stable release of the tool. This branch is the 'source of truth' if you will. The only way to modify this branch is to put in a pull request and meet the specifications listed below:
         1. Only submit a pull request to master from the **develop branch.** If you attempt to submit a pull request from your personal branch to master, it will be deleted, and you will most likely hear from the Admins.

         2. The pull request may not have any merge conflicts present upon merging into master. Put in the request, and fix all conflicts that arise before proceeding to the reviewal process.

         3. The pull request must be reviewed and approved by one of the main project contributors (either Stephen or James) before a merge into master may occur. If any additional changes are desired, the pull request will be commented upon by Stephen or James, and all changes should be pushed to your pull request so we may review the updated code.

         4. Once the code is deemed appropriate and has gone through the approval process, the pull request will be approved and merged into master.

      * ***develop:***

      Is a branch off of master Houses the current 'in progress' version of the tool. This branch is either a replica of master, or is currently ahead of it and will be eventually be merged into master to update it. Consider this branch a stable version of the tool as well, but with tweaks that still need to be added before it will be represented on master.

      The only way to modify this branch is to put in a pull request and meet the specifications listed below:
         1. Only submit a pull request to develop from a **personal branch.**

         2. ***Don't submit a pull request to develop unless your personal branch is currently up to date with develop. This will minimize merge conflicts. ALWAYS PULL FROM DEVELOP TO YOUR PERSONAL BRANCH BEFORE SUBMITTING A PULL REQUEST!***

         3. Follow all other steps outlined in master above.

      * ***personal branch:***

      This entails any and all personal branches, which are branched off of develop. **The only rule here is to only contribute to your own personal branch!** Feel free to pull changes from other's personal branches to your own if you want to fiddle around with their code.

      Once you have finished implementing a feature and would like to see it in the develop branch, follow the pull request steps listed above.

## Suggesting Enhancements
   * If you would like to request a feature, a bug fix, or any other enhancement to the source code you will perform the following procedures on the [Home page of this repo](https://github.com/Swhite9478/GitHub-Mining-Tool):

      1. Click on the *issues* tab on the home page of the project.

      2. Click the green *New issue* button.

      3. Add a nice descriptive title that can encapsulate the general idea of what you would like to implement.

      4. Make use of the comment section to provide a more complete description of what you would like to implement/have implement and make use of the markdown (.md) syntax as necessary, and click on the *preview* tab to see what the issue will look like to the rest of us.

         * Any code examples that you would like to type, make sure to encapsulate them in the following way:
         ```
         Code should look like this
         ```
      5. Once your description is complete, on the right hand side of the page make use of the following buttons:
         * **Labels:** Mark what kind of issue this is so it will be easier for the admins to track specific kinds of issues that were fixed/still need fixing. If you want to implement something yourself but want to request help, be sure to mark the issue with the *Help Wanted* label.

         * **Projects:** If you are requesting a change to the python source code, make sure you select *GitHub Data Mining Tool Python Code* so the issue will automatically be placed in the *To Do* section of the project Kanban board.

         * **Assignees:** If you would like to request that a specific person implement a change, add their name to this space and they will be notified.

      6. Your issue is now ready to be reviewed by the community!
---

# Style Guides

## How to Properly Commit
   * When you are making a commit, if you don't need a detailed message and only require a title, use:
   ```
   $ git commit -m "descriptive title"
   ```
   If you need a lengthy, more descriptive message, follow these procedures:
   ```
   type $ git commit
   ```
   Your window will change to your default CLI editor and prompt you to input information regarding your commit.

      * on the first line, ***in no more than 50 characters,*** create a meaningful title for your commit.

      * Hit enter twice, now ensure that the first character on this line is an asterisk (\*) and a space. Now you may begin typing a more detailed description of your contribution, ***not exceeding 80 characters per line.*** Should you get close to the 80 char limit, hit enter, ensure that the first char on that line is an asterisk (\*) and continue in this manner as needed.

## Python Code
   * A great starting place for understanding the basics of writing code that is clean and effective is by reading the book [Clean Code](https://www.investigatii.md/uploads/resurse/Clean_Code.pdf) by Robert C. Martin

   * In general, follow these practices when writing Python code for this project:
      1. All variables that are declared should be descriptive and words should be separated by underscores. e.g.
      ```
      my_num = 3

      this_is_a_string = "Hello World!"

      username_dict = {"username" : 12345}

      my_new_list = ['h', 'e', 'l', 'l', 'o']

      for list_index in range (0, len(repo_list)) ...

      for repository in repo_list ...
      ```
      Notice how no variable name is a single character? This not only makes the code easier to read, it cuts down on the need for useless comments.

      2. function names should also be descriptive and  words should be separated by underscores. e.g.
      ```
      def collect_repos_from_github(repo_list)...

      def this_function_does_something(arg_name_1, arg_name_2 ...)
      ```
      This is important for the same reason discussed above.

      3. If you introduce a new python script, make sure the first character is lowercase, and if it is more than one word, make use of camel case as follows:
      ```
      pullRequestCollector.py
      targetCreator.py
      logger.py

      etc.
      ```

      4. Use comments sparingly, and do so in the following way:
      ```
      # This comment may describe something about function_name below
      def function_name():

      for (thing in list):  # This comment may be brief to describe this loop
      ```
      The overall goal is to make your code as self-explainable as possible. Striving to upkeep the quality of this code is of the highest importance, and reviews of pull requests might include comments about code quality. Don't take this personally, we are all here to learn!
