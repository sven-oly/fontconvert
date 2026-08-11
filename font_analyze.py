# -*- coding: utf-8 -*-
from fontTools.ttLib import TTFont
import fontTools.unicodedata as ut

import sys


def get_supported_characters(font_path):
    font = TTFont(font_path)
    # Fetch the best character map platform table automatically
    cmap = font.getBestCmap()
    htmx = font['hmtx']
    # cmap returns a dict where key = decimal unicode, value = glyph name
    supported_chars = []
    for code, glyph_name in cmap.items():
        char = chr(code)
        hex_char = hex(code)
        combining = False
        if ut.combining(char) > 0:
            combining = True
        advance_width, lsb = htmx[glyph_name]
        if advance_width <= 0 or lsb < 0:
            combining = True  # It may be a code point for a combiner
        supported_chars.append({
            "hex": hex(code),
            "char": chr(code) if code <= 0x10ffff else "",  # Prevent overflow
            "glyph_name": glyph_name,
            "combining": combining, # True is we think this is a combiner
            "advance_width": advance_width,
            'lsb':  lsb,
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
