from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class TextToSpeechForm(FlaskForm):
    text = TextAreaField('Texto', validators=[DataRequired(), Length(min=1, max=500)], render_kw={'class': 'form-control', "rows": 5})
    submit = SubmitField('Enviar', render_kw={'class': 'mt-1 btn btn-primary'})
