# Create my own home page for web browser

Use a python script to create home page for navigation.



## NOTE - This is a synchronized multi-repo

There are 2 repositories working as backups for each other, which are

- From **Gitee**: [git@gitee.com:pyrad/HomePageMaker.git](git@gitee.com:pyrad/HomePageMaker.git)
- From **GitHub**: [git@github.com:Pyrad/HomePageMaker.git](git@github.com:Pyrad/HomePageMaker.git)

So the 2 repositories must be ***exactly the same*** as each other.

For daily use, clone it from Gitee, and add another URL from Github as `push` URL to keep them synced.

```bash
### Clone to local folder
$ git clone git@gitee.com:pyrad/HomePageMaker.git
### Check current fetch & push origin
$ git remote -v 
origin  git@gitee.com:pyrad/HomePageMaker.git (fetch)
origin  git@gitee.com:pyrad/HomePageMaker.git (push)
### Add another repo as *PUSH* origin
$ git remote set-url --add origin git@github.com:Pyrad/HomePageMaker.git
### Check current fetch & push origin again
$ git remote -v
origin  git@gitee.com:pyrad/HomePageMaker.git (fetch)
origin  git@gitee.com:pyrad/HomePageMaker.git (push)
origin  git@github.com:Pyrad/HomePageMaker.git (push)
```



Check the following pages to see how to set multiple remote origins on a same local repo:

- [Multiple Remote Repositories](https://pyrad.github.io/2022/05/16/multiple-remote-repositories/#more)
- [https://pyrads-notes.readthedocs.io/en/latest/Git/gitcmd.html](
