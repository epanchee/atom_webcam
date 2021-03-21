import base64
import json
from datetime import datetime
from time import sleep
from urllib.parse import quote

import requests
from requests import Request, Session

# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

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
    'Connection': 'keep-alive',
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
    'Connection': 'keep-alive',
    'Origin': ORIGIN,
    'Referer': URL,
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}
img_name_template = '/tmp/atom.{0}.jpg'


def main():
    s = Session()
    req = Request(method='GET', params=GET_PARAMS, url=URL, headers=REQ_HEADERS)
    preped = req.prepare()
    preped.url = preped.url.replace('%25', '%')
    print(preped.url)
    response = s.send(preped)

    try:
        cookies = response.cookies or {}
        post_data = {
            'url': f'{quote(SRC_URL, safe="")}',
            'camid': 43
        }
        sleep(0.1)
        response = requests.post(url=f'{ORIGIN}/updimg', data=post_data, headers=REQ2_HEADERS,
                                 cookies=cookies)
        resp_obj = json.loads(response.content.decode())
        imgdata = base64.b64decode(resp_obj['SnapshotImg'])
        with open(img_name_template.format(datetime.now().timestamp()), 'wb') as f:
            f.write(imgdata)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
