import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_SIZE = 128
AVATAR_COLORS = [
    (100, 149, 237),
    (119, 158, 203),
    (95, 158, 160),
    (143, 188, 143),
    (176, 196, 222),
    (135, 206, 250),
    (147, 112, 219),
    (188, 143, 143),
    (210, 180, 140),
    (152, 251, 152),
]
FONT_COLOR = (255, 255, 255)


def generate_avatar(name: str) -> ContentFile:
    letter = name[0].upper() if name else "?"
    bg_color = random.choice(AVATAR_COLORS)

    img = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=60)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=60)
        except (IOError, OSError):
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), letter, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_w) / 2 - bbox[0]
    y = (AVATAR_SIZE - text_h) / 2 - bbox[1]
    draw.text((x, y), letter, fill=FONT_COLOR, font=font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
