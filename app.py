from flask import Flask
from extensions import cache

import blueprints

app = Flask(__name__)
app.config.from_pyfile("configs/app.py")

cache.init_app(app)

app.register_blueprint(blueprints.index)
app.register_blueprint(blueprints.api)
