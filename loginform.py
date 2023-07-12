from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired

# FileField
# Если из формы добавлен файл, то обюращаться к нему при обработке формы следует так: f.form.<название поля с файлом
# ORM - Object Relationship Mapping


class LoginForm(FlaskForm):
    username = StringField('логин', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    file = FileField('файл')
    submit = SubmitField('Вход')
