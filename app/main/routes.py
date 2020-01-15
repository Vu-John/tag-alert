from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, TagForm
from app.models import User, Tag
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TagForm()
    if form.validate_on_submit():
        query_user_tag = current_user.tags.filter(
            Tag.text == form.post.data).first()
        if query_user_tag is not None:
            flash('You have already added this tag')
        else:
            tag = Tag.query.filter_by(text=form.post.data).first()
            if tag is None:
                tag = Tag(text=form.post.data)
                db.session.add(tag)
            current_user.tags.append(tag)
            db.session.commit()
            flash('Your tag has been saved')
        return redirect(url_for('main.index'))
    tags = current_user.tags.all()
    return render_template('index.html', title='Home', form=form, tags=tags)


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
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
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
