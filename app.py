from flask import Flask
import blueprints

app = Flask(__name__)
app.register_blueprint(blueprints.index)