import logging
from argparse import ArgumentParser
from time import sleep

import webcam

log = None


def setup_logger(debug=False):
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.basicConfig(format='%(name)s: %(asctime)s %(message)s')
    return logger


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
    log = setup_logger(args.debug)

    while True:
        try:
            log.debug("Получаем картинку...")
            webcam.main()
        except Exception as e:
            log.error(e)
        log.debug(f"Спим {args.interval} сек")
        sleep(args.interval)
