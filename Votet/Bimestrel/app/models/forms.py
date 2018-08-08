from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

from wtforms.fields.html5 import EmailField

class LoginForm(Form):

    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])

class CommentForm(Form):
    comment = StringField('post', validators=[DataRequired()])