from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, HiddenField, SelectField

from src.service.conversion_service import ENGINES


class ImageToTextForm(FlaskForm):
    engine = SelectField('Motor', choices=ENGINES, render_kw={'class': 'form-control'})
    image = FileField('Imagen', render_kw={'class': 'form-control-file'})
    file_name = HiddenField('file_name')
    file_mime_type = HiddenField('file_mime_type')
    btn_submit = SubmitField('Enviar', render_kw={'class': 'mt-1 btn btn-primary'})
