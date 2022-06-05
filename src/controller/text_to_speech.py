from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main import db
from src.entity.text_to_speech import TextToSpeech
from src.form.text_to_speech_form import TextToSpeechForm
from src.service import conversion_service

mod = Blueprint('dashboard_text_to_speech', __name__, url_prefix='/dashboard/text-to-speech')


@mod.route('/')
@login_required
def list_action():
    conversions = TextToSpeech.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/text-to-speech/list.twig', conversions=conversions)


@mod.route('/new', methods=["GET", "POST"])
@login_required
def new_action():
    form = TextToSpeechForm()

    if form.validate_on_submit():
        # Read form data
        engine = form.engine.data
        lang = form.lang.data
        text = form.text.data

        # Process with AWS Polly
        file_name = conversion_service.text_to_speech(engine, lang, text)

        # Store in db
        tts = TextToSpeech(
            engine=engine,
            lang=lang,
            text=text,
            speech=file_name,
            created_by=current_user.id
        )
        db.session.add(tts)
        db.session.commit()

        return redirect(url_for('dashboard_text_to_speech.list_action'))

    return render_template('dashboard/text-to-speech/new-edit.twig', form=form)
