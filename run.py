import os
import transcribe
import translate
import cv2
import re


def run():
    for chapter in os.listdir('processedChapters/'):
        try:
            with open(f'Translations/{chapter}.txt') as f:
                print(f'Skipped {chapter}')
                continue
        except IOError:
            pass
        basePath = f'processedChapters/{chapter}'
        transcription = []
        i = 0
        for textbox in os.listdir(basePath):
            rawImg = cv2.imread(f'{basePath}/{textbox}')
            median = cv2.medianBlur(rawImg, 5)
            result = transcribe.imgToText(cv2.imencode('.jpg', median)[1].tobytes())
            if result != 'None':
                result = ''.join(list(filter(lambda c: not re.match(r'[a-zA-Z]+', c), result)))
                if result != '' and result != ' ':
                    print(result)
                    transcription.append(result)
        print(f'{chapter} Transcription Done')
        translationResult = translate.google_jp_to_en(transcription)
        print(f'{chapter} Translation Done')
        file = open(f'Translations/{chapter}.txt', 'w', encoding='utf8')

        for jpText, enText in zip(transcription, translationResult):
            file.write(jpText + '\n')
            file.write(enText.translated_text + '\n\n')
        file.close()


if __name__ == '__main__':
    run()