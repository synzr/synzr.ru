from flask import Blueprint
from flask_restful import Api

from resources import ActivityResource

blueprint_name = "api_blueprint"
blueprint = Blueprint(blueprint_name, blueprint_name, url_prefix="/api/")

api = Api(blueprint)

api.add_resource(ActivityResource, "/activity/")
