from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class RegisterForm(FlaskForm):
    email = EmailField('Po4ta', validators=[DataRequired()])
    password = PasswordField('Parol', validators=[DataRequired()])
    password_again = PasswordField('Parol', validators=[DataRequired()])
    name = StringField('Vawe imya', validators=[DataRequired()])
    about = TextAreaField('Nemnogo o sebe')  #
    submit = SubmitField('Voiti')

