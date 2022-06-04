import os
import time
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.service import aws_service

face_client = FaceClient(
    os.environ.get('AZURE_FACE_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_FACE_KEY'))
)

vision_client = ComputerVisionClient(
    os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT'),
    CognitiveServicesCredentials(os.environ.get('AZURE_COMPUTER_VISION_KEY'))
)


def detect_faces_in_image(url: str):
    attributes = ['age', 'emotion']
    detected_faces = face_client.face.detect_with_url(url=url, return_face_attributes=attributes)

    if not detected_faces:
        return []

    # Find emotion with better score
    for face in detected_faces:
        emotions = face.face_attributes.emotion
        face.emotion = get_most_scored_emotion(emotions)

    return detected_faces


def get_most_scored_emotion(emotions):
    scores = {
        'anger': emotions.anger,
        'contempt': emotions.contempt,
        'disgust': emotions.disgust,
        'fear': emotions.fear,
        'happiness': emotions.happiness,
        'neutral': emotions.neutral,
        'sadness': emotions.sadness,
        'surprise': emotions.surprise,
    }

    name = max(scores, key=scores.get)
    score = scores[name]

    return {
        'name': name,
        'score': score,
    }


def describe_image(url: str, lang: str):

    analysis = vision_client.describe_image(url, 1, lang)

    if not analysis:
        raise Exception('No analysis returned.')

    return analysis.captions[0].text


def analyze_image(url: str, lang: str):
    features = [
        VisualFeatureTypes.tags,
        VisualFeatureTypes.color,
    ]

    analysis = vision_client.analyze_image(url, visual_features=features, language=lang)

    tags = [tag.name for tag in analysis.tags]
    color = analysis.color.accent_color

    return tags, color


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
