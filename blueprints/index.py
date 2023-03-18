from flask import Blueprint, render_template

blueprint_name = "index_blueprint"
blueprint = Blueprint(blueprint_name, blueprint_name)


@blueprint.get("/")
def index():
    return render_template("pages/index.html")
