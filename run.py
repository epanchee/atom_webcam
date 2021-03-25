from argparse import ArgumentParser

import webcam
from schedule import Schedule

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
    parser.add_argument(
        '--schedule', '-s', type=str,
        help='JSON-файл с расписанием, по которому сохранять картинки', default='schedule.json'
    )
    parser.add_argument('--debug', action='store_true', help='Set log level to DEBUG')
    args = parser.parse_args()
    webcam.DATA_PATH = args.data_path
    webcam.DEBUG = args.debug
    log = webcam.setup_logger(debug=args.debug, name=__file__)
    schedule = Schedule(min_interval=args.interval, config=args.schedule, logger=log)

    while True:
        try:
            log.debug("Получаем картинку...")
            webcam.main()
        except Exception as e:
            log.error(e)
        schedule.do_sleep()
