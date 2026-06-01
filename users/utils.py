import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from .constants import (
    AVATAR_COLORS,
    AVATAR_SIZE,
    FONT_COLOR,
    FONT_PATH_LINUX,
    FONT_PATH_MAC,
    FONT_SIZE,
)


def generate_avatar(name: str) -> ContentFile:
    letter = name[0].upper() if name else "?"
    bg_color = random.choice(AVATAR_COLORS)

    img = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH_MAC, size=FONT_SIZE)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype(FONT_PATH_LINUX, size=FONT_SIZE)
        except (IOError, OSError):
            font = ImageFont.load_default(size=FONT_SIZE)

    bbox = draw.textbbox((0, 0), letter, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_w) / 2 - bbox[0]
    y = (AVATAR_SIZE - text_h) / 2 - bbox[1]
    draw.text((x, y), letter, fill=FONT_COLOR, font=font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
