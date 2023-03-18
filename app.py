from flask import Flask
import blueprints

app = Flask(__name__)
app.config.from_pyfile("config.py", True)

app.register_blueprint(blueprints.index)