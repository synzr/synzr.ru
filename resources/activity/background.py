from flask import current_app, abort, request
from flask_restful import Resource

from extensions import cache

from PIL import Image, ImageOps
from colorthief import ColorThief

from io import BytesIO
from base64 import urlsafe_b64decode, b64encode

import requests



class ActivityBackgroundResource(Resource):
    def __init__(self) -> None:
        super().__init__()

        self.session = requests.Session()
        self.mask_gradient = self._generate_gradient()
    
    # https://stackoverflow.com/questions/39842286/python-pillow-add-transparent-gradient-to-an-image
    def _generate_gradient(self):
        mask_gradients = []

        for size in [(2048, 1), (1, 2048)]:
            mask_gradient = Image.new('L', size, 0xFF)

            value_is_first = size[0] != 1
            value = size[0] if value_is_first else size[1]

            for a in range(value):
                mask_gradient.putpixel((a, 0) if value_is_first else (0, a), int(a / value * 255))
            
            mask_gradient = ImageOps.mirror(mask_gradient)
            mask_gradient = mask_gradient.resize((2048, 2048))

            mask_gradients.append(mask_gradient)
        
        left_gradient, top_gradient = mask_gradients
        
        mask_gradient = Image.composite(top_gradient, left_gradient, top_gradient)
        return mask_gradient

    def _generate_color_gradient(self, color: tuple[int], width: int, height: int):
        alpha_gradient = Image.new('RGBA', (width, height), color)
        alpha_gradient.putalpha(self.mask_gradient.resize((width, height)))

        return alpha_gradient

    def _generate_background(self, source_image: BytesIO):
        color_thief = ColorThief(source_image)
        darkest_color = min(color_thief.get_palette(color_count=6))

        destination_image = Image.open(source_image)
        destination_image = destination_image.convert("RGBA")

        width, height = destination_image.size

        gradient = self._generate_color_gradient(darkest_color, width, height)

        destination_image.alpha_composite(gradient)
        destination_image = destination_image.convert('RGB')

        return destination_image, darkest_color

    @cache.cached(3600)
    def get(self, base64_url: str):
        url = urlsafe_b64decode(
            base64_url.encode("ascii")
        ).decode("ascii")

        if not url.startswith("https://vkplay.ru/hotbox/") \
            and not url.startswith("https://cdn.akamai.steamstatic.com/steam/apps/"):
            return abort(400)

        with self.session.get(url, stream=True) as response:
            if response.status_code != 200:
                return abort(500)

            source_image = BytesIO()

            for chunk in response.iter_content(chunk_size=2048):
                source_image.write(chunk)
            
            source_image.seek(0, 0)

            generated_background, darkest_color = self._generate_background(source_image)
            generated_background_content = BytesIO()

            generated_background.save(generated_background_content, "jpeg", quality=75)

            return {
                "backgroundURL": "data:image/jpeg;base64," + b64encode(generated_background_content.getvalue()).decode("ascii"),
                "darkestColor": f"rgb({darkest_color[0]}, {darkest_color[1]}, {darkest_color[2]})"
            }
