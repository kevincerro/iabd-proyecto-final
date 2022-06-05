from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main import db, ENGINE_AWS
from src.entity.speech_to_text import SpeechToText
from src.form.speech_to_text_form import SpeechToTextForm
from src.service import conversion_service, aws_service

mod = Blueprint('dashboard_speech_to_text', __name__, url_prefix='/dashboard/speech-to-text')


@mod.route('/')
@login_required
def list_action():
    conversions = SpeechToText.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/speech-to-text/list.twig', conversions=conversions)


@mod.route('/new', methods=["GET", "POST"])
@login_required
def new_action():
    form = SpeechToTextForm()

    if form.validate_on_submit():
        # Read form data
        lang = form.lang.data
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
        text = conversion_service.speech_to_text(ENGINE_AWS, lang, dest_file)

        # Store in db
        stt = SpeechToText(
            lang=lang,
            speech=dest_file,
            text=text,
            created_by=current_user.id
        )
        db.session.add(stt)
        db.session.commit()

        return redirect(url_for('dashboard_speech_to_text.list_action'))

    return render_template('dashboard/speech-to-text/new-edit.twig', form=form)
