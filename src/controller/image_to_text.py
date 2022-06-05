from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main import db
from src.entity.image_to_text import ImageToText
from src.form.image_to_text_form import ImageToTextForm
from src.service import conversion_service, aws_service

mod = Blueprint('dashboard_image_to_text', __name__, url_prefix='/dashboard/image-to-text')


@mod.route('/')
@login_required
def list_action():
    conversions = ImageToText.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/image-to-text/list.twig', conversions=conversions)


@mod.route('/new', methods=["GET", "POST"])
@login_required
def new_action():
    form = ImageToTextForm()

    if form.validate_on_submit():
        # Read form data
        engine = form.engine.data
        file_name = form.file_name.data
        file_mime_type = form.file_mime_type.data

        # Copy & remove from upload to dest folder
        dest_file = None
        if aws_service.does_object_exists_in_temp(file_name):
            dest_file = aws_service.copy_object_from_temp_to_dest(file_name, 'image_to_text', file_mime_type)
            aws_service.delete_object_from_temp(file_name)

        if not dest_file:
            raise Exception('Uploaded object cannot be recovered.')

        # Process with selected engine
        text = conversion_service.image_to_text(engine, dest_file)

        # Store in db
        stt = ImageToText(
            engine=engine,
            image=dest_file,
            text=text,
            created_by=current_user.id
        )
        db.session.add(stt)
        db.session.commit()

        return redirect(url_for('dashboard_image_to_text.list_action'))

    return render_template('dashboard/image-to-text/new-edit.twig', form=form)