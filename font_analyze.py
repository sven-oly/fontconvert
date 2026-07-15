# -*- coding: utf-8 -*-
from fontTools.ttLib import TTFont

import sys
# Load the TTF file
font_path = 'static/fonts/Shan/hacked/SHAN.TTF'
font = TTFont(font_path)


def get_supported_characters(font_path):
    font = TTFont(font_path)
    # Fetch the best character map platform table automatically
    cmap = font.getBestCmap()

    # cmap returns a dict where key = decimal unicode, value = glyph name
    supported_chars = []
    for code, glyph_name in cmap.items():
        supported_chars.append({
            "hex": hex(code),
            "char": chr(code) if code <= 0x10ffff else "",  # Prevent overflow
            "glyph_name": glyph_name
        })

    return supported_chars


def main(argv):
    # Access the 'name' table (contains metadata)
    name_record = font['name'].names

    # Print key metadata (Name ID 1 = Family Name, 4 = Full Name, 0 = Copyright)
    for record in name_record:
        if record.nameID in [0, 1, 4, 5, 6]:
            print(f"NameID {record.nameID}: {record.toUnicode()}")

    chars = get_supported_characters(font_path)
    print('Supported characters in %s' % font_path)
    for code in chars:
        print('  %s' % code)

if __name__ == '__main__':
    main(sys.argv)
