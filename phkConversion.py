# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Tai Phake encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import logging
import re
import sys

from docx.oxml.ns import qn
from docx.oxml.shared import OxmlElement, qn

from docx.shared import Pt

from converterBase import ConverterBase

from check_complex_script import fix_cs_formatting_run

VARIANT_SELECTOR = '\uFE00'

# This font as an output does not use 0x00A0 to connect doubled vowels
FONT_WITHOUT_NBSP = 'Phake Ramayana Unicode'


# Reverse characters
def sub321(m):
    return m.group(3) + m.group(2) + m.group(1)


# Swap order of two items
def sub21(m):
    return m.group(2) + m.group(1)


# Swap order of ra and consonant


def sub_ra(m):
    return m.group(3) + m.group(2)


# For moving e-vowel, and dropping un-reordered flag
def sub9cc(m):
    # When 9c7 is just before 9cc, change the second to 9d7
    return '\u09c7' + m.group(2)


def fix_e_consonant(m):
    return m.group(3) + m.group(2)


# For moving e-vowel, and dropping un-reordered flag
def fix_e_r_consonant(m):
    return m.group(5) + m.group(4) + m.group(2)


def sub3dfor2c2c(m):
    return '\U0001173d'


def remove_dup(m):
    return m.group(1)


def insert200d(m):
    return m.group(1) + '\u200d' + m.group(2)


def insert200b(m):
    return m.group(1) + '\u200b' + m.group(2)


def remove_break(m):
    return m.group(1)


# Very special case to fix typo with duplicated 'uM'
def remove_dup_u_m(m):
    return '\u102f\u1036'


def fix_triples(m):
    return m.group(1) + m.group(2)


def connect_double_vowels(m):
    return m.group(1) + '\u00a0' + m.group(1)


def convert_double_sat(m):
    c = m.group(1)
    # replace with U+103a + myanmar modifier letter khamti reduplication
    return c + '\uaa70'
    # Or replace with myanmar modifier letter khamti reduplication
    # return '\uaa70'
    # Or add a non-breaking space between the two characters
    # return m.group(1) + '\u00a0' + m.group(1)
    # Or something else ???


# Remove a space between two vowels.
def remove_space_between(m):
    return m.group(1) + m.group(2)


# Remove a space before some vowel signs.
def remove_space_before(m):
    return m.group(1)


def vs_replacer(match_obj):
    return match_obj.group(0) + VARIANT_SELECTOR


# Character constants for conversion


def insert_break_fn(match_obj):
    new_text = '\u200b' + match_obj.group(0)
    return new_text


