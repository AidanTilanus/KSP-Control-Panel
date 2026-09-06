from PIL import Image, ImageDraw, ImageFont
from math import floor

def test_page(draw: ImageDraw.ImageDraw, telemetry: dict):
    draw.text((2, 0), str(floor(telemetry["altitude"])) + " m", fill=1)
    draw.text((2, 9), str(floor(telemetry["apoapsis"])) + " m", fill=1)
    draw.text((2, 18), str(floor(telemetry["periapsis"])) + " m", fill=1)

def orbit_page(draw: ImageDraw.ImageDraw, telemetry: dict):
    draw.font = ImageFont.truetype("fonts/KSP Controller.ttf", 5)
    
    draw.ellipse((22, 19, 106, 44), fill=0, outline=1) #Orbit
    draw.ellipse((87, 29, 93, 34), fill=1, outline=1)  #Body
    
    draw.text((22, 32), str(floor(telemetry["apoapsis"])) + " m", fill=1)
    draw.text((87, 32), str(floor(telemetry["periapsis"])) + " m", fill=1)
    
    draw.text((2, 2), "Body: " + telemetry["body"].name, fill=1)

PAGES = {
    0: test_page,
    1: orbit_page
}

current_page = 1

def get_current_page_function():
    return PAGES[current_page]

def render(telemetry):
    image = Image.new('1', (128, 64), 0)
    draw = ImageDraw.Draw(image)
    PAGES[current_page](draw, telemetry)
    return image
