import os
import tempfile
import time
from azure.cognitiveservices.speech import speech, SpeechConfig, AudioDataStream
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.service import aws_service
from main import LANG_ES, LANG_EN
from src.service.aws_service import upload_speech_to_s3

face_client = FaceClient(
    os.environ.get('AZURE_FACE_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_FACE_KEY'))
)

vision_client = ComputerVisionClient(
    os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_COMPUTER_VISION_KEY'))
)

speech_config = SpeechConfig(
    subscription=os.environ.get('AZURE_SPEECH_KEY'),
    region=os.environ.get('AZURE_SPEECH_REGION')
)


def init(app):
    pass


def text_to_speech(text: str, lang_raw: str):
    if lang_raw == LANG_ES:
        lang = 'es-ES'
    elif lang_raw == LANG_EN:
        lang = 'en-US'
    else:
        raise Exception('Lang not supported')

    # Create speech client
    speech_config.speech_synthesis_language = lang
    speech_synthesizer_client = speech.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None
    )

    # Store audio in S3
    with tempfile.NamedTemporaryFile(suffix='.wav') as t:
        result = speech_synthesizer_client.speak_text_async(text).get()
        stream = AudioDataStream(result)
        stream.save_to_wav_file(t.name)

        return upload_speech_to_s3(open(t.name, 'rb'), '.wav')


def image_to_text(file_name: str):
    file_url = aws_service.get_presigned_file_url('image_to_text', file_name)

    # Request OCR
    analysis = vision_client.read(file_url, raw=True)
    location = analysis.headers["Operation-Location"]
    id_location = len(location) - 36  # TODO Make max chars parameterizable
    operation = location[id_location:]

    # Wait until OCR completes
    i = 0
    while True:
        result = vision_client.get_read_result(operation)

        if i >= 10 or result.status == OperationStatusCodes.succeeded:
            break

        i = i + 1
        time.sleep(1)

    texts = [line.text for line in result.analyze_result.read_results[0].lines]

    return ' '.join(texts)


def image_analysis(file_name: str, lang_raw: str):
    if lang_raw == LANG_ES:
        lang = 'es'
    elif lang_raw == LANG_EN:
        lang = 'en'
    else:
        raise Exception('Lang not supported')

    file_url = aws_service.get_presigned_file_url('image_to_text', file_name)
    analysis = vision_client.describe_image(file_url, 1, lang)

    if not analysis:
        raise Exception('No analysis returned.')

    return analysis.captions[0].text
