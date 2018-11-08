# Dev env for `github` and `arc` in laptop and remote machine

If you are coding in laptop (e.g. macbook) and testing in remote machine (e.g. EC2), this would be helpful for you!

## In local machine (e.g. your laptop)

Sync up your local branch with master (if necessary)
```
git fetch origin master && git rebase -i origin/master
```

You can't simply `git push` your `local_branch1` to remote origin github because, the `arc` CR will be merged to non-master branch remotely, that's probably not what you want.

Alternatively, you have to clone a new branch same as the `local_branch1`, then push to origin github, and the remote machine can pull the code.
```
REMOTE=remote_branch1 LOCAL=local_branch1; \
  git push origin --delete $REMOTE && git branch -D $REMOTE \
  && git checkout master && git pull \
  && git merge --squash $LOCAL \
  && git checkout -b $REMOTE \
  && git commit -a -m "debug1" \
  && git push --set-upstream origin $REMOTE \
  && git checkout $LOCAL
```

## In remote machine (e.g. EC2)

```
REMOTE=remote_branch1; \
  git checkout master \
  && git branch -D $REMOTE \
  && git pull \
  && git checkout $REMOTE
```
