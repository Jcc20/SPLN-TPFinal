from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class ExtrairJson(FlaskForm):
    link = StringField('Website link')
    palavra = StringField('Palavra a procurar')
    submit = SubmitField('Procurar')