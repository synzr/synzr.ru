from flask import Blueprint

blueprint_name = "index_blueprint"
blueprint = Blueprint(blueprint_name, blueprint_name)


@blueprint.get("/")
def index():
    return "Hello, world!"