class PhakeConverter(ConverterBase):
    private_use_map = {
        'Phake Script': {
            ':': '\u1038',  # ???
            '½': '\u104b',  # ???
            '=': '=',
            '\u2018': '\u2018', # ???
            "\u2026": '\u2026',
            ',': ',',
            '.': '.',
            '!': '!',  # ???
            "A": "ဢ",
            "B": "ꩰ",
            "C": "\u108a",
            "D": "ꩰ",
            "E": "\u105e\u103a",
            "F": "\u103a\u1036",
            "G": "\u1087",
            "H": "\u1088",
            "I": "\u102e",
            "J": "ို",
            "K": "\u1039\u1000",
            "L": "\u1038",
            "M": "ံ",
            "N": "\u107a",
            "O": "\u1089",
            "P": "\u1039\u1015",
            "Q": "\uaa77",
            "R": "\u200c\u103c",
            "S": "꩷",
            "T": "\u1039\u1010",
            "U": "\u1030",
            "V": "\ua9f2",
            "W": "ွ်",
            "X": "ႜ",
            "Y": "ျ",
            "Z": "ၞ",
            "a": "ႃ",
            "b": "ပ",
            "c": "ꩡ",
            "d": "ဒ",
            "e": "\u200c\u1031",  # signal for non-reordered
            "f": "ၸ",
            "g": "င",
            "h": "\uaa6d",
            "i": "ိ",
            "j": "\u109d",
            "k": "က",
            "l": "လ",
            "m": "မ",
            "n": "ꩫ",
            "o": "ွ",
            "p": "ပ",
            "q": "\u103a",  # ?? u103a
            "r": "\uAA7A",
            "s": "\uaa6c",
            "t": "တ",
            "u": "ု",
            "v": "ထ",
            "w": "ဝ",
            "x": "ၵ",
            "y": "ယ",
            "z": "\uAA78",
            "@": "\ua9f2",
            "(": "(",
            ")": ")",
            "\u002f": "။",
            "\\": "၊",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "\u200c\u103c",
            "}": "\u103a\u103d",
            "~": "",
            "1": "၁",
            "2": "၂",
            "3": "၃",
            "4": "၄",
            "5": "၅",
            "6": "၆",
            "7": "၇",
            "8": "၈",
            "9": "၉",
            "0": "၀",
            "#": "\u1036",
            "$": "ီ",
            "^": "\u102c",
            "_": "\u103a\u105e",
            "%": "\u00a0\u103a",
            "&": "\u00a0\u109d",
            "`": "`",
            " ": " ",
            "\t": "\t",
        },
        'Phake Ramayana': {
            "\t": '\t',
            "...": '\u2026',
            "A": "ဢ",
            "B": "ꩰ",
            "C": ":",
            "D": "ꩰ",
            "E": "\u105e\u103a",
            "F": "\u103a\u1036",
            "G": "\u1087",
            "H": "\u1088",
            "I": "ီ",
            "J": "ို",
            "K": "\u1039\u1000",
            "L": "\u1038",
            "M": "ံ",
            "N": "\u107a",
            "O": "\u1089",
            "P": "\u1039\u1015",
            "Q": "\uaa77",
            "R": "\u200c\u103c",
            "S": "꩷",
            "T": "\u1039\u1010",
            "U": "\u1030",
            "V": "\ua9f2",
            "W": "ွ်",
            "X": "ႜ",
            "Y": "ျ",
            "Z": "ၞ",
            "a": "ႃ",
            "b": "ပ",
            "c": "ꩡ",
            "d": "ဒ",
            "e": "\u200c\u1031",  # signal for non-reordered
            "f": "ၸ",
            "g": "င",
            "h": "\uaa6d",
            "i": "ိ",
            "j": "\u109d",
            "k": "က",
            "l": "လ",
            "m": "မ",
            "n": "ꩫ",
            "o": "ွ",
            "p": "ပ",
            "q": "\u103a",
            "r": "\uAA7A",
            "s": "\uaa6c",
            "t": "တ",
            "u": "ု",
            "v": "ထ",
            "w": "ဝ",
            "x": "ၵ",
            "y": "ယ",
            "z": "\uAA78",
            "@": "\ua9f2",
            "(": "(",
            ")": ")",
            "\u002f": "။",
            "\\": "၊",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "\u200c\u103c",
            "}": "\u103a\u103d",
            "~": "",
            "1": "၁",
            "2": "၂",
            "3": "၃",
            "4": "၄",
            "5": "၅",
            "6": "၆",
            "7": "၇",
            "8": "၈",
            "9": "၉",
            "0": "၀",
            "#": "\u1036",
            "$": "ီ",
            "^": "\u102c",
            "_": "\u103a\u105e",
            "%": "\u00a0\u103a",
            "&": "&",
            "`": "`",
            " ": " ",
            ".": ".",
            "…": "…"
        },
        'Aiton Script': {
            '\u00a0': '\u00a0',
            ',': ',',
            "A": "ဢ",
            "B": "ꩰ",
            "C": "\u108a",
            "D": "ꩰ",
            "E": "\u105e\u103a",
            "F": "\u103a\u1036",
            "G": "\u1087",
            "H": "\u1088",
            "I": "ီ",
            "J": "ို",
            "K": "\u1039\u1000",
            "L": "\u1038",
            "M": "ံ",
            "N": "\u107a",
            "O": "\u103d",
            "P": "\u1039\u1015",
            "Q": "\uaa77",
            "R": "\u200c\u103c",
            "S": "꩷",
            "T": "\u1039\u1010",
            'U': "\u1030",
            "V": "\u1030",  # ???
            "W": "ွ်",
            "X": "ႜ",
            "Y": "ျ",
            "Z": "ၞ",
            "a": "ႃ",
            "b": "ပ",
            "c": "ꩡ",
            "d": "ဒ",
            "e": "\u200c\u1031",  # signal for non-reordered
            "f": "ၸ",
            "g": "င",
            "h": "\uaa6d",
            "i": "ိ",
            "j": "\u109d",
            "k": "က",
            "l": "လ",
            "m": "မ",
            "n": "ꩫ",
            "o": "ွ",
            "p": "ပ",
            "q": "်",
            "r": "\uAA7A",
            "s": "\uaa6c",
            "t": "တ",
            "u": "ု",
            "v": "ထ",
            "w": "ဝ",
            "x": "ၵ",
            "y": "ယ",
            "z": "\uAA78",
            "@": "\u1092",
            "(": "(",
            ")": ")",
            "/": "\u104b",
            "\\": "\u104a",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "\u200c\u103c",
            "}": "\u105c",
            "~": "\u1039\u101a",
            "_": "꩹",
            "1": "၁",
            "2": "၂",
            "3": "၃",
            "4": "၄",
            "5": "၅",
            "6": "၆",
            "7": "၇",
            "8": "၈",
            "9": "၉",
            "0": "၀",
            "%": "\u00a0\u103a",
            "&": "\u00a0\u109d",
            "`": "\u1039ꩡ",
            ".": ".",
            " ": " ",
            "\t": "\t",
            "…": "…",
            '¥': '¥',

        },
        'Banchob': {
            ' ': ' ',
            'N': 'ŋ',
            'M': 'ñ',
            'j': 'ɛ',
            'v': 'ü',
            'z': 'ə',
            'q': 'ɔ',
            'I': 'ī',
            'E': 'ē',
            'J': 'ɛ̄',
            'V': 'ǖ',
            'Z': 'ə̄',
            'A': 'ā',
            'U': 'ū',
            'O': 'ō',
            'Q': 'ɔ̄',
            '1': '¹',
            '2': '²',
            '3': '³',
            '4': '⁴',
            '5': '⁵',
            '6': '⁶',
            '7': '⁷',
            '8': '⁸',
            '9': '⁹',
            "…": "…"
        },
        'Assam New': {
            #'»¶': '»¶',  # ???
            '\t': '\t',
            #'»¶': '»¶',  # ???
            #'¡¶': '¡¶',  # ???
            #'¥': '¥',    # ???
            ' ': ' ',
            '¶': '\u09aa',  ## Update
            "¡": 'ক',
            "¢": 'খ',
            "¤": 'গ',
            "¦": 'ঘ',
            "§": 'ঙ',
            "¨": 'চ',
            "©": 'ছ',
            "ª": 'জ',
            "¬": 'ঝ',
            "\u00ad": 'ঞ',  # Soft hyphen
            '¯': 'ট',
            '°': 'ঠ',
            '±': 'ড',
            '²': 'ঢ',
            '³': 'ণ',
            '´': 'ৎ',
            'µ': 'ত',
            '·': 'দ',
            '¸': 'ধ',
            '¹': 'ন',
            '»': 'প',
            '¼': 'ফ',
            '¾': 'ব',
            'A': '\u2019',
            'À': 'ভ',
            'Á': 'ম',
            'Â': 'য',
            'Ã': 'ৰ',
            'Å': 'ল',
            'Ç': 'ৱ',
            'Æ': 'র',
            'È': 'শ',
            'É': 'ষ',
            'Ê': 'স',
            'Ë': 'হ',
            '×': 'ং',
            'Ð': 'ঃ',
            'í': 'ঁ',
            'Ä': 'ড়',
            'Ì': 'ঢ়',
            '¿': 'য়',
            'Í': 'অ',
            'ÍÒ': 'আ',
            'b': 'ই',
            'u': 'ঈ',
            '6': 'উ',
            '^': 'ঊ',
            '7': 'ঋ',
            'g': 'এ',
            'c': 'ঐ',
            'F': 'ও',
            'w': 'ঔ',
            'Ò': 'া',
            'Ô': 'ি',
            'å': 'ি',
            'Õ': 'ী',
            'Ø': 'ু',
            'Ù': 'ূ',
            'Ö': 'ৃ',
            'à': 'ে',
            'á': 'ৈ',
            'ä': 'ৗ',
            'ì': '\u09cd',
            'p': '\u09cd\u09af',
            'x': '\u09aa',
            'V': '\u0995\u09cd\u09b7',
            "…": "…",
            ",": ',',
            '(': '(',
            ')': ')',
            '/': '/',
            '#': '/#',
            '\"': '\"',
        },
        # Include Ahom texts, too.
        'Ahom': {
            'a': '\U00011721',
            'b': '\U00011708',
            'c': '\U0001170B',
            'd': '\U00011713',
            'e': '\U00011726',
            'f': '\U00011707',
            'g': '\U00011715',
            'h': '\U00011711',
            'i': '\U00011722',
            'j': '\U00011729',
            'k': '\U00011700',
            'l': '\U0001170E',
            'm': '\U00011709',
            'n': '\U00011703',
            'o': '\U00011728',
            'p': '\U00011706',
            'q': '\U0001172B',
            'r': '\U0001170D',
            's': '\U0001170F',
            't': '\U00011704',
            'u': '\U00011724',
            'v': '\U0001170C',
            'w': '\U00011730\U0001172B',
            'x': '\U00011701',
            'y': '\U0001170A',
            'z': '\U00011731',

            '@': '\U0001173e',
            'A': '\U00011712',
            'B': '\U00011718',
            'D': '\U00011714',
            'E': '\U00011722\U00011724',
            'F': 'F',
            'G': '\U00011717',
            'H': '\U00011729',
            'I': '\U00011723',
            'J': '\U00011719',
            'K': '\U00011715',
            'M': '\U0001172A',
            'N': '\U00011710',
            'O': '\U0001172a',
            'P': 'P',
            'Q': '\U0001172b',

            # Medials
            'R': '\U0001171D',
            'S': '\U0001171E',
            'U': '\U00011725',
            'W': '\U00011729',
            'Y': '\U0001171d',

            # Punctuation
            ',': ',',
            '.': '\U0001173D',
            ';': '\U00011720',
            '[': '\U00011702',
            ']': '\U00011727',
            '/': '\U0001173D',

            '\u0020': ' ',

            '\"': '\"',
            '#': '\u1046',
            '$': '\U00011739',
            '%': '\U00011736',
            '&': '&',
            '\'': '\'',
            '(': '(',
            ')': ')',
            '*': '*',
            '+': '+',

            '0': '\U00011730',
            '1': '\U00011731',
            '2': '\U00011732',
            '3': '\U00011733',
            '4': '\U00011734',
            '5': '\U00011735',
            '6': '\U00011736',
            '7': '\U00011737',
            '8': '\U00011738',
            '9': '\U00011739',
            ':': ':',
            '<': '\U00011701\U0001171F',
            '=': '\u003d',
            '>': '\U00011724\U00011728',
            '?': '\U00011707\U0001171F',

            '\\': '\\',

            '{': '{',
            '|': '|',
            '}': '}',
            '~': '~',

            '\u00a1': '\U00011700',
            '\u00a2': '\U00011701',
            '\u00a4': '\U00011715',
            '\u00a5': '\U00011729',
            '\u00a6': '\U00011717',
            '\u00a7': '\U00011702',
            '\u00a8': '\U0001170b',
            '\u00ac': '\U00011719',

            '\u00b4': '\U00011713',
            '\u00b5': '\U00011704',
            '\u00b6': '\U0001170c',
            '\u00b7': '·',
            '\u00b8': '\U00011714',
            '\u00b9': '\U00011703',
            '\u00ba': '\U00011708',
            '\u00bb': '\U00011706',
            '\u00bc': '\U00011707',
            '\u00bd': '\u00bd',
            '\u00be': '\u00be',
            '\u00bf': '\U0001171d',

            '\u00c0': '\U00011718',
            '\u00c1': '\U00011709',
            '\u00c2': '\U0001170e',
            '\u00c3': '\U0001170d',
            '\u00c4': '\U0001171e',
            '\u00c5': '\U0001170e',
            '\u00c6': 'Æ',
            '\u00c7': '\U00011730',
            '\u00c8': '\U0001172a',
            '\u00ca': '\U0001170f',
            '\u00cb': '\U00011711',
            '\u00cd': '\U00011712',
            '\u00ce': '\U0001172b',

            '\u00d0': '\U00011720',
            '\u00d2': '\U00011721',
            '\u00d4': '\U00011722',
            '\u00d5': '\U00011723',
            '\u00d6': '\U00011729',
            '\u00d7': '\U00011722',
            '\u00d8': '\U00011724',
            '\u00d9': '\U00011725',

            '\u00e0': '\U00011726',
            '\u00e1': '\U0001172b',
            '\u00e2': '\U00011728',
            '\u00e3': '\U00011727',
            '\u00e4': '\U00011729',

            '\u00f1': '\U00011731',

            '\u0112': '.',
            '\u0160': '\u030c',
            '\u0161': '\U0001170f',
            '\u02c6': '\u030c',
            '\u02c7': '\u0302',
            '\u2022': '\u2022',
            '\u2122': '\u2122',
        },
        'Ahom Manuscript': {
            'a': '\U00011721',
            'b': '\U00011708',
            'c': '\U0001170B',
            'd': '\U00011713',
            'e': '\U00011726',
            'f': '\U00011707',
            'g': '\U00011716',
            'h': '\U00011711',
            'i': '\U00011722',
            'j': '\U00011729',
            'k': '\U00011700',
            'l': '\U0001170E',
            'm': '\U00011709',
            'n': '\U00011703',
            'o': '\U00011728',
            'p': '\U00011706',
            'q': '\U0001172B',
            'r': '\U0001170D',
            's': '\U0001170F',
            't': '\U00011704',
            'u': '\U00011724',
            'v': '\U0001170C',
            'w': '\U00011730\u0001172B',
            'x': '\U00011701',
            'y': '\U0001170A',
            'z': '\U00011731',

            # Punctuation
            ',': ',',
            '.': '\U0001173C',
            ';': '\U00011720',
            '[': '\U00011702',
            ']': '\U00011727',
            '/': '\U0001173D',

            # Specified by hex values.
            '\u0020': ' ',
            '\u0021': '!',
            '\u0022': '\"',
            '\u0023': '\U00011719',
            '\u0024': '\U00011739',
            '\u0025': '\U00011736',
            '\u0026': '&',
            '\u0027': '\'',
            '\u0028': '(',
            '\u0029': ')',
            '\u002a': '*',
            '\u002b': '+',

            '0': '\U00011730',
            '1': '\U00011731',
            '2': '\U00011732',
            '3': '\U00011733',
            '4': '\U00011734',
            '5': '\U00011735',
            '6': '\U00011736',
            '7': '\U00011737',
            '8': '\U00011738',
            '9': '\U00011739',

            ':': '\U00011734',
            '<': '\U00011701\U0001171F',
            '=': '\u003d',
            '>': '\U00011724\U00011728',
            '?': '\U00011707\U0001171f',

            '\u0040': '\U0001173e',
            'A': '\U00011712',
            '\u0042': '\U00011718',
            '\u0044': '\U00011714',
            'E': '\U00011722\U00011724',
            '\u0046': '\U00011730',
            '\u0047': '\U00011717',
            '\u0048': '\U00011729',
            '\u0049': '\U00011723',
            '\u004a': '\U00011719',
            '\u004b': '\U00011715',
            '\u004d': '\U0001172a',
            '\u004e': '\U00011710',
            '\u004f': '\u004f',

            '\u0051': '\U0001172b',
            '\u0052': '\U0001171d',
            '\u0053': '\U0001171e',
            'U': '\U00011725',
            'W': '\U00011728',
            'Y': '\U0001171d',
            '\\': '\\',

            '`': '\U0001173c',

            '\u007b': '{',
            '\u007c': '|',
            '\u007d': '}',
            '\u007e': '~',

            '\u00a1': '\U00011705\U0001170a',
            '\u00a2': '\U00011701',
            '\u00a4': '¤',
            '\u00a5': '\U00011729',
            '\u00a6': '\U00011717',
            '\u00a7': '\U00011702',
            '\u00a8': '\U0001170b',
            '\u00ac': '\U00011719',

            '\u00b4': '\U00011713',
            '\u00b5': '\U00011704',
            '\u00b6': '\U0001170c',
            '\u00b7': '\U0001170c\U00011727',
            '\u00b8': '\U00011714',
            '\u00b9': '\U00011703',
            '\u00ba': '\U00011708',
            '\u00bb': '\U00011706',
            '\u00bc': '\U00011707',
            '\u00bd': '\U00011712',
            '\u00be': '\U0001171f',
            '\u00bf': '\U0001171d',

            '\u00c0': '\U00011718',
            '\u00c1': '\U00011709',
            '\u00c2': '\U0001170e',
            '\u00c3': '\U0001170d',
            '\u00c4': '\U0001171e',
            '\u00c5': '\U0001170e',
            '\u00c6': '\U0001170e',
            '\u00c7': '\U00011708\U0001171f',
            '\u00c8': '\U0001172a',
            '\u00ca': '\U0001170f',
            '\u00cb': '\U00011711',
            '\u00cd': '\U00011712',
            '\u00ce': '\U0001172b',

            '\u00d0': '\U00011720',
            '\u00d2': '\U00011721',
            '\u00d4': '\U00011722',
            '\u00d5': '\U00011723',
            '\u00d6': '\U00011729\U00011728',
            '\u00d7': '\U00011722\U00011724',
            '\u00d8': '\U00011724',
            '\u00d9': '\U00011725',

            '\u00e0': '\U00011726',
            '\u00e1': '\U0001172b',
            '\u00e2': '\U00011728',
            '\u00e3': '\U00011727',
            '\u00e4': '\U00011729',

            '\u00f1': '\U00011731',

            '\u0112': '.',
            '\u0160': '\u030c',
            '\u0161': '\U0001170f\u030c',
            '\u02c6': '\u030c',
            '\u02c7': '\u0302',
            '\u2022': '\u2022',
            '\u2122': '\U0001171e'
        }
    }

    dictionary_to_font = {
        'lx': ['Lexeme', 'Phake Script'],
        'le': ['Lexeme Alternative Spelling', 'Phake Script'],
        'ph': ['Phonetic form', 'Banchob'],
        'so': ['Source (listing of sound file link)'],
        'hm': ['Homonym number'],
        'ps': ['Part of speech'],
        'sn': ['Sense number'],
        'de': ['Definition (English)'],
        'ge': ['Gloss (English)'],
        'pc1': ['(Picture 1)'],
        'pc2': ['Picture 2'],
        'pl': ['Couplet form', 'Phake Script'],

        'pd': ['Couplet form phonetic', 'Banchob'],
        'pde': ['Couplet form English'],
        'pdn': ['Couple form Assamese', 'Assamese'],
        'dn': ['Definition Assamese', 'Assamese'],
        'rf': ['Reference [For example sentences taken from texts]'],
        'xv': ['Example Phake', 'Phake Script'],
        'xr': ['Example Phonetic', 'Banchob'],
        'xe': ['Example free translation English'],
        'xn': ['Example free translation Assamese', 'Assamese'],
        'notes': ['Notes'],
        'se': ['Subentry', 'Phake Script'],
    }

    # For splitting by ASCII characters
    # re.ASCII

    def __init__(self, old_font_list=None, new_font=None,
        default_output_font='Phake Ramayana Unicode'):
        self.font_index = None
        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())

        super().__init__(self.FONTS_TO_CONVERT, new_font, default_output_font)  # Call the parent class's __init__
        self.thisDefaultOutputFont = default_output_font
        self.defaultOutputFont = default_output_font
        self.defaultFontSize = Pt(12)
        self.grapheme_boundary_char = '\u200b'
        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())
        self.ONE_POINT_FACTOR = 12700  # for each "point" of the font size
        self.current_table = None
        self.add_grapheme_boundary_char = True
        self.old_font_name = self.FONTS_TO_CONVERT[0]
        self.reset_font_size = True

        self.grapheme_boundary_char = '\u200b'
        self.add_grapheme_boundary_char = True

        # Initialize splitting by regex based on each script's keys
        self.split_by_script = {}
        for font in self.FONTS_TO_CONVERT:
            font_keys = sorted(
                self.private_use_map[font].keys(), key=len, reverse=True)

        self.thisDefaultOutputFont = default_output_font

        # These characters take variation sequence modifiers
        self.variation_sequence_code_points = re.compile(
            '([\u1000\u1002\u1004\u1010\u1011\u1015\u1019\u101a\u101c\u101d\u1022\u1031\u1075\u1078\u1080\uaa60'
            '-\uaa66\uaa6b\uaa6c\uaa6f\uaa7a])')

        # Matches characters that can have a break \u200b before
        self.break_before_old = re.compile(
            '[^\u102b-\u1035\u1040-\u104b\u1056-\u1059\u1062-\u106d\u1072-\u1074\u1082-\u108d\u1090-\u1099\u109a'
            '-\u109d\uaa7b-\uaa7d]')
        self.insert_break_char = '\u200b'
        self.break_before = re.compile('([\u1000-\u102a\u1075-\u1081\u1087-\u108a\uaa61-\uaa6d])')

        self.add_variant_selectors = True
        self.handle_sentences = False

        # Special flag for including ZW
        self.encoding = 0  # Default
        self.encodingScripts = self.FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        if not old_font_list:
            self.oldFonts = self.FONTS_TO_CONVERT
        else:
            self.oldFonts = old_font_list

        # For Phake Script to Phake Ramayana Unicode
        self.font_resize_factor = 0.8

        self.token_splitter = None

        # Default script = 'Latn'
        self.scriptToConvert = 'Phake Script'
        self.scriptIndex = 0

        self.font_substitution = {
            'Phake Script': 'PhakeRamayanaUnicode',
            'Phake Ramayana': 'PhakeRamayanaUnicode',
            'Aiton Script': 'Noto Sans Myanmar', # 'PhakeRamayanaUnicode',
            'Assam New': 'Noto Serif Bengali',
            'Ahom': 'Noto Serif Ahom',
            'Ahom Manuscript': 'Noto Serif Ahom',
        }
        self.OUTPUT_FONTS = ['PhakeRamayanaUnicode', 'Noto Serif Bengali', 'Noto Serif Ahom']

        if new_font:
            self.unicodeFont = new_font
        else:
            self.unicodeFont = default_output_font

        self.set_complex_font = True

        self.set_script_range(0x1000, 0x106f)
        self.set_upper_case_range(0x1000, 0x106f)
        self.description = 'Converts Phake font encoding to Unicode'

        self.forceFont = True  # May be used to set all font fields to the Unicode font

        self.isRtl = False

        self.description = 'Converts Phake font encoding to Unicode'
        self.ignore_start_of_sentence = re.compile(
            r'([\U00011700-\U0001173f])')

        self.encoding = None
        self.debug = False

        self.setLowerMode(True)
        self.setSentenceMode(True)

        self.end_of_sentence_pattern = re.compile(r'([.?!⸮؟$])')

        # For inserting question and exclamation before sentences.
        self.pre_punctuation = {
        }

        # How words are split in Phake text - split on non-Phake text
        self.wordSplitRegEx = re.compile(r'(\W+)')

        self.collectConvertedWordFrequency = True
        self.convertedWordFrequency = {}

        # Information on language detection
        self.detectLang = False
        self.ignoreLangs = []  # Language codes for not conversion

        self.not_converted = {}  # Array of unconverted characters / strings and scripts with counts

        # TODO: Put in more conversions as needed.
        # TODO? compile these patterns
        self.pattern_replace_list = [
            # Space between o, u, Y and u - remove.
            [r'([\u102f\u103b\u103d])\u0020([\u102f\u103d])', remove_space_between],

            # Remove a space before some consonants
            [r'\u0020([\u109c])', remove_space_before],

            # e and R before a consonant
            [r'(\u200c)(\u1031)(\u200c)(\u103c)([\u1000-\u1029\u1075-\u1081\uaa60-\uaa7a])',
             fix_e_r_consonant],
            # Migrate e-vowel over consonant
            [r'(\u200c)(\u1031)([\u1000-\u1029\u1075-\u1081\uaa60-\uaa7a])',
             fix_e_consonant],

            # Swap R and e
            [r'(\u1031)(\u103c)', sub21],

            # Move e-vowel right to after other vowels
            [r'(\u1031)([\u103D\u103b\u103c\u103A\u105E]+)',
             sub21],

            # Flip medial wa and medial ya
            [r'(\u103d)(\u103b)', sub21],

            # Move UU after asat and medials
            [r'(\u1030)([\u103a-\u103d]+)', sub21],

            # Move Ra after Asat
            [r'(\u103c)([\u103a\u103b]+)', sub21],

            # Move ra over consonant
            [r'(\u200c)(\u103c)([\u1000-\u1029\u1075-\u1081\uaa60-\uaa7a])',
             sub_ra],

            # Move vowel reordering
            [r'(\u1036)(\u102F)', sub21],
            [r'([\u102d\u102e])([\u103a\u103b\u103c\u103d\u105e])', sub21],
            [r'([\u102f\u1030\u1036])([\u103a\u103b\u103c\u103d\u105e\u109d\ua935])', sub21],
            [r'([\u103b\u103c\u103d])(\u105e)', sub21],

            # Remove duplicate of uMuM
            [r'(\u102f\u102f)(\u1036\u1036)', remove_dup_u_m],

            # Special case to handle II$ and III
            [r'(\u102e)(\u102e)(\u102e)', fix_triples],

            # Handle duplicates
            [r'(\u103b)(\u103b)', remove_dup],
            [r'(\u103c)(\u103c)', remove_dup],
            [r'(\u105e)(\u105e)', remove_dup],

            # Assamese reordering
            [r'([\u09bf\u09c7-\u09cc])([\u0985-\u09b9\u09dc-\u09fd])', sub21],

            # Change second one to a different character
            [r'([\u09cc])([\u0985-\u09b9\u09dc-\u09fd])', sub9cc],
            [r'([\u09cc])([\u09cc])', remove_dup],

            # Reorder
            [r'([\u0981])([\u09be])', sub21],
            [r'([1038])([\u109d])', sub21],

            [r'(\u200b)([1038])', remove_break],

            # Insert between
            [r'([\u09cd])([\u09be])', insert200d],
            [r'([\u0985])([\u09be])', insert200d],
            [r'([\u0997])([\u09c1])', insert200d],
            [r'([\u09cd])([\u09a1-\u09a5\u0997\u09b2])', insert200b],
        ]

        # How to replace this doubled form. It appears to be font-specific.
        self.pattern_replace_list.append([r'(\u103a)(\u103a)', convert_double_sat])

        if self.thisDefaultOutputFont != FONT_WITHOUT_NBSP:
            # These are used with Noto and Padauk fonts, but
            # Not Ramayana
            self.pattern_replace_list.extend(
                [
                    [r'(\u102e)(\u102e)', connect_double_vowels],
                    [r'(\u1036)(\u1036)', connect_double_vowels],
                    [r'(\u109d)(\u109d)', connect_double_vowels]
                ])

    # TODO: check input and conversion tables for Unicode NFC normalization.

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        # e.g, vowel sign to right of consonants.
        new_text = in_text
        for pair in self.pattern_replace_list:
            new_text = re.sub(pair[0], pair[1], new_text)
        return new_text

    def add_variation_modifiers(self, text):
        out_text = re.sub(self.variation_sequence_code_points, vs_replacer, text)
        return out_text

    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Split input into tokens for script conversion
    # def tokenizeText(self, text_in):
    #     # ASCII and whitespace characters
    #     if self.scriptIndex == 0:
    #         return [i for i in re.split(r'([\w\s.])', text_in) if i]
    #     elif self.scriptIndex == 4:
    #         return text_in

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, text_in, fontTextInfo=None,
                    font_index=0, input_font=None):
        # For passing these values along as needed
        # self.encoding = self.encodingScripts[font_index]
        self.font_index = font_index

        if input_font:
            try:
                font_index = self.FONTS_TO_CONVERT.index(input_font)
            except BaseException:
                # Font not found. Return the text
                return text_in
        else:
            input_font = self.FONTS_TO_CONVERT[font_index]

        if font_index < len(self.FONTS_TO_CONVERT):
            self.encoding = input_font
            # Compute the encoding map for the encoding font
            encoding_map = self.private_use_map[input_font]
            self.token_splitter = re.compile(r'(\s)')
        else:
            # UnknownConversion - just return unchanged text
            self.token_splitter = None
            return text_in

        if not fontTextInfo:
            # Only raw text, without formatting or structure information.
            if self.remove_returns_in_block:
                text_in = text_in.replace('\n', '')
                # TODO: remove later
                logging.info('Removing return in block: %s', text_in)

            result = self.convertString(text_in, input_font, encoding_map)

            # result = self.reorderText(result)
            if self.add_variant_selectors:
                result = self.add_variation_modifiers(result)

            if self.add_grapheme_boundary_char:
                result = self.insert_grapheme_boundaries(result)
            return result

        # Take the data from the fontTextInfo field.
        convert_list = []
        for item in fontTextInfo:
            tags = []
            for fmt in item[1]:
                loc = fmt.tag.find('}')
                tags.append(fmt.tag[loc + 1:])

            convert_list.append(
                self.convertString(item[0], tags, encoding_map))

        result = self.reorderText(''.join(convert_list))
        # Post-processing of the converted text
        if self.add_variant_selectors:
            result = self.add_variation_modifiers(result)

        if self.add_grapheme_boundary_char:
            result = self.insert_grapheme_boundaries(result)

        return result

    def insert_grapheme_boundaries(self, text):
        # use self.break_before to insert \u200b before
        new_text = self.break_before.sub(insert_break_fn, text)
        return new_text

    # Handles details of converting the text, including case conversion.
    def convert_string(self, text_in, font_info,
                       conversion_map):
        # type: (object, object, object) -> object
        converted_list = []

        tokens = self.tokenizeText(text_in)
        if not tokens:
            pass

        for c in tokens:
            # Special handling if needed
            out = c
            if c in conversion_map:
                out = conversion_map[c]
            else:
                key = '%s-%s' % (self.encoding, c)
                if key not in self.not_converted:
                    self.not_converted[key] = 1
                    # for i in range(len(c)):
                    #    print('** Code point %s' % hex(ord(c[i])))
                    # print('Cannot convert %s in %s' % (c, self.encoding))
                else:
                    self.not_converted[key] += 1

            # Special case for handling underlined text
            converted_list.append(out)

        convert_result = self.reorderText(''.join(converted_list))

        if self.lower_mode:
            convert_result = self.toLower(convert_result)

        return convert_result

    def compute_sentence_starts_ends(self, text):
        # Get all the positions of sentence endings
        all_sentence_ends = self.end_of_sentence_pattern.finditer(text)
        text_len = len(text)
        if not all_sentence_ends:
            # No sentence endings. Should first be capitalized?
            return None
        sentence_starts = [0]
        ignore_match = self.ignore_start_of_sentence.match(text)
        if ignore_match:
            sentence_starts[0] = ignore_match.end()
        sentence_ends = []
        for sentence_end in all_sentence_ends:
            # Position and character of this sentence ending
            sentence_ends.append((sentence_end.start(), sentence_end.group(0)[0]))
            end_pos = sentence_end.end()
            while end_pos < text_len and (
                    text[end_pos] == ' ' or text[end_pos] == '\r'
                    or text[end_pos] == '\t' or text[end_pos] == '\n'):
                end_pos += 1
            # Move the letter content
            #         self.ignore_start_of_sentence = re.compile(
            # r'([\U0001E950\U0001E959\u0020()]+)')
            start_pos = end_pos
            if start_pos < text_len:
                ignore_match = self.ignore_start_of_sentence.match(text[start_pos:])
                if ignore_match:
                    start_pos += ignore_match.end() - 1
            sentence_starts.append(start_pos)
        # The paragraph text ends a sentence
        sentence_ends.append((len(text) - 1, '$'))
        return sentence_ends, sentence_starts

    def findDefinitionEnds(self, p):
        # Get the run indices of runs that have a new line \n
        # of a paragraph
        end_indices = []
        index = 0
        for r in p.runs:
            if r.text.find('\n') >= 0:
                end_indices.append(index)
            index += 1
        # one after the last item
        end_indices.append(len(p.runs))

        return end_indices

    def processParagraphRuns(self, p):
        # Handle the text within each paragraph
        # if not p.text:
        #     # Nothing to process
        #     return


        # Check on the language of the paragraph. May not convert.

        # TODO: Fix this later?
        if False and self.detectLang:
            detected = self.detectLang.classify(p.text.strip())
            if detected[0] in self.ignoreLangs:
                return

            
        for run in p.runs:
            old_text = run.text
            if isinstance(run.font.size, list):
                pass  # This is a list!
            try:
                old_font_name = run.font.name
                if not old_font_name:
                    continue
                try:
                    script_index = self.FONTS_TO_CONVERT.index(old_font_name)
                except ValueError:
                    # Not a font to convert
                    continue

                # Save for deeper calls
                self.old_font_name = old_font_name
                self.font_index = script_index

                new_font_name = self.unicodeFont
                try:
                    new_font_name = self.font_substitution[old_font_name]
                except:
                    pass  # Use a default

                # Will this make the information for the font to work correctly?
                # Nope, not good enough.
                # https://python-docx.readthedocs.io/en/latest/_modules/docx/text/font.html
                run.font.complex_script = True

                run.text = self.convertText(old_text, None, script_index, input_font=old_font_name)
                run.font.name = new_font_name
                # TODO: Fix this
                if new_font_name:  # == 'PhakeRamayanaUnicode':
                    user_cs_font_size = 12
                    fix_cs_formatting_run(run, user_cs_font_size, new_font_name)

                try:
                    if self.reset_font_size:
                        if self.current_table:
                            # smaller in the table
                            # new_font_size = 20 * self.ONE_POINT_FACTOR
                            new_font_size = Pt(20)
                        else:
                            #
                            # new_font_size = 35 * self.ONE_POINT_FACTOR
                            new_font_size = Pt(35)
                        run.font.size = new_font_size
                        run.font.cs_size = new_font_size
                except TypeError:
                    pass
            except ValueError:
                continue

        if self.handle_sentences:
            self.processSentences(p)

        if self.collectConvertedWordFrequency:
            self.updateWordsFrequencies(p)
        return

    def processSentences(self, p):
        # Deal with questions and exclamations, inserting
        # initial marks at the start of sentences.

        # Get all the positions of sentence endings
        sentence_ends, sentence_starts = \
            self.computeSentenceStartsEnds(p.text)

        start_runs = []
        r_index = 0
        for sIndex in range(0, len(sentence_starts)):
            start_pos = sentence_starts[sIndex]

            while r_index < len(run_map) and run_map[r_index][1] < start_pos:
                r_index += 1
                if r_index >= len(run_map):
                    break
            start_runs.append(r_index)

        # Patch for capitals and punctuation at sentence starts.
        for sIndex in range(0, len(start_runs)):
            run_id = start_runs[sIndex]
            if run_id >= len(run_map):
                break
            run = run_map[run_id][2]
            # This is the run.
            text = run.text
            offset = sentence_starts[sIndex] - run_map[run_id][0]  # Where the text actually starts
            capped = text[offset:].capitalize()  # Capitalized portion
            first_part = text[0:offset]  # Before the capitalized section
            # Check for end character to prepend
            char_end = sentence_ends[sIndex][1]
            if char_end in self.pre_punctuation:
                new_start = self.pre_punctuation[char_end]
            else:
                new_start = ''
            # Put text back in run
            try:
                run.text = first_part + new_start + capped
            except:
                run.text = '*BROKEN* *Broken*'
        return

    # Given a start position in the paragraph text, return run and place there.
    def textPositionInRun(self, run_map, start):
        # TODO: Ignore some characters at start, e.g., digits, space, punctuation
        for rmap in run_map:
            if rmap[0] <= start <= rmap[1]:
                return rmap[2], start - rmap[0]
        return None, None

    # Frequency processing for a paragraph's text
    def updateWordsFrequencies(self, para):
        p_text = para.text
        words = self.wordSplitRegEx.split(p_text)
        for word in words:
            # Should ignore empty non-word items
            if word and word != ' ':
                self.addWordToFrequencyList(word)


