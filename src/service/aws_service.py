import json
import os
import tempfile
import time
from urllib.request import urlopen
from boto3 import Session
from botocore.exceptions import ClientError
from main import LANG_ES, LANG_EN

UPLOADS_TEMP_DIR = 'tmp_uploads/'

session = Session()
polly = session.client('polly')
transcribe = session.client('transcribe')
rekognition = session.client('rekognition')
s3 = session.client('s3')
s3_bucket: str = os.getenv('UPLOADS_BUCKET')


def init(app):
    pass


def text_to_speech(text, lang_raw):
    if lang_raw == LANG_ES:
        lang = 'es-ES'
    elif lang_raw == LANG_EN:
        lang = 'en-EN'
    else:
        raise Exception('Lang not supported')

    # Send to AWS Polly
    response = polly.synthesize_speech(
        Text=text,
        LanguageCode=lang,
        OutputFormat='mp3',
        VoiceId='Lucia'
    )

    # Store audio in S3
    return upload_speech_to_s3(response['AudioStream'].read())


def speech_to_text(file_name, lang_raw):
    if lang_raw == LANG_ES:
        lang = 'es-ES'
    elif lang_raw == LANG_EN:
        lang = 'en-EN'
    else:
        raise Exception('Lang not supported')

    file_path = 's3://' + s3_bucket + '/speech_to_text/' + file_name

    transcribe.start_transcription_job(
        TranscriptionJobName=file_name,
        Media={'MediaFileUri': file_path},
        MediaFormat='mp3',
        LanguageCode=lang
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe.get_transcription_job(TranscriptionJobName=file_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status == 'COMPLETED':
            jsonurl = urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            data = json.loads(jsonurl.read())
            return data['results']['transcripts'][0]['transcript']
        time.sleep(1)

    raise Exception('Cannot convert speech-to-text')


def image_to_text(file_name):
    response = rekognition.detect_text(Image={
        'S3Object': {
            'Bucket': s3_bucket,
            'Name': 'image_to_text/' + file_name
        }
    })
    texts = [text['DetectedText'] for text in response['TextDetections'] if text['Type'] == 'LINE']

    return ' '.join(texts)


def upload_speech_to_s3(blob, suffix='.mp3'):
    with tempfile.NamedTemporaryFile(suffix=suffix) as t:
        file_name = os.path.basename(t.name)
        s3.put_object(
            Body=blob,
            Bucket=s3_bucket,
            Key='text_to_speech/' + file_name
        )

        return file_name


def get_presigned_file_url(folder, file_name):
    return s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': s3_bucket,
            'Key': folder + '/' + file_name
        },
        ExpiresIn=3600
    )


def generate_random_file_name():
    with tempfile.NamedTemporaryFile() as file_name:
        return os.path.basename(file_name.name)


def get_presigned_upload_url(file_name):
    return s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': s3_bucket,
            'Key': UPLOADS_TEMP_DIR + file_name
        },
        ExpiresIn=3600
    )


def does_object_exists_in_temp(file_name):
    file_name_without_extension = file_name.split('.')[0]
    path = UPLOADS_TEMP_DIR + file_name_without_extension

    try:
        s3.head_object(Bucket=s3_bucket, Key=path)
        return True
    except ClientError:
        return False


def copy_object_from_temp_to_dest(file_name, dest_folder, mime_type):
    file_name_without_extension = file_name.split('.')[0]
    source_file = s3_bucket + '/' + UPLOADS_TEMP_DIR + file_name_without_extension
    dest_file_name = generate_random_file_name()
    dest_file = dest_folder + '/' + dest_file_name

    s3.copy_object(
        Bucket=s3_bucket,
        Key=dest_file,
        CopySource=source_file,
        ContentType=mime_type,
        MetadataDirective='REPLACE'
    )

    return dest_file_name


def delete_object_from_temp(file_name):
    file_name_without_extension = file_name.split('.')[0]

    s3.delete_object(
        Bucket=s3_bucket,
        Key=UPLOADS_TEMP_DIR + file_name_without_extension
    )
