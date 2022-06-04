from src.service import aws_service
from src.service import azure_service

ENGINE_AWS = 'aws'
ENGINE_AZURE = 'azure'
ENGINES = (
    (ENGINE_AWS, 'AWS'),
    (ENGINE_AZURE, 'Azure')
)


def image_to_text(engine, file_name):
    if engine == ENGINE_AWS:
        return aws_service.image_to_text(file_name)
    elif engine == ENGINE_AZURE:
        return azure_service.image_to_text(file_name)
    else:
        raise Exception('Engine not supported')
