import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google.cloud import translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Developer/keys/ocr-key.json"


def watson_jp_to_en(translateText):
    authenticator = IAMAuthenticator("yQdLnG0S4D5uUHuoG600gF_erI0TPM-mstBv3bO2pFqO")
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )

    language_translator.set_service_url(
        'https://api.jp-tok.language-translator.watson.cloud.ibm.com/instances/787408b0-dc97-49b0-84b1-d6726a8fc5fb')

    response = language_translator.translate(text=translateText, model_id='ja-en').get_result()

    return response['translations']


def google_jp_to_en(translateText):
    client = translate.TranslationServiceClient()

    response = client.translate_text(
        contents=translateText,
        target_language_code='en',
        source_language_code='ja',
        mime_type="text/plain",
        parent='projects/reference-rain-313307')

    return response.translations
