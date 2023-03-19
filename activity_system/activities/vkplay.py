from .base import BaseActivity
from ..activity_result import ActivityResult
import json

import requests


class VKPlayActivity(BaseActivity):
    def __init__(self, slug: str) -> None:
        self.session = requests.Session()
        self.slug = slug
    
    def get_current_activity(self) -> ActivityResult:
        with self.session.get(
            "https://api.vkplay.ru/profile2new/get_main_page_info_for_slug",
            params={"slug": self.slug}
        ) as user_response:
            user_response.raise_for_status()

            user_result = user_response.json()
            assert(user_result["status"] == "ok")

            user_data = user_result["data"]

            if user_data["in_games"]:
                with self.session.get(
                    "https://api.vkplay.ru/play/games/get/",
                    params={"id": user_data["play_game_id"]}
                ) as game_response:
                    game_response.raise_for_status()
                    game_data = game_response.json()

                    return ActivityResult(
                        is_in_game=True,
                        is_vkp_cloud_game=(not game_data["has_distribution"]) and game_data["is_cloud"],
                        game_url=f"https://vkplay.ru/play/game/{game_data['slug']}",
                        game_icon_url=game_data["icon"],
                        game_title=game_data["name"]
                    )

            return ActivityResult()
