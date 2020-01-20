import os
from app import create_app, db, scheduler
from app.cron import send_alerts
from app.models import User, Tag, Subreddit

app = create_app()

# In debug mode, Flask's reloader will load the flask app twice
# Do this to prevent the scheduler from running in the master process
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.start()
    app.apscheduler.add_job(
        func=send_alerts,
        trigger='cron',
        minute='*/10',
        hour='*',
        args=[app],
        id="send_alerts"
    )


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Tag': Tag,
        'Subreddit': Subreddit
    }
