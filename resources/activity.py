from flask import current_app
from flask_restful import Resource

from activity_system import SteamActivity, VKPlayActivity

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
        
        if current_app.config.get("VKPLAY_URL"):
            vkplay_slug = current_app.config["VKPLAY_URL"].split("/profile/")[-1]
            self.vkplay_activity = VKPlayActivity(vkplay_slug)
        else:
            self.vkplay_activity = None
    
    @cache.cached(60)
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
        
        if self.vkplay_activity:
            current_activity = self.vkplay_activity.get_current_activity()

            if current_activity.is_in_game:
                if result["isActive"] and current_activity.is_vkp_cloud_game \
                    and (
                        current_activity.game_url.endswith("virtual_computer") or
                        current_activity.game_url.endswith("steam_launcher") or
                        current_activity.game_url.endswith("remote_desktop")
                    ):
                    result["isVKPCloud"] = True
                else:
                    result["isActive"] = not result["isActive"]
                    result["gameURL"] = current_activity.game_url
                    result["gameIconURL"] = current_activity.game_icon_url
                    result["gameTitle"] = current_activity.game_title
                    result["platform"] = "vkp"

        return result
