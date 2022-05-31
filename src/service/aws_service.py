import os
import tempfile
from boto3 import Session

session = Session()
polly = session.client('polly')
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
    return upload_text_to_speech_to_s3(response['AudioStream'].read())


def upload_text_to_speech_to_s3(blob):
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
