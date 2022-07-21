import io
import os
import uuid
import requests
import numpy as np
from PIL import Image
from ISR.models import RRDN
from bs4 import BeautifulSoup
from pathlib import Path

def padNumber(num):
    string = str(num)
    return '0' * (3 - len(string)) + string


def fetchManga(link, fetchAll, startFrom=0, exclude=[]):

    domain = 'https://www.manga2000.com'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    page = requests.get(link, headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    allLinks = []
    if fetchAll:
        for link in soup.find('div', class_='linkchap').findChild('select').find_all('option'):
            if int(float(link.text)) >= startFrom and int(float(link.text)) not in exclude:
                allLinks.append(link['value'])
        print(f'Chapter(s) found {len(allLinks)}')
    else:
        allLinks.append(link)
    # Load model
    # rrdn = RRDN(weights='gans')
    for relativeLink in allLinks:
        if fetchAll:
            completeLink = domain + relativeLink[1:]
        else:
            completeLink = relativeLink
        page = requests.get(completeLink, headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('header', class_='entry-header').select('h1.entry-title')[0].text

        result = soup.find_all('figure', class_='wp-block-image')
        imageLinks = []
        for element in result:
            imageLinks.append(element.find('img')['data-src'])

        print('Image Found:', str(len(imageLinks)))
        Path(f"downloads/{title}").mkdir(parents=True, exist_ok=True)
        filesExist = len(os.listdir(f'downloads/{title}'))
        pageCount = 1
        for link in imageLinks:
            if pageCount > filesExist:
                filename = f'page{padNumber(pageCount)}-' + str(uuid.uuid1())
                response = requests.get(link)
                img = Image.open(io.BytesIO(response.content))
                """
                lr_img = np.array(img)
                sr_img = rrdn.predict(lr_img)
                Image.fromarray(sr_img).save(f'downloads/{title}/{filename}.jpg')
                """
                # Image.fromarray(img).save(f'downloads/{title}/{filename}.jpg')
                img.save(f'downloads/{title}/{filename}.jpg')
            print(f'Done Page{pageCount}')
            pageCount += 1

        print(f'{title} Done')


if __name__ == '__main__':
    fetchManga('https://www.manga2000.com/episode/3g0taj2kmjudynzs3737/hz6wbxvadv55s01b84092.html', fetchAll=True, startFrom=120, exclude=[])
