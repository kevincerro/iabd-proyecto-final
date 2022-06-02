from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user
from main import db
from src.entity.speech_to_text import SpeechToText
from src.entity.text_to_speech import TextToSpeech
from src.form.speech_to_text_form import SpeechToTextForm
from src.form.text_to_speech_form import TextToSpeechForm
from src.service import aws_service

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.text_to_speech'))


@mod.route('/text-to-speech')
@login_required
def text_to_speech():
    conversions = TextToSpeech.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/text-to-speech/list.twig', conversions=conversions)


@mod.route('/text-to-speech/new', methods=["GET", "POST"])
@login_required
def new_text_to_speech():
    form = TextToSpeechForm()

    if form.validate_on_submit():
        # Read form data
        text = form.text.data

        # Process with AWS Polly
        file_name = aws_service.text_to_speech(text)

        # Store in db
        tts = TextToSpeech(
            text=text,
            speech=file_name,
            created_by=current_user.id
        )
        db.session.add(tts)
        db.session.commit()

        return redirect(url_for('dashboard.text_to_speech'))

    return render_template('dashboard/text-to-speech/new-edit.twig', form=form)


@mod.route('/speech-to-text')
@login_required
def speech_to_text():
    conversions = SpeechToText.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/speech-to-text/list.twig', conversions=conversions)


@mod.route('/speech-to-text/new', methods=["GET", "POST"])
@login_required
def new_speech_to_text():
    form = SpeechToTextForm()

    if form.validate_on_submit():
        # Read form data
        file_name = form.file_name.data
        file_mime_type = form.file_mime_type.data

        # Copy & remove from upload to dest folder
        dest_file = None
        if aws_service.does_object_exists_in_temp(file_name):
            dest_file = aws_service.copy_object_from_temp_to_dest(file_name, 'speech_to_text', file_mime_type)
            aws_service.delete_object_from_temp(file_name)

        if not dest_file:
            raise Exception('Uploaded object cannot be recovered.')

        # Process with AWS Polly
        text = aws_service.speech_to_text(dest_file)

        # Store in db
        stt = SpeechToText(
            speech=dest_file,
            text=text,
            created_by=current_user.id
        )
        db.session.add(stt)
        db.session.commit()

        return redirect(url_for('dashboard.speech_to_text'))

    return render_template('dashboard/speech-to-text/new-edit.twig', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.index'))
