from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):

    class Meta:
        csrf = False

    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit = SubmitField('Login')

class MessageForm(FlaskForm):

    class Meta:
        csrf = False

    message = StringField('Message', widget=TextArea(), validators=[InputRequired()])
    submit = SubmitField('Send')

class NoteForm(FlaskForm):

    class Meta:
        csrf = False

    username = StringField("Username", validators = [InputRequired()])
    note = StringField('Message', widget=TextArea(), validators=[InputRequired()])
    submit = SubmitField('Send')
