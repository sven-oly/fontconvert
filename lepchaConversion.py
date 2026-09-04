# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from converterBase import ConverterBase

import re
import sys

thisDefaultOutputFont = 'Noto Sans Lepcha'

def sub21(m):
    return m.group(2) + m.group(1)

def sub312(m):
    return m.group(3) + m.group(1) + m.group(2)

def sub1(m):
    return m.group(1)

class lepchaConverter(ConverterBase):
    private_use_map = {
        'Munsalong': {
            '\u0021': '!',
            '\u0022': '\"',
            '\u0023': '\"',
            '\u0024': '$',
            '\u0025': '\u1c25',
            '\u0026': '\u1c24',
            '\u0027': '\'',
            '\u0028': '*',
            '\u0029': '\u1c25',
            '\u002a': '\u1c24',
            '\u002b': '\u1c36',
            '\u002c': '\u1c25',
            '\u002d': '-',
            '\u002e': '.',
            '\u0030': '\u1c40',
            '\u0031': '\u1c41',
            '\u0032': '\u1c42',
            '\u0033': '\u1c43',
            '\u0034': '\u1c44',
            '\u0035': '\u1c45',
            '\u0036': '\u1c46',
            '\u0037': '\u1c47',
            '\u0038': '\u1c48',
            '\u0039': '\u1c49',
            '\u003a': '\u1c2e',
            '\u003b': '\u1c2f',
            '\u003c': '\u1c31',
            '\u003e': '\u1c30',
            '\u003f': '\u1c32',

            '\u0040': '@',
            '\u0041': '\u1c00',
            '\u0042': '\u1c02',
            '\u0043': '\u1c03',
            '\u0044': '\u1c05',
            '\u0045': '\u1c06',
            '\u0046': '\u1c07',
            '\u0047': '\u1c08',
            '\u0048': '\u1c09',
            '\u0049': '\u1c0a',
            '\u004a': '\u1c0b',
            '\u004b': '\u1c0c',
            '\u004c': '\u1c0d',
            '\u004d': '\u1c0e',
            '\u004e': '\u1c10',
            '\u004f': '\u1c11',

            '\u0050': '\u1c13',
            '\u0051': '\u1c15',
            '\u0052': '\u1c17',
            '\u0053': '\u1c18',
            '\u0054': '\u1c19',
            '\u0055': '\u1c1a',
            '\u0056': '\u1c1b',
            '\u0057': '\u1c1c',
            '\u0058': '\u1c1d',
            '\u0059': '\u1c1f',
            '\u005a': '\u1c21',
            '\u005b': '\u1c2d',
            '\u005c': '\u1c37',
            '\u005d': '\u1c35\u200b',
            '\u005e': '\u1c36',
            '\u005f': '\u1c33',

            '\u0061': '\u1c36',
            '\u0062': '\u1c26',
            '\u0063': '\u1c28\u200b',
            '\u0064': '\u1c27\u200b',
            '\u0065': '\u1c36',
            '\u0066': '\u1c29\u200b',
            '\u0067': '\u1c2a',

            '\u0068': '\u1c2b',
            '\u0069': '\u1c2c',
            '\u006a': '\u1c34\u200b',
            '\u006b': '\u1c20',
            '\u006c': '\u1c22',
            '\u006d': '\u1c01',
            '\u006e': '\u1c04',
            '\u006f': '\u1c0f',

            '\u0070': '\u1c12',
            '\u0071': '\u1c14',
            '\u0072': '\u1c1e',
            '\u0073': '\u1c16',
            '\u0074': '\u1c00\u1c25\u1c37',
            '\u0075': '\u1c1d\u1c25\u1c37',
            '\u0076': '\u1c03\u1c25\u1c37',
            '\u0077': '\u1c23',
            '\u0078': '\u1c00\u1c37\u1c25\u1c2c',
            '\u0079': '\u1c1d\u1c37\u1c25\u1c2c',
            '\u007a': '\u1c03\u1c37\u1c25\u1c2c',
            '\u007b': '\u1c2d',
            '\u007c': '|',
            '\u007d': '%',

            '\u00c0': '+',
            '\u00c1': ':',
            '\u00c2': '+',
            '\u00c3': '(',
            '\u00c4': ')',
            '\u00c5': '[',
            '\u00c6': ']',
            '\u00c7': '{',
            '\u00c8': '}',
            '\u00c9': '<',
            '\u00ca': '>',
            '\u00cb': 'Ë',
            '\u00cc': 'Ì',
            '\u00cd': 'Í',
            '\u00ce': 'Î',
            '\u00cf': 'Ï',

            '\u00d2': '',
            '\u00d3': '',
            '\u00d4': '',
            '\u00d5': '',
            '\u00d6': '',
            '\u00d9': '',
            '\u00da': '',
            '\u00db': '',
            '\u00dc': '',
            '\u00dd': '',

            '\u00e0': '',
            '\u00e1': '',
            '\u00e2': '',
            '\u00e3': '',
            '\u00e4': '',
            '\u00e5': '',
            '\u00e8': '',
            '\u00e9': '',
            '\u00ea': '',
            '\u00eb': '',
            '\u00ec': '',
            '\u00ed': '',
            '\u00ee': '',
            '\u00ef': '',

            '\u00f2': 'ò',
            '\u00f3': 'ó',
        },
        'JG Lepcha': {
            '\u0021': '\u1c29\u200b\u1c2d',
            '\u0022': '\u1c29\u200b\u1c2e',
            '\u0023': '\u1c29\u200b\u1c2f',
            '\u0024': '\u1c29\u200b\u1c30',
            '\u0025': '\u1c29\u200b\u1c31',
            '\u0026': '\u1c29\u200b\u1c32',
            '\u0027': '\u1c29\u200b\u1c33',
            '\u0028': '\u1c2d\u1c36',
            '\u0029': '\u1c2e\u1c36',
            '\u002a': '\u1c2f\u1c36',
            '\u002b': '\u1c30\u1c36',
            '\u002c': ',',
            '\u002d': '\u1c31\u1c36',
            '\u002e': '\u1c3f',
            '\u0030': '\u1c40',
            '\u0031': '\u1c41',
            '\u0032': '\u1c42',
            '\u0033': '\u1c43',
            '\u0034': '\u1c44',
            '\u0035': '\u1c45',
            '\u0036': '\u1c46',
            '\u0037': '\u1c47',
            '\u0038': '\u1c48',
            '\u0039': '\u1c49',
            '\u003a': '\u1c27\u200b\u1c35\u200b',
            '\u003b': '\u1c37',
            '\u003c': 'v\u25CC',
            '\u003e': 'c/v\u25cc',
            '\u003f': '\u1c25',

            '\u0040': '\u1c32\u1c36',
            '\u0041': '\u1c23',
            '\u0042': '\u1c31',
            '\u0043': '\u1c07',
            '\u0044': '\u1c33',
            '\u0045': '\u1c14',
            '\u0046': '\u1c12',
            '\u0047': '\u1c05',
            '\u0048': '\u1c1e',
            '\u0049': '\u1c16',
            '\u004a': '\u1c09',
            '\u004b': '\u1c02',
            '\u004c': '\u1c2f',
            '\u004d': '\u1c2e',
            '\u004e': '\u1c30',
            '\u004f': '\u1c26\u200b',

            '\u0050': '\u1c10',
            '\u0051': '\u1c18',
            '\u0052': '\u1c32',
            '\u0053': '\u1c21',
            '\u0054': '\u1c0b',
            '\u0055': '\u1c2b',
            '\u0056': '\u1c35\u200b',
            '\u0057': '\u1c01',
            '\u0058': '\u1c2d',
            '\u0059': '\u1c0f',
            '\u005a': '\u1c34\u200b',
            '\u005b': '[',
            '\u005c': '/',
            '\u005d': ']',
            '\u005e': '\u1c33\u1c36',
            '\u005f': '\u1c36',

            '\u0061': '\u1c28\u200b',
            '\u0062': '\u1c13',
            '\u0063': '\u1c06',
            '\u0064': '\u1c0c',
            '\u0065': '\u1c2c',
            '\u0066': '\u1c11',
            '\u0067': '\u1c03',

            '\u0068': '\u1c1d',
            '\u0069': '\u1c27\u200b',
            '\u006a': '\u1c08',
            '\u006b': '\u1c00',
            '\u006c': '\u1c1c',
            '\u006d': '\u1c15',
            '\u006e': '\u1c0d',
            '\u006f': '\u1c29\u200b',

            '\u0070': '\u1c0e',
            '\u0071': '\u1c17',
            '\u0072': '\u1c1b',
            '\u0073': '\u1c20',
            '\u0074': '\u1c0a',
            '\u0075': '\u1c2a',
            '\u0076': '\u1c1f',
            '\u0077': '\u1c22',
            '\u0078': '\u1c04',
            '\u0079': '\u1c1a',
            '\u007a': '\u1c19',
            '\u007b': '{',
            '\u007c': '|',
            '\u007d': '}',

            '\u00c0': '\u1c00\u1c24',
            '\u00c1': '\u1c02\u1c24',
            '\u00c2': '\u1c03\u1c24',
            '\u00c3': '\u1c0a\u1c24',
            '\u00c4': '\u1c0b\u1c24',
            '\u00c5': '\u1c0c\u1c24',
            '\u00c6': 'Æ',
            '\u00c7': 'Ç',
            '\u00c8': '\u1c0e\u1c24',
            '\u00c9': '\u1c10\u1c24',
            '\u00ca': '\u1c11\u1c24',
            '\u00cb': '\u1c13\u1c24',
            '\u00cc': '\u1c15\u1c24',
            '\u00cd': '\u1c1b\u1c24',
            '\u00ce': '\u1c1c\u1c24',
            '\u00cf': '\u1c1d\u1c24',

            '\u00d2': '\u1c1f\u1c24',
            '\u00d3': '\u1c01\u1c24',
            '\u00d4': '\u1c04\u1c24',
            '\u00d5': '\u1c0f\u1c24',
            '\u00d6': '\u1c12\u1c24',
            '\u00d9': '\u1c14\u1c24',
            '\u00da': '\u1c16\u1c24',
            '\u00db': '\u1c1e\u1c24',
            '\u00dc': '\u1c23\u1c24',
            '\u00dd': '\u1c00\u1c25',

            '\u00e0': '\u1c03\u1c25',
            '\u00e1': '\u1c05\u1c25',
            '\u00e2': '\u1c0e\u1c25',
            '\u00e3': '\u1c11\u1c25',
            '\u00e4': '\u1c13\u1c25',
            '\u00e5': '\u1c15\u1c25',
            '\u00e8': '\u1c1d\u1c25 ',
            '\u00e9': '\u1c00\u1c25\u1c24',
            '\u00ea': '\u1c03\u1c25\u1c24',
            '\u00eb': '\u1c05\u1c25\u1c24',
            '\u00ec': '\u1c0e\u1c25\u1c24',
            '\u00ed': '\u1c11\u1c25\u1c24',
            '\u00ee': '\u1c13\u1c25\u1c24',
            '\u00ef': '\u1c15\u1c25\u1c24',

            '\u00f2': '\u1c1d\u1c25\u1c24',
            '\u00f3': '\u1c21\u1c24',
        },
        'Shipmoo Lepcha': {
            '\u0021': '!',
            '\u0022': '\"',
            '\u0023': '#',
            '\u0024': '$',
            '\u0025': '\u1c25',
            '\u0026': '\u1c24',
            '\u0027': '\'',
            '\u0028': '(',
            '\u0029': '\u1c25',
            '\u002a': '\u1c24',
            '\u002b': '\u1c36',
            '\u002c': ',',
            '\u002d': '-',
            '\u002e': '.',
            '\u0030': '\u1c40',
            '\u0031': '\u1c41',
            '\u0032': '\u1c42',
            '\u0033': '\u1c43',
            '\u0034': '\u1c44',
            '\u0035': '\u1c45',
            '\u0036': '\u1c46',
            '\u0037': '\u1c47',
            '\u0038': '\u1c48',
            '\u0039': '\u1c49',
            '\u003a': '\u1c2e',
            '\u003b': '\u1c2f',
            '\u003c': '\u1c31',
            '\u003e': '\u1c30',
            '\u003f': '\u1c32',

            '\u0040': '@',
            '\u0041': '\u1c00',
            '\u0042': '\u1c02',
            '\u0043': '\u1c03',
            '\u0044': '\u1c05',
            '\u0045': '\u1c06',
            '\u0046': '\u1c07',
            '\u0047': '\u1c08',
            '\u0048': '\u1c09',
            '\u0049': '\u1c0a',
            '\u004a': '\u1c0b',
            '\u004b': '\u1c0c',
            '\u004c': '\u1c0d',
            '\u004d': '\u1c0e',
            '\u004e': '\u1c10',
            '\u004f': '\u1c11',

            '\u0050': '\u1c13',
            '\u0051': '\u1c15',
            '\u0052': '\u1c17',
            '\u0053': '\u1c18',
            '\u0054': '\u1c19',
            '\u0055': '\u1c1a',
            '\u0056': '\u1c1b',
            '\u0057': '\u1c1c',
            '\u0058': '\u1c1d',
            '\u0059': '\u1c1f',
            '\u005a': '\u1c21',
            '\u005b': '\u1c2d',
            '\u005c': '\u1c37',
            '\u005d': '\u1c35\u200b',
            '\u005e': '^',
            '\u005f': '\u1c33',

            '\u0061': '\u1c36',
            '\u0062': '\u1c26',
            '\u0063': '\u1c28\u200b',
            '\u0064': '\u1c27\u200b',
            '\u0065': '\u1c36',
            '\u0066': '\u1c29\u200b',
            '\u0067': '\u1c2a',

            '\u0068': '\u1c2b',
            '\u0069': '\u1c2c',
            '\u006a': '\u1c34\u200b',
            '\u006b': '\u1c20',
            '\u006c': '\u1c22',
            '\u006d': '\u1c01',
            '\u006e': '\u1c04',
            '\u006f': '\u1c0f',

            '\u0070': '\u1c12',
            '\u0071': '\u1c14',
            '\u0072': '\u1c1e',
            '\u0073': '\u1c16',
            '\u0074': '\u1c4d',
            '\u0075': '\u1c4e',
            '\u0076': '\u1c4f',
            '\u0077': '\u1c23',
            '\u0078': 'x',
            '\u0079': 'y',
            '\u007a': 'z',
            '\u007b': '\u1c2d',
            '\u007c': '|',
            '\u007d': '}',

            '\u00c0': 'À',
            '\u00c1': 'Á',
            '\u00c2': 'Â',
            '\u00c3': 'Ã',
            '\u00c4': 'Ä',
            '\u00c5': 'Å',
            '\u00c6': 'Æ',
            '\u00c7': 'Ç',
            '\u00c8': 'È',
            '\u00c9': 'É',
            '\u00ca': 'Ê',
            '\u00cb': 'Ë',
            '\u00cc': 'Ì',
            '\u00cd': 'Í',
            '\u00ce': 'Î',
            '\u00cf': 'Ï',

            '\u00d2': '',
            '\u00d3': '',
            '\u00d4': '',
            '\u00d5': '',
            '\u00d6': '',
            '\u00d9': '',
            '\u00da': '',
            '\u00db': '',
            '\u00dc': '',
            '\u00dd': '',

            '\u00e0': '',
            '\u00e1': '',
            '\u00e2': '',
            '\u00e3': '',
            '\u00e4': '',
            '\u00e5': '',
            '\u00e8': '',
            '\u00e9': '',
            '\u00ea': '',
            '\u00eb': '',
            '\u00ec': '',
            '\u00ed': '',
            '\u00ee': '',
            '\u00ef': '',

            '\u00f2': 'ò',
            '\u00f3': 'ó',
        }
    }

    def __init__(self, old_font_list=None, newFont=None,
                 defaultOutputFont=thisDefaultOutputFont):
        super().__init__(old_font_list=self.private_use_map.keys())

        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())

        self.font_substitution = self.font_substitution_options = {
            'Shipmoo Lepcha': 'Mingzat',
            'Munsalong': 'Mingzat',
            'JG Lepcha': 'Mingzat',
        }

        self.thisDefaultOutputFont = 'Noto Serif Ahom'
        self.OUTPUT_FONTS = [self.thisDefaultOutputFont]

        self.unicode_fonts = [self.thisDefaultOutputFont]
        self.newFont = newFont
        self.defaultOutputFont = defaultOutputFont

        self.set_script_range(0x11700, 0x1173f)
        self.set_upper_case_range(0x11700, 0x1174f)
        self.description = 'Converts Ahom font encoding to Unicode'

        # Reordering operations
        self.pattern_replace_list = [
            # Move signs from before the consonant
            [re.compile(r'([\u1c27-\u1c29\u1c34-\u1c35])\u200b([\u1c27-\u1c29\u1c34-\u1c35])\u200b([\u1c00-\u1c23\u1c4d-\u1c4f])'),
             sub312],
            # # Combination move over consonants
            [re.compile(r'([\u1c27-\u1c29\u1c34\u1c35])\u200b([\u1c00-\u1c23\u1c4d-\u1c4f])'), sub21],
            # Move single over consonants
            # Move signs into the correct order
            [re.compile(r'(\u1c36)([\u1c24-\u1c35\u1c37]+)'), sub21],  # Move \u1c36
            [re.compile(r'([\u1c24-\u1c36]+)([\u1c37]+)'), sub21],  # Move \u1c37
            [re.compile(r'([\u1c2c-\u1c35]+)([\u1c24-\u1c2b\u1c37]+)'), sub21],  # The

            [re.compile(r'([\u1c26-\u1c2b]+)([\u1c24-\u1c25\u1c37]+)'), sub21],  # The
            [re.compile(r'([\u1c27])([\u1c25])'), sub21],  # The
            [re.compile(r'([\u1c2d\u1c35])([\u1c2c])'), sub21],  # The
            [re.compile(r'([\u1c34-\u1c35])([\u1c25-\u1c2c])'), sub21],
            [re.compile(r'([\u1c26-\u1c36]+)([\u1c24\u1c25\u1c37])'), sub21],
            [re.compile(r'([\u1c2d-\u1c36]+)([\u1c2a\u1c2b])'), sub21],
            [re.compile(r'([\u1c2e\u1c33]+)([\u1c28\u1c2c])'), sub21],
            [re.compile(r'([\u1c26\u1c2b\u1c31]+)([\u1c2c\u1c37])'), sub21],
            [re.compile(r'([\u1c27\u1c35]+)([\u1c24\u1c25])'), sub21],
            [re.compile(r'([\u1c36]+)([\u1c2b\u1c2d\u1c33])'), sub21],
            [re.compile(r'([\u1c2d]+)([\u1c2c])'), sub21],
            [re.compile(r'([\u1c28\u1c29]+)([\u1c24])'), sub21],
            [re.compile(r'([\u1c2d\u1c2f\u1c30\u1c31\u1c32\u1c35\u1c36]+)([\u1c28])'), sub21],
            # Remove
            [re.compile(r'(\u1c28)+'), sub1],  # Duplicate
            [re.compile(r'(\u1c31)+'), sub1],  # Duplicate
            [re.compile(r'(\u1c36)+'), sub1],  # Duplicate
            [re.compile(r'(\u1c2c\u1c33)+'), sub1],  # Duplicate

        ]

        self.bad_diacritic_order = [
        ]


