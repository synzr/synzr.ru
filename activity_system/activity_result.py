from dataclasses import dataclass


@dataclass
class ActivityResult:
    is_in_game: bool = False
    is_vkp_cloud_game: bool = False # It is a VK Play Cloud game?
    game_url: str = ""
    game_icon_url: str = ""
    game_title: str = ""
