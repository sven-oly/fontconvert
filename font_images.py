# -*- coding: utf-8 -*-
#
from PIL import Image, ImageDraw, ImageFont

# 1. Define configuration
HEX_CODE_POINT = "0x0061"  # Example: Greek small letter lambda (λ)
#FONT_PATH = "arial.ttf"    # Path to a TrueType/OpenType font file
FONT_PATH = "/static/fonts/Shan/hacked/SHAN.TTF"
FONT_SIZE = 1000
IMG_SIZE = (150, 150)

# 2. Convert code point to character string
code_point_int = int(HEX_CODE_POINT, 16)
char_to_draw = chr(code_point_int)

# 3. Create a blank image and a drawing context
image = Image.new("RGB", IMG_SIZE, color="white")
draw = ImageDraw.Draw(image)

# 4. Load the font and calculate text position to center it
try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except IOError:
    font = ImageFont.load_default()

# Get bounding box of the character
# Note: Newer Pillow versions use font.getbbox(), older ones use draw.textbbox()
bbox = draw.textbbox((0, 0), char_to_draw, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

# Calculate coordinates to center the character
x = (IMG_SIZE[0] - text_w) / 2
y = (IMG_SIZE[1] - text_h) / 2

# 5. Draw the character and save
draw.text((x, y), char_to_draw, font=font, fill="black")
image.save("character_image.png")
image.show()