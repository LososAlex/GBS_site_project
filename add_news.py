from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    project = SelectField('К какому проекту относится', coerce=str, choices=[
        ('CTK', 'Catch the key'),
        ('GiOL', 'Game in one level'),
        ('TM', 'The mountain')
    ])
    image = FileField('Загрузить фото', validators=[FileAllowed(['jpg', 'png'], 'Только картинки!')])
    submit = SubmitField('Добавить')
