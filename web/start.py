import os
from argparse import ArgumentParser

from flask import Flask, render_template


def init_app():
    parser = ArgumentParser()
    parser.add_argument(
        '--data-folder', '-d', type=str, default="/opt/atom_webcam/data",
        help='Папка с папками с изображениями.'
    )
    args = parser.parse_args()
    new_app = Flask(__name__, template_folder='templates')
    new_app.config.update(args.__dict__)
    return new_app


app = init_app()


@app.route("/")
def index():
    date_folders = sorted([
        _dir for _dir in os.listdir(app.config['data_folder'])
        if os.path.isdir(os.path.join(app.config['data_folder'], _dir))
    ])
    return render_template('index.jinja2', dates=date_folders)


@app.route("/show_day/<day>")
def show_day(day: str):
    images_path = os.path.join(app.config['data_folder'], day)
    images = [
        item for item in os.listdir(images_path)
        if os.path.isfile(os.path.join(images_path, item))
    ]
    return render_template('day_page.jinja2', day=day, images=images)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
