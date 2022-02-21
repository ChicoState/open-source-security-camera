#Steps

from github, go to repo we want:

* Fork repo to my remote repository on github.
* Git clone <ssh_Address@git.github.com>
    - now it is in local repo on my PC.
* make changes ..
* git add file_name.<EXT>
* git commit -m "my commit message"
* git status or git log to make sure it's 'Staged'
* git push origin main
* git remote add upstream <upstream_url>
* git remote -v
    ##### check list of remotes for one just added (upstream)
* git pull upstream <branch_name>
* git commit -m "merged changes from upstream"
* git push origin main

* now sync with open_source sec_camera.