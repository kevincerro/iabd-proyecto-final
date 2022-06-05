from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, HiddenField, SelectField
from main import ENGINES, LANGS


class SpeechToTextForm(FlaskForm):
    engine = SelectField('Motor', choices=ENGINES, render_kw={'class': 'form-control'})
    lang = SelectField('Idioma', choices=LANGS, render_kw={'class': 'form-control'})
    speech = FileField('Audio', render_kw={'class': 'form-control-file'})
    file_name = HiddenField('file_name')
    file_mime_type = HiddenField('file_mime_type')
    btn_submit = SubmitField('Enviar', render_kw={'class': 'mt-1 btn btn-primary'})
