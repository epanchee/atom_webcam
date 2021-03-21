import base64
import json
import logging
import os
from datetime import datetime
from time import sleep
from urllib.parse import quote

import urllib3
from requests import Request, Session

urllib3.util.url.QUERY_CHARS |= {'%'}

MAIN_URL = 'https://www.atomstroy.net'
SRC_URL = f'{MAIN_URL}/zhilaya_nedvizhimost/art-gorod-park'
ORIGIN = 'https://webcam.atomsk.ru:3001'
GET_PARAMS = {
    'vid': 'itip',
    'w': '100%',
    'h': '700px',
    'src': SRC_URL,
    'f': 1,
    'wc': '100%'
}
URL = f'{ORIGIN}/index'
REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': MAIN_URL,
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'iframe'
}

REQ2_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': ORIGIN,
    'Referer': URL,
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}
DATA_PATH = '/tmp/data'
DEBUG = False
log = None


def setup_logger(debug=False, name=''):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    if debug:
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
    logging.basicConfig(format='%(name)s: %(asctime)s %(message)s',
                        filename='/var/log/atom_webcam.log')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if debug else logging.INFO)
    formatter = logging.Formatter('%(name)s: %(asctime)s %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger


def main():
    img_name_template = f'{DATA_PATH}/atom.{{0}}.jpg'
    log = setup_logger(debug=DEBUG, name=__file__)
    s = Session()
    req = Request(method='GET', params=GET_PARAMS, url=URL, headers=REQ_HEADERS)
    preped = req.prepare()
    preped.url = preped.url.replace('%25', '%')
    log.debug("Делаем первый запрос, чтобы установить куки")
    s.send(preped)

    try:
        post_data = {
            'url': f'{quote(SRC_URL, safe="")}',
            'camid': 43
        }
        sleep(0.1)
        req = Request(method='POST', url=f'{ORIGIN}/updimg', data=post_data, headers=REQ2_HEADERS)
        log.debug("Делаем второй запрос, чтобы получить картинку")
        response = s.send(req.prepare())
        resp_obj = json.loads(response.content.decode())
        imgdata = base64.b64decode(resp_obj['SnapshotImg'])
        os.makedirs(img_name_template[:img_name_template.rindex('/')], exist_ok=True)
        img_path = img_name_template.format(int(datetime.now().timestamp()))
        log.debug(f"Сохраняем картинку в {img_path}")
        with open(img_path, 'wb') as f:
            f.write(imgdata)
        log.debug("Готово")
    except Exception as e:
        log.error(e)


if __name__ == '__main__':
    main()