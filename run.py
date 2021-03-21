from argparse import ArgumentParser
from time import sleep

import webcam

log = None

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--interval', '-i', type=int, default=60,
        help='Интервал между запросами. Меньше 60 сек не имеет смысла.'
    )
    parser.add_argument(
        '--data_path', '-d', type=str,
        help='Папка, куда сохранять картинки', default='/tmp/data'
    )
    parser.add_argument('--debug', action='store_true', help='Set log level to DEBUG')
    args = parser.parse_args()
    webcam.DATA_PATH = args.data_path
    webcam.DEBUG = args.debug
    log = webcam.setup_logger(debug=args.debug, name=__file__)

    while True:
        try:
            log.debug("Получаем картинку...")
            webcam.main()
        except Exception as e:
            log.error(e)
        log.debug(f"Спим {args.interval} сек")
        sleep(args.interval)
