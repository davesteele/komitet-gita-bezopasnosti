import logging
import flask
from . import github
from . import rules

log = logging.getLogger(__name__)


def check_pr(commits_url, comments_url, status_url):
    github.update_status(status_url)
    all_errors = 0
    messages = []
    for commit in github.get_commits(commits_url):
        message = commit["commit"]["message"]
        errors = rules.apply(message)
        if len(errors) > 0:
            sha = commit["sha"]
            messages.append("\n".join([sha, github.quote(message), ""] +
                                      errors))
            all_errors += len(errors)

    log.debug(all_errors)
    github.upsert_comment(comments_url, messages)
    github.update_status(status_url, sum(len(err[1]) for err in errors))


def github_pr():
    body = flask.request.json
    if body is None:
        return "", 500
    keys = body.keys()
    if "zen" in keys:
        # This is the initial event sent to test the hook.
        return "", 204
    if "action" not in keys or "pull_request" not in keys:
        log.error({"error": "not_a_pull_request", "body": body})
        return "", 500
    elif body["action"] in {"assigned", "unassigned",
                            "labeled", "unlabeled", "closed"}:
        log.debug({"event": "non_event", "body": body})
        return "", 200
    elif body["action"] in {"opened", "reopened", "synchronize"}:
        log.debug({"event": "analyse_pr", "body": body})
        check_pr(body["pull_request"]["commits_url"],
                 body["pull_request"]["comments_url"],
                 body["pull_request"]["statuses_url"])
        return ""

    return "", 204


def setup(app):
    app.add_url_rule('/github/pr',
                     'github_pr',
                     github_pr,
                     methods=["POST"])
    return app
