Komitet Git'a bezopasnosti
==========================

# Failing branch

This branch is used as an example of failing pr.

Komitet Git'a bezopasnosti (KGB) or Git security committee, is a commit message style enforcer.
It will listen to pull-request(pr) events from github, analyse the commit messages in the pr, and if there are any violations, it will submit a helpful if somewhat authoritative comment message and set the status to error. If there are no violations it will set the status to success.

If you want to run it you can use:
```
GH_TOKEN=`YOUR GITHUB TOKEN HERE` python -m komitet_git_bezopasnosti
```

Using docker remember to set the GH_TOKEN environment variable and link to port 5000.

The github token is needed to write the comment, set the pr status as well as access any private repo.
