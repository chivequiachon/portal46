# Portal46
This is a project which aims to guide new fans (and old fans as well) in the 46G fandom by providing some insights as to what N46 and K46 does and also by providing them subtitles for their favorite 46G-related shows.

# Basic Features
- A simple profile page for both N46 and K46.
- A simple page containing some download links to the shows they're part of.
- About page for me and how I came into the fandom.
- A simple newsfeeds. _**(to be followed)**_
- Album sales prediction and Member analytics. _**(to be followed)**_

# Basic Architecture
This web application will be hosted using Heroku (free dyno). Apart from that, information regarding these 2 groups and download links/urls will be stored in a google spreadsheet for easy updates and maintenance (this infos will be retrieved using Google App Script).

# Workflow
1. Clone this repository.
2. Create feature branches (i.e. feature/PORTAL46-[trello card number]_[branch name])and test it in your development machine.
3. If ever the development is finished, create pull request to _**feature/develop**_ and wait for review, the reviewer will test it in the staging environment.
4. If reviewer approves, the reviewer will be the one to create pull request to the _**master**_ branch from the _**feature/develop**_ branch.
5. Another reviewer will then test it on the production environment and if it is approved, the reviewer will then approve the _pull request_.
