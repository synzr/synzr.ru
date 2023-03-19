from .base import BaseActivity
from ..activity_result import ActivityResult

import requests


class SteamActivity(BaseActivity):
    def __init__(self, url_id: str, steam_api_key: str) -> None:
        self.session = requests.Session()

        self.steam_api_key = steam_api_key
        self.steam_id = self._get_steam_id(url_id)
    
    def _get_steam_id(self, url_id: str) -> str:
        with self.session.get(
            "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",
            params={"key": self.steam_api_key, "vanityurl": url_id}
        ) as response:
            response.raise_for_status()

            result = response.json()["response"]
            assert(result["success"] == 1)

            return result["steamid"]
    
    def get_current_activity(self) -> ActivityResult:
        with self.session.get(
            "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
            params={"key": self.steam_api_key, "steamids": self.steam_id}
        ) as response:
            response.raise_for_status()

            result = response.json()["response"]
            player = result["players"][0]

            if player.get("gameid"):
                return ActivityResult(
                    is_in_game=True,
                    is_vkp_cloud_game=False,
                    game_url=f"https://store.steampowered.com/app/{player['gameid']}/",
                    game_icon_url="/static/img/logos/steam.svg", # TODO: Need to get game icon
                    game_title=player["gameextrainfo"]
                )

            return ActivityResult()
