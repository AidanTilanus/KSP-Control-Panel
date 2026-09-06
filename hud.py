from PIL import Image, ImageDraw, ImageFont
from math import floor

def test_page(draw: ImageDraw.ImageDraw, telemetry: dict):
    draw.text((2,0), str(floor(telemetry["altitude"])) + " m", fill=0)
    draw.text((2,9), str(floor(telemetry["apoapsis"])) + " m", fill=0)
    draw.text((2,18), str(floor(telemetry["periapsis"])) + " m", fill=0)

PAGES = {
    0: test_page
}

current_page = 0

def get_current_page_function():
    return PAGES[current_page]

def render(telemetry):
    image = Image.new('1', (128, 64), 1)
    draw = ImageDraw.Draw(image)
    PAGES[current_page](draw, telemetry)
    return image
