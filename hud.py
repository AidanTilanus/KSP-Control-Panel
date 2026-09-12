import math

from PIL import Image, ImageDraw, ImageFont

# From the YM12864C datasheet: 62.0x44.0mm view area over 128x64 pixels.
PIXEL_ASPECT = (62.0 / 128) / (44.0 / 64)  # width/height per pixel, ~0.705

#SECTION - Helpers

#Thanks Claude for making this function I could have never produced myself.
def draw_orbit_shape(draw, eccentricity, periapsis_radius, body_radius,
                      focus=(80, 32), screen_size=(128, 64),
                      body_radius_px=3, pixel_aspect=PIXEL_ASPECT):
    """
    Draw the orbit outline anchored at `focus`, scaled so `body_radius` maps
    to `body_radius_px` pixels (true-to-scale relative to the body, not
    stretched to the screen). periapsis_radius/body_radius must share units
    (both km, both m, ...) and periapsis_radius is measured from the body's
    centre, e.g. kRPC's orbit.periapsis.

    Also compensates for the panel's non-square pixels via pixel_aspect.

    Returns (periapsis_px, apoapsis_px); apoapsis_px is None for e >= 1.
    """
    cx, cy = focus
    w, h = screen_size
    e = eccentricity
    n_points = 64

    px_per_unit = body_radius_px / body_radius
    rp = periapsis_radius * px_per_unit
    p = rp * (1 + e)

    theta_limit = math.pi if e < 1.0 else math.acos(-0.999 / e)
    step = theta_limit / n_points

    def to_screen(theta, r):
        return (cx + r * math.cos(theta), cy + r * math.sin(theta) * pixel_aspect)

    def side_points(sign):
        pts = []
        for i in range(n_points + 1):
            theta = sign * step * i
            r = p / (1 + e * math.cos(theta))
            x, y = to_screen(theta, r)
            if not (0 <= x < w and 0 <= y < h):
                break
            pts.append((x, y))
        return pts

    points = side_points(-1)[::-1][:-1] + side_points(1)
    if len(points) >= 2:
        draw.line(points, fill=1)

    periapsis_px = tuple(round(v) for v in to_screen(0.0, rp))
    apoapsis_px = None
    if e < 1.0:
        apoapsis_px = tuple(round(v) for v in to_screen(math.pi, p / (1 - e)))

    return periapsis_px, apoapsis_px

#SECTION - Pages

def test_page(draw: ImageDraw.ImageDraw, telemetry: dict):
    draw.text((2, 0), f"{math.floor(telemetry['altitude'])} m", fill=1)
    draw.text((2, 9), f"{math.floor(telemetry['apoapsis'])} m", fill=1)
    draw.text((2, 18), f"{math.floor(telemetry['periapsis'])} m", fill=1)

def orbit_page(draw: ImageDraw.ImageDraw, telemetry: dict):
    draw.font = ImageFont.truetype("fonts/KSP Controller.ttf", 5)
    
    draw.text((2, 2), f"Body: {telemetry['body'].name}", fill=1)
    draw.text((2, 57), f"I: {telemetry['inclination']:.1f}°", fill=1)
    
    draw.circle((80, 32), 2, fill=1, outline=1) # Body
    
    peri_x, apo_x = draw_orbit_shape(draw, telemetry['eccentricity'], 6, 2)

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
