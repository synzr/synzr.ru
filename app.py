from flask import Flask
from flask_minify import Minify

from extensions import cache

import blueprints

app = Flask(__name__)
app.config.from_pyfile("configs/app.py")

cache.init_app(app)
Minify(app)

app.register_blueprint(blueprints.index)
app.register_blueprint(blueprints.api)
