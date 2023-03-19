from flask import current_app
from flask_restful import Resource

from activity_system import SteamActivity

from extensions import cache


class ActivityResource(Resource):
    def __init__(self) -> None:
        super().__init__()

        if current_app.config.get("STEAM_URL") and current_app.config.get("STEAM_API_KEY"):
            steam_url_id = current_app.config["STEAM_URL"].split("/id/")[-1]
            if steam_url_id.endswith("/"): steam_url_id = steam_url_id[:-1]

            steam_api_key = current_app.config["STEAM_API_KEY"]

            self.steam_activity = SteamActivity(steam_url_id, steam_api_key)
        else:
            self.steam_activity = None
    
    def get(self):
        result = {"isActive": False}

        if self.steam_activity:
            current_activity = self.steam_activity.get_current_activity()

            if current_activity.is_in_game:
                result["isActive"] = not result["isActive"]
                result["gameURL"] = current_activity.game_url
                result["gameIconURL"] = current_activity.game_icon_url
                result["gameTitle"] = current_activity.game_title
                result["platform"] = "steam"

        return result
