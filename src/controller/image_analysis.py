from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main import ENGINE_AZURE, db
from src.entity.image_analysis import ImageAnalysis
from src.form.image_analysis_form import ImageAnalysisForm
from src.service import aws_service, conversion_service

mod = Blueprint('dashboard_image_analysis', __name__, url_prefix='/dashboard/image-analysis')


@mod.route('/')
@login_required
def list_action():
    conversions = ImageAnalysis.query.filter_by(created_by=current_user.id).all()

    return render_template('dashboard/image-analysis/list.twig', conversions=conversions)


@mod.route('/new', methods=["GET", "POST"])
@login_required
def new_action():
    form = ImageAnalysisForm()

    if form.validate_on_submit():
        # Read form data
        lang = form.lang.data
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
        text = conversion_service.image_analysis(ENGINE_AZURE, lang, dest_file)

        # Store in db
        stt = ImageAnalysis(
            lang=lang,
            image=dest_file,
            text=text,
            created_by=current_user.id
        )
        db.session.add(stt)
        db.session.commit()

        return redirect(url_for('dashboard_image_analysis.list_action'))

    return render_template('dashboard/image-analysis/new-edit.twig', form=form)
