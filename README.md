# Tag Alert

An app for getting alerts on new reddit submissions based on user defined tags.

#### Example App Usage:
1. Sign up for an account and login
2. Add one or more subreddit to your account
3. Add one or more tag to your account
4. Go to profile page and edit profile and enable Send Email and submit
4. Log out
5. Now you should get an email notification when a new submission with your desired tag(s) gets posted to your specified subreddit(s)

## Environment Variables

Create a `.flaskenv` file in the root directory

```
FLASK_APP=tag_alert.py
SECRET_KEY=<SECRET_KEY_YOU_WILL_NEVER_GUESS>
SQLALCHEMY_DATABASE_URI=<DATA_BASE_URL> # (Optional) If not set SQLite database will be used

# Mail Credentials
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=<YOUR_GMAIL_EMAIL>
MAIL_PASSWORD=<YOUR_GOOGLE_APP_PASSWORD>

# Reddit Credentials
REDDIT_CLIENT_ID=<YOUR_REDDIT_CLIENT_ID>
REDDIT_CLIENT_SECRET=<YOUR_REDDIT_CLIENT_SECRET>
REDDIT_USERAGENT=<YOUR_USERAGENT>
```

## Installation

```
$ pip install -r requirements.txt
```

## Database Setup
```
$ flask db init
$ flask upgrade
```

## Running the application
```
$ flask run
```