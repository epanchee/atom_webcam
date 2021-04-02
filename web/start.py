import os
from argparse import ArgumentParser
from datetime import datetime

from flask import Flask, render_template


def list_day_folders():
    date_folders = [
        _dir for _dir in os.listdir(app.config['data_folder'])
        if os.path.isdir(os.path.join(app.config['data_folder'], _dir))
    ]
    date_folders.sort(key=lambda date: datetime.strptime(date, "%d%m%y"))
    return date_folders


def init_app():
    parser = ArgumentParser()
    parser.add_argument(
        '--data-folder', '-d', type=str, default="/opt/atom_webcam/data",
        help='Папка с папками с изображениями.'
    )
    args = parser.parse_args()
    new_app = Flask(__name__, template_folder='templates')
    new_app.config.update(args.__dict__)
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
    app.run(host='0.0.0.0')
