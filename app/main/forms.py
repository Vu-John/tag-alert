from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField, FormField
from wtforms.validators import ValidationError, DataRequired
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    send_email = BooleanField('Send Email')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class TagForm(FlaskForm):
    tag = TextAreaField('Enter a tag', validators=[DataRequired()])
    submit_tag = SubmitField('Submit')


class SubredditForm(FlaskForm):
    subreddit = TextAreaField('Enter a subreddit', validators=[DataRequired()])
    submit_subreddit = SubmitField('Submit')


class IndexForm(FlaskForm):
    tag_form = FormField(TagForm)
    subreddit_form = FormField(SubredditForm)