def test_strings(converter):
    # List of font, encoded string, expected Unicode
    tests = [
        ['Shipmoo Lepcha', 'dH>QdH>', 'ᰉᰧᰰᰕᰉᰧᰰ'],
        ['Munsalong', 'dH>QdH>', 'ᰉᰧᰰᰕᰉᰧᰰ'],
        ['JG Lepcha', 'dHQdH', 'ᰌᰞᰘᰌᰞ'],
        ['Shipmoo Lepcha', 'fC& A_b WbcY', 'ᰃᰤᰩ ᰀᰦᰳ ᰜᰦᰟᰨ'],
        ['Munsalong', 'fC& A_b WbcY', 'ᰃᰤᰩ ᰀᰦᰳ ᰜᰦᰟᰨ'],
        ['Shipmoo Lepcha',
         'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
         'ᰀ ᰂ ᰃ ᰅ ᰆ ᰇ ᰈ ᰉ ᰊ ᰋ ᰌ ᰍ ᰎ ᰐ ᰑ ᰓ ᰕ ᰗ ᰘ ᰙ ᰚ ᰛ ᰜ ᰝ ᰟ ᰡ'],
        ['Shipmoo Lepcha',
         'a b c d e f g h i j k l m n o p q r s t u v w x y z',
         'ᰶ ᰦ ᰨ​ ᰧ​ ᰶ ᰩ​ ᰪ ᰫ ᰬ ᰴ​ ᰠ ᰢ ᰁ ᰄ ᰏ ᰒ ᰔ ᰞ ᰖ ᱍ ᱎ ᱏ ᰣ x y z'],
        ['JG Lepcha',
         'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
         'ᰣ ᰱ ᰇ ᰳ ᰔ ᰒ ᰅ ᰞ ᰖ ᰉ ᰂ ᰯ ᰮ ᰰ ᰦ​ ᰐ ᰘ ᰲ ᰡ ᰋ ᰫ ᰵ​ ᰁ ᰭ ᰏ ᰴ​'],
        ['JG Lepcha',
         'a b c d e f g h i j k l m n o p q r s t u v w x y z',
         'ᰨ​ ᰓ ᰆ ᰌ ᰬ ᰑ ᰃ ᰝ ᰧ​ ᰈ ᰀ ᰜ ᰕ ᰍ ᰩ​ ᰎ ᰗ ᰛ ᰠ ᰊ ᰪ ᰟ ᰢ ᰄ ᰚ ᰙ'],
        ['Munsalong',
         'a b c d e f g h i j k l m n o p q r s t u v w x y z',
         'ᰶ ᰦ ᰨ​ ᰧ​ ᰶ ᰩ​ ᰪ ᰫ ᰬ ᰴ​ ᰠ ᰢ ᰁ ᰄ ᰏ ᰒ ᰔ ᰞ ᰖ ᰀ᰷ᰥ ᰝ᰷ᰥ ᰃ᰷ᰥ ᰣ ᰀ᰷ᰥᰬ ᰝ᰷ᰥᰬ ᰃ᰷ᰥᰬ'],
        ['Munsalong',
         'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
         'ᰀ ᰂ ᰃ ᰅ ᰆ ᰇ ᰈ ᰉ ᰊ ᰋ ᰌ ᰍ ᰎ ᰐ ᰑ ᰓ ᰕ ᰗ ᰘ ᰙ ᰚ ᰛ ᰜ ᰝ ᰟ ᰡ'],
        ['Shipmoo Lepcha',
         'I[gdZ:, wbdY[,wb]cJ,wbfH?, ]fP]fI,wbJ[&b,wb]dAe, I[gfL:, wbdQ[+, M>gdEe.',
         'ᰊᰪᰭᰡᰧᰮ, ᰣᰦᰟᰧᰭ,ᰣᰦᰋᰨᰵ,ᰣᰦᰉᰩᰲ, ᰓᰩᰵᰊᰩᰵ,ᰣᰦᰋᰤᰦᰭ,ᰣᰦᰀᰧᰵᰶ, ᰊᰪᰭᰍᰩᰮ, ᰣᰦᰕᰧᰭᰶ, ᰎᰪᰰᰆᰧᰶ.'],
        ['Shipmoo Lepcha',
         'M>g]Gi kw[&b, O_b kw[*b, dQe kw[*b, k[gQ_g kw[*b, ]wh kw[&b, jW kw[&b, ]Ah kw[&b',
         'ᰎᰪᰰᰈᰬᰵ ᰠᰣᰤᰦᰭ, ᰑᰦᰳ ᰠᰣᰤᰦᰭ, ᰕᰧᰶ ᰠᰣᰤᰦᰭ, ᰠᰪᰭᰕᰪᰳ ᰠᰣᰤᰦᰭ, ᰣᰫᰵ ᰠᰣᰤᰦᰭ, ᰜᰴ ᰠᰣᰤᰦᰭ, ᰀᰫᰵ ᰠᰣᰤᰦᰭ'],
        ['Munsalong',
         'M>g]Gi kw[&b, O_b kw[*b, dQe kw[*b, k[gQ_g kw[*b, ]wh kw[&b, jW kw[&b, ]Ah kw[&b',
         'ᰎᰪᰰᰈᰬᰵ ᰠᰣᰤᰦᰭ, ᰑᰦᰳ ᰠᰣᰤᰦᰭ, ᰕᰧᰶ ᰠᰣᰤᰦᰭ, ᰠᰪᰭᰕᰪᰳ ᰠᰣᰤᰦᰭ, ᰣᰫᰵ ᰠᰣᰤᰦᰭ, ᰜᰴ ᰠᰣᰤᰦᰭ, ᰀᰫᰵ ᰠᰣᰤᰦᰭ'],
    ]
    for test in tests:
        result = converter.convertString(test[1], test[0], converter.private_use_map[test[0]])
        if result != test[2]:
            print('Failed: %s for \"%s\" :\n  %s\n  %s' % (test[0], test[1], result, test[2]))
        else:
            print('Passed: %s for \"%s\"' % (test[0], test[1]))

    return


def simple_tests(converter):
    return


def main(argv):
    converter = lepchaConverter()
    test_strings(converter)

    simple_tests(converter)


if __name__ == '__main__':
    main(sys.argv)
