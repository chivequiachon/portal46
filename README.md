# Portal46
This is a project which aims to guide new fans (and old fans as well) in the 46G fandom by providing some insights as to what N46 and K46 does and also by providing them subtitles for their favorite 46G-related shows.

# Basic Features
- A simple profile page for both N46 and K46.
- A simple page containing some download links to the shows they're part of.
- About page for me and how I came into the fandom.
- A simple newsfeeds. _**(to be followed)**_
- Album sales prediction and Member analytics. _**(to be followed)**_

# Basic Architecture
This web application will be hosted using Heroku (free dyno). Apart from that, information regarding these 2 groups and download links/urls will be stored in a google spreadsheet for easy updates and maintenance (these data will be retrieved using Google App Script).

# Git Branches
- feature(s) -> Each feature will have its own feature branches.
- develop -> All feature branches will be merged here and will be deployed to the staging. It will then undergo automated tests and if everything is fine, it will then be deployed to production.
- master -> The branch containing the code used in the production environment.

# Development Requirements
1. python 3.6+
2. pipenv

# Pipeline
We are using a simple Heroku pipeline containing one app for the staging and one app for the production. Any push performed to the _**feature/develop**_ branch will automatically be deployed in the staging environment and any push performed to the _**master**_ branch will automatically be deployed in the production environment.

# Workflow
1. Clone this repository.
2. Create feature branches (i.e. feature/PORTAL46-[trello card number]_[branch name])and test it in your development machine.
3. During development, create a virtual environment using _pipenv_ to install and encapsulate dependencies away from your original system. The presence of the pipfile will be the guide for the pipenv for the installation of dependencies. (For more information, please refer to [this](https://devcenter.heroku.com/articles/getting-started-with-python#declare-app-dependencies) page.)
4. If ever the development is finished, create pull request to _**feature/develop**_ and wait for review, the reviewer will test it in the staging environment.
5. If reviewer approves, the reviewer will be the one to create pull request to the _**master**_ branch from the _**feature/develop**_ branch.
6. Another reviewer will check it and if it is approved, the reviewer will then approve the _pull request_.
