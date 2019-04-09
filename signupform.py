from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class SignUpForm(FlaskForm):
    username = StringField('Придумайте логин', validators=[DataRequired(), Length(min=5, max=25)])
    password = PasswordField('Придумайте пароль', validators=[DataRequired(),
                                                              EqualTo('confirm', message='Пароли должны совпадать'),
                                                              Length(min=8)])
    confirm = PasswordField('Повторите пароль')
    submit = SubmitField('Зарегистрироваться')
