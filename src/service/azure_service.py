import os
import time
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.service import aws_service
from main import LANG_ES, LANG_EN

face_client = FaceClient(
    os.environ.get('AZURE_FACE_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_FACE_KEY'))
)

vision_client = ComputerVisionClient(
    os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_COMPUTER_VISION_KEY'))
)

def init(app):
    pass


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
