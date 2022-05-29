from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TextToSpeechForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()], render_kw={'class': 'form-control'})
    text = TextAreaField('Texto', validators=[DataRequired()], render_kw={'class': 'form-control', "rows": 5})
    submit = SubmitField('Enviar', render_kw={'class': 'mt-1 btn btn-primary'})
