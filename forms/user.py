from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class RegisterForm(FlaskForm):
    email = EmailField('Электронный адрес', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Введите ваше имя', validators=[DataRequired()])
    about = TextAreaField('Если хотите, расскажите о себе')  #
    submit = SubmitField('Зарегестрироваться')

