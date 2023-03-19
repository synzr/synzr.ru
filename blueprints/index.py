from flask import Blueprint, render_template, make_response
from extensions import cache

blueprint_name = "index_blueprint"
blueprint = Blueprint(blueprint_name, blueprint_name)


@blueprint.get("/")
@cache.cached(3600)
def index():
    return render_template("pages/index.html")
