from main import ENGINE_AZURE, ENGINE_AWS
from src.service import aws_service
from src.service import azure_service


def text_to_speech(engine, lang, text):
    if engine == ENGINE_AWS:
        return aws_service.text_to_speech(text, lang)
    elif engine == ENGINE_AZURE:
        return azure_service.text_to_speech(text, lang)
    else:
        raise Exception('Engine not supported')


def speech_to_text(engine, lang, file_name):
    if engine == ENGINE_AWS:
        return aws_service.speech_to_text(file_name, lang)
    else:
        raise Exception('Engine not supported')


def image_to_text(engine, file_name):
    if engine == ENGINE_AWS:
        return aws_service.image_to_text(file_name)
    elif engine == ENGINE_AZURE:
        return azure_service.image_to_text(file_name)
    else:
        raise Exception('Engine not supported')
