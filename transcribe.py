import io
import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Developer/keys/ocr-key.json"


def imgToText(imageData):

    client = vision.ImageAnnotatorClient()

    if isinstance(imageData, str):
        with io.open(imageData, 'rb') as image_file:
            content = image_file.read()
    else:
        content = imageData

    image = vision.Image(content=content)

    response = client.text_detection(image=image, image_context={"language_hints": ["ja"]})
    texts = response.text_annotations

    if len(texts) != 0:
        transcription = texts[0].description.replace('\n', '')
    else:
        transcription = 'None'
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return transcription
