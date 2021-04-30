import os
from argparse import ArgumentParser
from datetime import datetime
from itertools import groupby

from flask import Flask, render_template


def list_day_folders():
    all_date_folders = [
        _dir for _dir in os.listdir(app.config['data_folder'])
        if os.path.isdir(os.path.join(app.config['data_folder'], _dir))
    ]

    aggregated_folders = dict()

    for key, val in groupby(
            all_date_folders, key=lambda x: datetime.strptime(x, "%d%m%y").strftime("%m%y")
    ):
        aggregated_folders.setdefault(key, [])
        aggregated_folders[key].extend(list(val))

    for val in aggregated_folders.values():
        val.sort(key=lambda date: datetime.strptime(date, "%d%m%y"))
    return aggregated_folders


# да, это мерзко, но .strftime("%B %y") дает мне название в склонённой форме,
# а мне нужно в именительном падеже
ru_monthes = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
        'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]


def month_to_human_view(value):
    return ru_monthes[datetime.strptime(value, "%m%y").month - 1]


def init_app():
    parser = ArgumentParser()
    parser.add_argument(
        '--data-folder', '-d', type=str, default="/opt/atom_webcam/data",
        help='Папка с папками с изображениями.'
    )
    args = parser.parse_args()
    new_app = Flask(__name__, template_folder='templates')
    new_app.config.update(args.__dict__)
    new_app.jinja_env.filters['month2human_view'] = month_to_human_view
    new_app.jinja_env.globals.update(list_day_folders=list_day_folders)
    return new_app


app = init_app()


@app.route("/")
def index():
    return render_template('index.jinja2')


@app.route("/show_day/<day>")
def show_day(day: str):
    images_path = os.path.join(app.config['data_folder'], day)
    images = [
        item for item in os.listdir(images_path)
        if os.path.isfile(os.path.join(images_path, item))
    ]
    images.sort()
    return render_template('day_page.jinja2', day=day, images=images)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