def convertDocx(files):
    converter = PhakeConverter()

    try:
        converter.setScriptIndex(scriptIndex)
        converter.setLowerMode(True)
        converter.setSentenceMode(True)
        paragraphs = doc.paragraphs
        count = len(paragraphs)
        msg_to_send = '%d paragraphs in %s\n' % (count, fileName)

    except BaseException as err:
        return 'Bad Phake converter. Err = %s' % err

    try:
        doc_converter = ConvertDocx(converter, documentIn=doc,
                                    reportProgressFn=progressFn)

        if doc_converter:
            result = doc_converter.processDocx()
    except BaseException as err:
        return 'Error in docConverter. Err = %s' % err


def test_phake_strings(converter):
    t = ["cJwq AJwq",
         'vukqvWmgqmigqAaepaetecawoaeya',
         'ttqtikqmj',
         'hJwqcJgqhJgq',
         'xigqsigqRfa',
         'muthjwganEcugq',
         'cgqhnqetayW',
         'ko ugq',
         '[pamattq'
         ]
    expected = ['ꩡ︀ိုဝ︀် ဢ︀ိုဝ︀်',
                'ထ︀ုက︀်ထ︀ွ်မ︀င︀်မ︀ိင︀်ဢ︀ႃပ︀ေ︀ႃတ︀ေ︀ꩡ︀ေ︀ႃဝ︀ွႃယ︀ေ︀ႃ',
                'တ︀တ︀်တ︀ိက︀်မ︀ႝ',
                'ꩭိုဝ︀်ꩡ︀ိုင︀်ꩭိုင︀်',
                'ၵ︀ိင︀်ꩬ︀ိင︀်ၸ︀ြႃ',
                'မ︀ုတ︀ꩭႝဝ︀င︀ႃꩫ︀ၞ်ꩡ︀ုင︀်',
                'ꩡ︀င︀်ꩭꩫ︀်တ︀ေ︀ႃယ︀ွ်',
                'က︀ွု​ ​င︀်​',
                'ပ︀ြႃ​မ︀ႃ​တ︀​တ︀်​',

                ]

    converter.add_variant_selectors = True
    index = 0
    for text in t:
        result = converter.convertText(text, font_index=0)

        if expected[index] != result:
            print('!!! Expected %s but got %s' % (expected[index], result))
        index += 1

    return


def main(argv):
    converter = PhakeConverter()
    testPhakeStrings(converter)


if __name__ == '__main__':
    main(sys.argv)
