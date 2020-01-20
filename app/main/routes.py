import json
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, IndexForm
from app.models import User, Tag, Subreddit
from app.main import bp
from app.reddit import sub_exists, get_tagged_submissions


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = IndexForm()
    if form.tag_form.submit_tag.data and form.tag_form.validate(form):
        tag_input = form.tag_form.tag.data
        query_user_tag = current_user.tags.filter(
            Tag.text == tag_input).first()
        if query_user_tag is not None:
            flash('You have already added this tag')
        else:
            tag = Tag.query.filter_by(text=tag_input).first()
            if tag is None:
                tag = Tag(text=tag_input)
                db.session.add(tag)
            current_user.tags.append(tag)
            db.session.commit()
            flash('Your tag has been saved')
        return redirect(url_for('main.index'))
    if (form.subreddit_form.submit_subreddit.data and
            form.subreddit_form.validate(form)):
        subreddit_input = form.subreddit_form.subreddit.data
        if not sub_exists(subreddit_input):
            flash(
                f'There aren\'t any subreddit with name: {subreddit_input}')
        else:
            query_user_subreddit = current_user.subreddits \
                .filter(Subreddit.sub == subreddit_input).first()
            if query_user_subreddit is not None:
                flash('You have already added this subreddit')
            else:
                subreddit = Subreddit.query.filter_by(
                    sub=subreddit_input).first()
                if subreddit is None:
                    subreddit = Subreddit(
                        sub=subreddit_input)
                    db.session.add(subreddit)
                current_user.subreddits.append(subreddit)
                db.session.commit()
                flash('Subreddit saved')
            return redirect(url_for('main.index'))
    tags = [tag.text for tag in current_user.tags.all()]
    subreddits = current_user.subreddits.all()
    submissions = get_tagged_submissions()
    return render_template(
        'index.html',
        title='Home',
        form=form,
        tags=tags,
        subreddits=subreddits,
        submissions=submissions,
        data=json.dumps(tags)
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.send_email = form.send_email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.send_email.data = current_user.send_email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/tag/remove/<tag_text>')
@login_required
def tag_remove(tag_text):
    tag = Tag.query.filter_by(text=tag_text).first()
    if tag is None:
        flash(f'Tag: {tag_text} not found.')
    else:
        current_user.tags.remove(tag)
        db.session.commit()
        flash(f'Tag: {tag_text} has been removed.')
    return redirect(url_for('main.index'))


@bp.route('/subreddit/remove/<subreddit>')
@login_required
def subreddit_remove(subreddit):
    subreddit = Subreddit.query.filter_by(sub=subreddit).first()
    if subreddit is None:
        flash(f'Subreddit: {subreddit.sub} not found.')
    else:
        current_user.subreddits.remove(subreddit)
        db.session.commit()
        flash(f'Subreddit: {subreddit.sub} has been removed.')
    return redirect(url_for('main.index'))
