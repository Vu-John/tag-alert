import re
from datetime import datetime
from flask import render_template
from flask_mail import Message
from threading import Thread
from app import db, mail, reddit
from app.email import send_email
from app.models import User, Subreddit


def send_alerts(app):
    with app.app_context():
        app.logger.info('*** Running send_alerts ***')
        users = User.query.all()
        subreddits = Subreddit.query.all()
        subreddit_submissions_dict = {}
        for subreddit in subreddits:
            submissions = reddit.subreddit(subreddit.sub).new(limit=25)
            subreddit_submissions_dict[subreddit] = submissions

        for user in users:
            if not user.send_email:
                continue
            user_subreddits = user.subreddits
            user_tags = user.tags
            send_to_user = []
            for user_subreddit in user_subreddits:
                for submission in subreddit_submissions_dict[user_subreddit]:
                    submission_date = datetime.utcfromtimestamp(
                        submission.created_utc)
                    # Send submission to user only if the user has not seen it yet
                    if submission_date > max(user.last_seen, user.last_email_sent):
                        for tag in user_tags:
                            if re.search(tag.text, submission.title, re.IGNORECASE):
                                send_to_user.append(submission)

            # If there are new submissions send and email to the user
            if send_to_user and user == User.query.all()[0]:
                user.last_email_sent = datetime.utcnow()
                db.session.commit()
                app.logger.info(f'Sending email to {user.email}')
                send_email(
                    '[Tag Alert] - New Submissions',
                    sender=app.config['ADMINS'][0],
                    recipients=[user.email],
                    text_body=render_template(
                        'email/tag_alert.txt', user=user, submissions=send_to_user
                    ),
                    html_body=render_template(
                        'email/tag_alert.html', user=user, submissions=send_to_user
                    )
                )
