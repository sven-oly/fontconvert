# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from converterBase import ConverterBase

# Convert font encoded Assemse text in  'Tanmatra Boishakhi' text to Unicode.
tanmatra = 'Tanmatra Boishakhi'


# Swap order of two items
def sub21(m):
    return m.group(2) + m.group(1)

def sub312(m):
    g2 = ''
    if m.group(2):
        g2 = m.group(2)
    return m.group(3) + m.group(1) + g2

def sub231(m):
    return m.group(2) + m.group(3) + m.group(1)

def sub23451(m):
    return m.group(2) + m.group(3) + m.group(4) + m.group(5) + m.group(1)

def subzwsp(m):
    return '\u09cd\ufeff' + m.group(1)

def subf0cd_1(m):
    return '\u09f0\u09cd' + m.group(1)

def sub95cdf9_1(m):
    return '\u0995\u09cd\u09f0' + m.group(1)

def suba8cd84cd_1(m):
    return '\u09a8\u09cd\u09a4\u09cd' + m.group(1)

def sub95cda41(m):
    if m.group(1):
        g1 = m.group(1)
    else:
        g1 = ''
    return '\u0995\u09CD\u09A4' + g1


class sgp_converter(ConverterBase):

    def __init__(self):
        self.unicodeFont = 'Noto Bengali'
        super().__init__(old_font_list=[tanmatra], new_font=self.unicodeFont,
                         default_output_font=self.unicodeFont)

        self.private_use_map = {
            'Tanmatra Boishakhi': {
                # Extra
                '\u201e': '৷',
                # 0x20
                ' ': ' ',
                '!': '!',
                '\"': '\u2018',
                '#': '\u09d7',
                '$': '৮',
                '%': '%',
                '&': '\u25EF',
                '\'': '\u2019',
                '(': '(',
                ')': ')',
                '*': '\u00d7',
                '+': '+',
                ',': ',',
                '-': '-',
                '.': '.',
                '/': '/',

                # 0x30
                '0': '০',
                '1': '১',
                '2': '২',
                '3': '৩',
                '4': '৪',
                '5': '৫',
                '6': '৬',
                '7': '৭',
                '8': '৮',
                '9': '৯',
                ':': '\u0983',
                ';': ';',
                '<': '<',
                '=': '=',
                '>': '>',
                '?': '?',

                # 0x40
                '@': '@',
                'A': '\u0985',
                'B': 'ই',
                'C': 'ঈ',
                'D': 'উ',
                'E': '\u098a',
                'F': '\u098b',
                'G': '\u098F',
                'H': '\u0990',
                'I': '\u0993',
                'J': '\u0994',
                'K': '\u0995',
                'L': '\u0996',
                'M': '\u0997',
                'N': 'ঘ',
                'O': 'ঙ',

                # 0x50
                'P': 'চ',
                'Q': 'ছ',
                'R': 'জ',
                'S': 'ঝ',
                'T': 'ঞ',
                'U': 'ট',
                'V': 'ঠ',
                'W': 'ড',
                'X': 'ঢ',
                'Y': 'ণ',
                'Z': 'ত',
                '[': '[',
                '\\': '\u09f1',
                ']': ']',
                '^': '\u0981',
                '_': '_',

                # 0x60
                '`': '\u00f7',
                'a': 'থ',
                'b': 'দ',
                'c': 'ধ',
                'd': 'ন',
                'e': 'প',
                'f': 'ফ',
                'g': 'ব',
                'h': 'ভ',
                'i': 'ম',
                'j': 'য',
                'k': '\u09B0',
                'l': 'ল',
                'm': 'শ',
                'n': 'ষ',
                'o': 'স',

                # 0x70
                'p': 'হ',
                'q': 'ক্ষ',
                'r': '\u09dc',
                's': '\u09dd',
                't': '\u09df',
                'u': 'ৎ',
                'v': 'ং',
                '\u0077': 'া',
                'x': '\u09bf',
                'y': '\u09c0',
                'z': '\u09cd',
                '{': '{',
                '|': '\u09be',
                '}': '}',
                '~': '\u0995\u09cd\u0995',

                # 0xa0
                ' ': 'X',
                '¡': '\u09A3\u09CD\u09A1',
                '¢': '\u09A4\u09CD\u09F0',
                '£': '\u0995',
                '\u00a3': '\u09a4\u09cd\u09a4',
                '¤': '\u09a4\u09CD\u09A5',
                '¥': '\u09A6\u09CD\u09A6',
                '¦': 'দ্ধ',
                '\u00a7': '\u09A6\u09CD\u09ac',
                # ?? '§': 'দ্\u09A6\u09CD\u09Ac',
                '¨': '\u09a6\u09CD\u09AD',
                '©': '\u09A6\u09CD\u09F0',
                'ª': '\u09A3\u09CD\u09A0',
                '\u00ab': '\u09a8\u09cd\u09a1',
                '\u00ac': '\u09a8\u09cd\u09a7',
                '­': 'ন্ড',
                '®': 'প্ত',
                '¯': '\u09AA\u09CD\u09AA',

                # 0xb0
                '\u00b0': '\u09ab\u09cd\u09f0',
                '\u00b1': '\u09ac\u09cd\u099c',
                '\u00b2': '\u09ac\u09cd\u09a6',
                '\u00b3': '\u09AC\u09CD\u09A6\u09CD\u09B9',
                '\u00b4': '\u09f0',
                '\u00b5': '\u09cd\u09ac',
                '\u00b6': '\u09a6\u09cd\u09a7',
                '\u00b7': '·',
                '\u00b8': '\u09AD\u09CD\u09b0',
                '¹': '\u09AE\u09CD\u09AC',
                'º': '\u09AE\u09CD\u09AD',
                '»': '\u09AE\u09CD\u09AD\u09CD\u09AC',
                '¼': '\u09F5\u2044\u09ea',
                '½': '\u09F5\u2044\u09e8',
                '¾': '\u09F8\u2044\u09ee',
                '¿': '\u09B2\u09CD\u0995',

                # 0xc0
                '\u00c0': '\u09B2\u09CD\u09A1',
                '\u00c1': '\u09B2\u09CD\u09B2',
                '\u00c2': '\u09B6\u09C1',
                '\u00c3': '\u09b6\u09cd\u09a4',
                '\u00c4': '\u09B7\u09CD\u099F',
                '\u00c5': '\u09B7\u09CD\u09A0',
                '\u00c6': '\u09b8\u09CD\u0995',
                '\u00c7': '\u09b8\u09cd\u0995\u09cd\u09f0',
                '\u00c8': 'স্ব',
                '\u00c9': 'হু',
                '\u00ca': '\u09b9\u09CD\u09ae',
                '\u00cb': '\u09c7',
                '\u00cc': '\u09c7',  # ['হু',
                '\u00cd': 'ন্ম',
                '\u00ce': 'ন্ম',
                '\u00cf': '॥',

                # 0d0
                '\u00d0': '\u09c8',
                '\u00d1': '\u09c8',
                '\u00d2': '\u09a8\u09cd\u09a8',  # Ò
                '\u00d4': '\u09c2',
                '\u00d6': '\u09c1',
                '\u00d7': '\u09c1',
                '\u00d8': '\u09c1',
                '\u00d9': '\u09c3',
                '\u00da': '\u09c3',
                '\u00de': '\u09cd\u09b0',
                '\u00df': '\u09cd\u09a4',

                # 0xe0
                '\u00e0': 'গ',
                '\u00e1': 'ঙ\u09cd',
                '\u00e2': '\u099a\u09cd',
                '\u00e3': '\u099E\u09CD\u099A',
                '\u00e4': 'ও',
                '\u00e5': '\u09a3\u09cd',
                '\u00e6': '\u09a4',
                '\u00e7': '\u0993',
                '\u00e8': '\u098f',
                '\u00e9': '\u099E\u09CD\u099A',
                '\u00ea': '\u09b0\u09cd',
                '\u00eb': '\u09a8\u09cd',
                '\u00ec': '\u09a8\u09cd',
                '\u00ed': '\u09cd\u09a8',
                '\u00ee': '\u09cd\u09a8',
                '\u00ef': ' ',

                # 0xf0
                '\u00f0': '\u09cd\u09ac',
                '\u00f1': '\u09cd\u09ac',
                '\u00f2': '\u09cd\u09ac',
                '\u00f3': '\u09ae\u09cd',
                '\u00f4': '\u09cd\u09ae',
                '\u00f5': '\u09b2',
                '\u00f6': '\u09cd\u09b2',
                '\u00f7': '\u09a7',
                # '\u00f8': '\u09cd\u09af',
                '\u00f8': '\u09cd\u09af',
                '\u00f9': '\u09b2\u09cd',  # OK
                '\u00fa': '\u09b6\u09cd',
                '\u00fb': '\u09b7\u09cd',
                '\u00fc': '\u09b7\u09cd',
                '\u00fd': '\u09b8\u09cd',
                '\u00fe': '\u09b8\u09cd',
                '\u00ff': '\u09cd\u09a5',

                '\u0152': '\u099c\u09cd\u099c',
                '\u0153': '\u09a1\u09cd\u09a1',
                '\u0160': '\u0999\u09CD\u0997',
                '\u0161': '\u099C\u09CD\u099E',
                '\u0178': '\u09a3\u09CD\u09a0',
                '\u2014': '\u099e\u09cd\u099a',
                '\u2018': '\u2018',
                '\u2019': '\u2019',
                '\u201c': '\u201c',
                '\u201d': '\u201d',
                '\u201e': '\u0964',
                '\u2020': '\u0997\u09c1',
                '\u2021': '\u0997\u09cd\u0997',
                '\u2022': '???',
                '\u2026': '\u0995\u09cd\u09b8',
                '\u2030': '\u0999\u09cd\u0995',
                '\u2039': '???',
                '\u203a': '\u099f\u09cd\u099f',
                '\u20ac': '\u0965',
                '\u2122': '\u099e\u09cd\u099c',
            },
            'Tanmatra Boishakhi old': {
                ' ': ' ',
                '!': '!',
                '\"': '\u2018',
                '#': '\u09d7',
                '$': '৮',
                '%': '%',
                '&': '\u25EF',
                '\'': '\u2019',
                '(': '(',
                ')': ')',
                '*': '\u00d7',
                '+': '+',
                ',': ',',
                '-': '-',
                '.': '.',
                '/': '/',

                # 0x30
                '0': '০',
                '1': '১',
                '2': '২',
                '3': '৩',
                '4': '৪',
                '5': '৫',
                '6': '৬',
                '7': '৭',
                '8': '৮',
                '9': '৯',
                ':': '\u0983',
                ';': ';',
                '<': '<',
                '=': '=',
                '>': '>',
                '?': '?',

                # 0x40
                '@': '\u09A8\u09CD\u09A1',
                'A': 'অ',
                'B': 'ই',
                'C': 'ঈ',
                'D': 'উ',
                'E': '\u098a',
                'F': '\u09e0',
                'G': '\u098F',
                'H': '\u0990',
                'I': '\u0993',
                'J': '\u0994',
                'K': '\u0995',
                'L': '\u0996',
                'M': '\u0997',
                'N': 'ঘ',
                'O': 'ঙ',
                # 0x50
                'P': 'চ',
                'Q': 'ছ',
                'R': 'জ',
                'S': 'ঝ',
                'T': 'ঞ',
                'U': 'ট',
                'V': 'ঠ',
                'W': 'ড',
                'X': 'ঢ',
                'Y': 'ণ',
                'Z': 'ত',
                '[': '[',
                '\\': '\u09f1',
                ']': ']',
                '^': '\u0981',
                '_': '_',
                # 0x60
                '`': '\u00f7',
                'a': 'থ',
                'b': 'দ',
                'c': 'ধ',
                'd': 'ন',
                'e': 'প',
                'f': 'ফ',
                'g': 'ব',
                'h': 'ভ',
                'i': 'ম',
                'j': 'য',
                'k': 'র',
                'l': 'ল',
                'm': 'শ',
                'n': 'ষ',
                'o': 'স',

                # 0x70
                'p': 'হ',
                'q': 'ক্ষ',
                'r': 'ড়\u09bc',
                's': 'ঢ়\u09bc',
                't': 'য়\u09bc',
                'u': 'ৎ',
                'v': 'ং',
                'w': 'া',
                'x': '\u09bf',
                'y': '\u09c0',
                'z': '\u09cd',
                '{': '{',
                '|': '|',
                '}': '}',
                '~': '\u0995\u09cd\u0995',

                # 0xa0
                '\u00a0': 'X',
                '¡': '\u09A3\u09CD\u09A1',
                '¢': '\u09A4\u09CD\u09F0',
                '£': '\u09A4\u09CD\u09A4',
                '¤': '\u09A4\u09CD\u09A5',
                '¥': '\u09A6\u09CD\u09A6',
                '¦': 'দ্ধ',
                '§': 'দ্\u09A6\u09CD\u09Ac',
                '¨': '\u09A6\u09CD\u09AD',
                '©': '\u09A6\u09CD\u09F0',
                'ª': '\u09A3\u09CD\u09A0',
                '«': 'দ্র',
                '¬': 'ম্',
                '\u00AD': 'ন্ড',
                '®': 'প্ত',
                '¯': '\u09AA\u09CD\u09AA',

                # 0xb0
                '±': 'জ',
                '²': '\u0b21',
                '³': '\u09AC\u09CD\u09A6\u09CD\u09B9',
                '´': '\u09f0',
                'µ': '\u09ac',
                '¶': '\u09ac',
                '·': 'দ্ধ',
                '¸': '\u09AD\u09CD\u09AC',
                '¹': '\u09AE\u09CD\u09AC',
                'º': '\u09AE\u09CD\u09AD',
                '»': '\u09AE\u09CD\u09AD\u09CD\u09AC',
                '¼': '\u09fc\u2044\u093a',
                '½': '\u09fc\u2044\u0938',
                '¾': '\u09f8\u2044\u093a',
                '¿': '\u09B2\u09CD\u0995',

                # 0xc0
                'À': '\u09B2\u09CD\u09B2',
                'Á': '\u09B6\u09CD\u09C1',
                'Â': 'প্ত',
                'Ã': '\u09B7\u09CD\u099F',
                'Ä': '\u09B7\u09CD\u09A0',
                'Å': 'ঠ',
                'Æ': 'স্ক',
                'Ç': 'ক্র',
                'È': 'স্ব',
                'É': 'হু',
                'Ê': '\u09B9\u09CD\u09B9',
                'Ë': '\u09c7',
                'Ì': '\u09c7',  # ['হু',
                'Í': 'ন্ম',
                'Î': '€',
                'Ï': '॥',

                # 0xd0
                '\u00d0': '\u09c8',
                '\u00d2': '\u09a8\u09cd\u09a8',  # Ò
                '\u00d1': '\u09c8',
                '\u00d4': '\u09c2',
                '\u00d6': '\u09c1',
                '\u00d7': '\u09c1',
                '\u00d8': '\u09cd\u09a4',
                '\u00d9': '\u09c3',
                '\u00da': '\u09c3',
                '\u00de': '\u09cd',
                '\u00df': '\u09cd\u09f0',

            # 0xe0
                'à': 'গ',
                'á': 'ঙ',
                'â': 'চ',
                'ã': '\u099E\u09CD\u099A',
                'ä': 'ও',
                'å': '০',
                'æ': '৩',
                'ç': '\u0993',
                'è': '\u098f',
                'é': '\u099E\u09CD\u099A',
                'ê': 'থ্',
                'ë': 'চ',
                'ì': 'নি',
                'í': 'ম',
                'î': '.',
                'ï': ' ',

                # 0xf0
                'ð': 'ঝ',
                'ñ': 'ন',
                'ò': 'শী',
                'ó': 'নু',
                'ô': 'ন',
                'õ': 'ল',
                'ö': 'ব',
                '÷': 'য',
                'ø': 'লী',
                'ù': 'শ',
                'ú': 'চ্',
                'û': 'ষ্',
                'ü': 'স্',
                'ý': 'স্ত',
                'þ': 'স্',
                'ÿ': 'স্ত',

                # Other
                '\u0160': '\u0999\u09CD\u0997',
                '\u0161': '\u099C\u09CD\u099E',
                '\u0178': '\u0993\u09CD\u09a0',
                '\u2018': '\u2018',
                '\u2019': '\u2019',
                '\u201c': '\u201c',
                '\u201d': '\u201d',
                '\u2020': '\u2020',
                '\u2122': '\u099e\09cd\u099c',
                '\u201e': '৷',
            }
        }
        self.map = None
        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())
        self.old_font_name = self.FONTS_TO_CONVERT[0]
        self.scriptIndex = 0

        self.OLD_pattern_replace_list = [
            [r'([\u09bf\u09c7\u09c8])([\u0995 -\u09b9])', sub21],
        ]
        self.pattern_replace_list = [
            [r'(\u09a1\u09bc)', '\u09dc'],
            [r'(\u09a2\u09bc)', '\u09dd'],
            [r'(\u09af\u09bc)', '\u09df'],
            [r'(\u09bc\u09bc)', '\u09bc'],  # Doubled!

            [r'(\u098b\u09c3)', '\u09e0'],

            [r'([\u0981])(\u09be)', sub21],
            [r'\u0985\u09be', '\u0986'],

            # Hack - remove duplicate virama
            [r'\u09cd\u09cd', '\u09cd'],

            # Bare virama before some cases. Insert ZWSP
            [r'\u09cd([\u09ab\u0964])', subzwsp],

            # 0xea and reversing - include following diacritic
            [r'([\u0993-\u09b9][\u09be\09c0-09cc]?)(\u09cd[\u09a3-\u09af])?(\u09b0\u09cd)', sub312],

            # 0xea
            [r'(\u09ae\u09cd)(\u09e9)', '\u09ae\u09cd\u09ad'],

            # vowel sign I moves over consonant
            [r'([\u09bf\u09c7\u09c8])([\u0985-\u09b9\u09dc-\u09e1\u09f0\u09f1])', sub21],

            # next, vowel sign I moves over two conjuncts and following
            [r'([\u09bf\u09c7\u09c8])(\u09cd)([\u0993-\u09b9\u09e6-\u09f1])(\u09cd)([\u0993-\u09b9\u09e6-\u09f1])',
                sub23451],

            # next, vowel sign I moves over conjunct and following
            [r'([\u09bf\u09c7\u09c8])(\u09cd)([\u0993-\u09b9\u09e6-\u09f1])', sub231],

            # Reorder combiners
            [r'u09bf\u09bc', '\u09bc\u09bf'],  # Doubled?

            [r'([\u0995-\u09b9\u09dc-\u09df\u09f0\09f1])\u09A5\u09CD', subf0cd_1],

            [r'([\u09bf\u09c7])(\u09cd\u09a4)', sub21],
            # Specific to a3 df
            [r'\u09a4\u09cd\u09a4\u09cd\u09a4', '\u0995\u09cd\u09a4'],
            # For a2 df
            [r'\u09a4\u09cd\u09f0(\u09c7?)\u09cd\u09a4', sub95cdf9_1],
            # Specific to ec e8
            [r'\u09a8\u09cd\u098f', '\u09ae\u09cd\u09b0'],
            # fe, e7
            [r'\u09B8\u09CD\u0993', '\u09b8\u09cd\u09a4\u09c1'],
            # fe, e8
            [r'\u09B8\u09CD\u098f', '\u09b8\u09cd\u09a4\u09cd\u09b0'],
            # ec e7
            [r'\u09a8\u09CD\u0993', '\u09a8\u09cd\u09a4\u09c1'],
            # ec e8
            [r'\u09ae\u09CD([\u09b0\u09f0])', suba8cd84cd_1],

            # A3 D8 - move 9bf over, too
            [r'\u09A4\u09CD\u09A4(\u09bf)?\u09C1', sub95cda41],
            # A9 AE special case
            [r'\u09A6\u09CD\u09f0\u09b0\u09cd', '\u09b0\u09CD\u09A6\u09cd\u09f0'],

            # Remove virama after U sign
            [r'([\u09c1])\u09cd', '\u09c1'],

            # ??? Move killer over 9c7 & 9c8
            [r'(\u09cd)([\u09c7\u09c8])', sub21],
    ]

    def tokenizeText(self, textIn):
        return [i for i in textIn]

    def convert(self, text, font_name):
        # Work to do here
        # !!! TEMPORARY
        output = self.convertString(text, None, self.private_use_map[font_name])
        unconverted = self.not_converted
        return output, unconverted
