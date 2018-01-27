# Portal46
This is a project which aims to guide new fans (and old fans as well) in the 46G fandom by providing some insights as to what N46 and K46 does and also by providing them subtitles for their favorite 46G-related shows.

# Basic Features
- A simple profile page for both Nogizaka46 and Keyakizaka46.
- A simple page containing some download links to the shows they're part of.
- About page for me and how I came into the fandom.
- A simple newsfeeds. _**(to be followed)**_
- Album sales prediction and Member analytics. _**(to be followed)**_

# Basic Architecture
This web application will be hosted using Heroku (free dyno). Apart from that, information regarding these 2 groups and download links/urls will be stored in a google spreadsheet for easy updates and maintenance (this infos will be retrieved using Google App Script).

# Git Branches
- feature(s) -> Each feature will have its own feature branches.
- develop -> All feature branches will be merged here and will be deployed to the staging. It will then undergo automated tests and if everything is fine, it will then be deployed to production.
- master -> The branch containing the code used in the production environment.
