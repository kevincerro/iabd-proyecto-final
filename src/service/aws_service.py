import os
import tempfile
import time

from boto3 import Session

session = Session()
polly = session.client('polly')
transcribe = session.client('transcribe')
s3 = session.client('s3')
s3_bucket: str = os.getenv('UPLOADS_BUCKET')


def init(app):
    pass


def text_to_speech(text):
    # Send to AWS Polly
    response = polly.synthesize_speech(
        Text=text,
        LanguageCode='es-ES',
        OutputFormat='mp3',
        VoiceId='Lucia'
    )

    # Store audio in S3
    return upload_speech_to_s3(response['AudioStream'].read())


def speech_to_text(file_url):
    transcribe.start_transcription_job(
        TranscriptionJobName=file_url,
        Media={'MediaFileUri': file_url},
        MediaFormat='mp3',
        LanguageCode='es-ES'
    )

    max_tries = 10
    while max_tries > 0:
        max_tries -= 1
        job = transcribe.get_transcription_job(TranscriptionJobName=file_url)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status == 'COMPLETED':
            return job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        time.sleep(1)

    raise Exception('Cannot convert speech-to-text')


def upload_speech_to_s3(blob):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as t:
        file_name = os.path.basename(t.name)
        s3.put_object(
            Body=blob,
            Bucket=s3_bucket,
            Key='text_to_speech/' + file_name
        )

        return file_name


def get_presigned_speech_url(speech):
    return s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': s3_bucket,
            'Key': 'text_to_speech/' + speech
        },
        ExpiresIn=3600
    )


def generate_random_file_name():
    with tempfile.NamedTemporaryFile() as file_name:
        return os.path.basename(file_name.name)


def get_presigned_upload_speech_url(file_name):
    return s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': s3_bucket,
            'Key': 'tmp_uploads/' + file_name
        },
        ExpiresIn=3600
    )
