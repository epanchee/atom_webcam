import locale
import os
from argparse import ArgumentParser
from datetime import datetime
from functools import reduce

from flask import Flask, render_template, redirect, url_for
from flask_caching import Cache


def list_day_folders():
    all_date_folders = [
        _dir for _dir in os.listdir(app.config['data_folder'])
        if os.path.isdir(os.path.join(app.config['data_folder'], _dir))
    ]

    aggregated_folders = dict()

    for folder_path in all_date_folders:
        dt = datetime.strptime(folder_path, "%d%m%y")
        aggregated_folders.setdefault(dt.year, dict())
        aggregated_folders[dt.year].setdefault(dt.month, [])
        aggregated_folders[dt.year][dt.month].append(folder_path)

    for months in aggregated_folders.values():
        for day in months.values():
            day.sort(key=lambda date: datetime.strptime(date, "%d%m%y"))

    return aggregated_folders


# да, это мерзко, но .strftime("%B %y") дает мне название в склонённой форме,
# а мне нужно в именительном падеже
ru_monthes = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
    'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]


def month_to_human_view(value):
    return ru_monthes[value - 1]


def get_month_by_day(day):
    return datetime.strptime(day, "%d%m%y").month


def get_year_by_day(day):
    return datetime.strptime(day, "%d%m%y").year


def to_human_dmy(date_str):
    return datetime.strptime(date_str, "%d%m%y").strftime("%d %B %Y")


def to_human_dm(date_str):
    return datetime.strptime(date_str, "%d%m%y").strftime("%d %B")


def today():
    return datetime.now().strftime("%d%m%y")


def init_app():
    parser = ArgumentParser()
    parser.add_argument(
        '--data-folder', '-d', type=str, default="/opt/atom_webcam/data",
        help='Папка с папками с изображениями.'
    )
    args = parser.parse_args()
    new_app = Flask(__name__, template_folder='templates')
    new_app.config.update(args.__dict__)
    new_app.jinja_env.filters.update(
        month2human_view=month_to_human_view,
        get_month_by_day=get_month_by_day,
        get_year_by_day=get_year_by_day,
        to_human_dmy=to_human_dmy,
        to_human_dm=to_human_dm
    )
    new_app.jinja_env.globals.update(
        list_day_folders=list_day_folders,
        today=today,
        MAIN_TITLE='Atom Webcam Gallery'
    )
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    new_app.config.update({
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": 'cache',
    })
    return new_app


app = init_app()
cache = Cache(app)
cache.init_app(app)


@app.route("/")
def index():
    return redirect(url_for('show_day', day=today()))


def need_caching(day):
    if day == today():
        return True
    images_path = os.path.join(app.config['data_folder'], day)
    if os.path.exists(images_path):
        images = [os.path.join(images_path, image) for image in os.listdir(images_path)]
        count = reduce(lambda acc, item: acc + 1 if os.path.isfile(item) else acc, images, 0)
        cached_count = cache.get(day)
        if count and cached_count != count:
            cache.set(day, count)
            return True

    return False


@app.route("/show_day/<day>")
@cache.cached(timeout=None, unless=lambda _, day=None: day and need_caching(day))
def show_day(day: str):
    images_path = os.path.join(app.config['data_folder'], day)
    images = None
    if os.path.exists(images_path):
        images = [
            item for item in os.listdir(images_path)
            if os.path.isfile(os.path.join(images_path, item))
        ]
        images.sort()
    return render_template('day_page.jinja2', day=day, images=images)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
