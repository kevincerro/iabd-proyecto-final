from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from main import LANGS


class TextToSpeechForm(FlaskForm):
    lang = SelectField('Idioma', choices=LANGS, render_kw={'class': 'form-control'})
    text = TextAreaField('Texto', validators=[DataRequired(), Length(min=1, max=500)], render_kw={'class': 'form-control', "rows": 5})
    submit = SubmitField('Enviar', render_kw={'class': 'mt-1 btn btn-primary'})
