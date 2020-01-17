import re
from app import reddit
from flask_login import current_user
from prawcore import NotFound


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def get_submissions():
    subreddits = current_user.subreddits.all()
    submissions = []

    for subreddit in subreddits:
        submissions.extend(reddit.subreddit(subreddit.sub).new(limit=25))

    return submissions


def get_tagged_submissions():
    tags = [tag.text.lower() for tag in current_user.tags.all()]
    submissions = get_submissions()
    tagged_submissions = []
    for submission in submissions:
        title = submission.title
        for tag in tags:
            if re.search(tag, title, re.IGNORECASE):
                tagged_submissions.append(submission)
                break

    return tagged_submissions
