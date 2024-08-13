# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Tai Phake encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import re
import sys

from docx import Document
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.text.hyperlink import Hyperlink
from docx.table import Table
from docx.oxml.ns import qn

from converterBase import ConverterBase

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

# For moving e-vowel, and dropping unreordered flag


def fix_e_consonant(m):
    return m.group(3) + m.group(2)

# For moving e-vowel, and dropping unreordered flag


def fix_e_r_consonant(m):
    return m.group(5) + m.group(4) + m.group(2)


def sub3dfor2c2c(m):
    return '\U0001173d'


def remdup(m):
    return m.group(1)

# Very special case to fix typo with duplicated 'uM'


def remdup_u_m(m):
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


def vs_replacer(matchobj):
    return matchobj.group(0) + VARIANT_SELECTOR

# Character constants for conversion


class PhakeConverter(ConverterBase):
    private_use_map = {
        'Phake Script': {
            "...": '\u2026',
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
            "@": "\ua9f2",
            "(": "(",
            ")": ")",
            "\u002f": "။",
            "\\": "၊",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "ၜ",
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
            ".": ".",
            "\t": "\t"
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
            "@": "\ua9f2",
            "(": "(",
            ")": ")",
            "\u002f": "။",
            "\\": "၊",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "ၜ",
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
            "\t": "\t"
        },
        'Aiton Script': {
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
            "\\": "\u103a\u105e",
            "[": "\u200c\u103c",
            "|": "\u1039\u101c",
            "]": "\u200c\u103c",
            "{": "\u200c\u103c",
            "}": "\u105c",
            "~": "\u1039\u101a",
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
            "`":  "\u1039ꩡ",
            "~": "\u1039\u101a",
            ".": ".",
            " ": " ",
            "\t": "\t"
        },
        'Banchob': {
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

    def __init__(self, oldFontList=None, newFont=None,
                 defaultOutputFont='Phake Ramayana Unicode'):

        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())

        self.thisDefaultOutputFont = defaultOutputFont

        # These characters take variation sequence modifiers
        self.variation_sequence_code_points = re.compile(
            '([\u1000\u1002\u1004\u1010\u1011\u1015\u1019\u101a\u101c\u101d\u1022\u1031\u1075\u1078\u1080\uaa60-\uaa66\uaa6b\uaa6c\uaa6f\uaa7a])')

        self.add_variant_selectors = True
        self.handle_sentences = False

        # Special flag for including ZW
        self.encoding = 0  # Default
        self.encodingScripts = self.FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        if oldFontList:
            self.oldFonts = self.FONTS_TO_CONVERT
        else:
            self.oldFonts = oldFontList

        # For Phake Script to Phake Ramayana
        self.font_resize_factor = 0.8

        self.token_splitter = None

        # Default script = 'Latn'
        self.scriptToConvert = 'Phake Script'
        self.scriptIndex = 0

        if newFont:
            self.unicodeFont = newFont
        else:
            self.unicodeFont = defaultOutputFont

        self.set_complex_font = True

        self.setScriptRange(0x1000, 0x106f)
        self.setUpperCaseRange(0x1000, 0x106f)
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

        self.end_of_sentence_pattern = re.compile(r'([\.\?!⸮؟$])')

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

            # Move e-vowel right over other vowels
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
            [r'(\u102f\u102f)(\u1036\u1036)', remdup_u_m],

            # Special case to handle II$ and III
            [r'(\u102e)(\u102e)(\u102e)', fix_triples],

            # Handle duplicates
            [r'(\u103b)(\u103b)', remdup],
            [r'(\u103c)(\u103c)', remdup],
            [r'(\u105e)(\u105e)', remdup],
        ]

        # How to replace this doubled form. It appear to be font-specific.
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
        # e.g, vowel sign to right of consonants,.
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
    def tokenizeText(self, text_in):
        # ASCII and whitespace characters
        if self.scriptIndex == 0:
            return [i for i in re.split(r'([\w\s\.])', text_in) if i]
        elif self.scriptIndex == 4:
            return text_in

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, text_in, fontTextInfo=None,
                    font_index=0, inputFont=None):
        self.encoding = self.encodingScripts[font_index]
        # print('fontIndex %s, encoding = %s' % (font_index, self.encoding))
        encoding_index = font_index
        encoding_map = {}

        if inputFont:
            try:
                font_index = self.FONTS_TO_CONVERT.index(inputFont)
            except BaseException:
                # Font not found. Return the text
                return text_in
        else:
            inputFont = self.FONTS_TO_CONVERT[font_index]

        if font_index < len(self.FONTS_TO_CONVERT):
            self.encoding = inputFont
            # Compute the encoding map for the encoding font
            encoding_map = self.private_use_map[inputFont]
            self.token_splitter = re.compile('(\w)')
        else:
            # UnknownConversion - just return unchanged text
            encoding_map = None
            self.token_splitter = None
            return text_in

        if not fontTextInfo:
            # Only raw text, without formatting or structure information.
            result = self.convertString(text_in, None, encoding_map)

            result = self.reorderText(result)
            if self.add_variant_selectors:
                result = self.add_variation_modifiers(result)
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
        if self.add_variant_selectors:
            result = self.add_variation_modifiers(result)

        return result

    # Handles details of converting the text, including case conversion.
    def convert_string(self, text_in, font_info,
                       conversion_map):
        # type: (object, object, object) -> object
        converted_list = []
        convert_result = ''

        tokens = self.tokenizeText(text_in)
        if not tokens:
            # print('????? WHY NO TOKENS in %s' % text_in)
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
                    #for i in range(len(c)):
                    #    print('** Code point %s' % hex(ord(c[i])))
                    #print('Cannot convert %s in %s' % (c, self.encoding))
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
        sentence_ends.append((len(text)-1, '$'))
        return sentence_ends, sentence_starts

    def map_runs_to_paragraph_text_posisions(self, runs):
        # Mapping of run starts & ends to text positions
        run_map = []
        pos = 0
        run_index = 0
        for run in runs:
            if run.text:
                run_map.append((pos, pos + len(run.text) - 1, run, run_index))
                pos += len(run.text)
            run_index += 1
        return run_map

    def processParagraphRuns(self, p):
        # Handle the text within each paragraph
        if not p.text:
            # Nothing to process
            return

        # Check on the language of the paragraph. May not convert.
        if self.detectLang:
            detected = self.detectLang.classify(p.text.strip())
            # print('%s in %s' % (detected, p.text))
            if detected[0] in self.ignoreLangs:
                return
            
        for run in p.runs:
            try:
                scriptIndex = self.FONTS_TO_CONVERT.index(run.font.name)

                run.text = self.convertText(run.text, None, scriptIndex)
                run.font.name = self.unicodeFont

                # Suggested by https://stackoverflow.com/questions/78829461/python-docx-change-name-of-font-in-wcs-converting-font-encoding-to-unicode
                run.element.rPr.rFonts.set(qn('w:cs'), self.unicodeFont)
                run.element.rPr.rFonts.set(qn('w:eastAsia'), self.unicodeFont)
                try:
                    new_font_size = int(run.font.size * self.font_resize_factor)
                    run.font.size = new_font_size
                except TypeError:
                    pass
            except ValueError:
                continue

        # Check on the font for the full paragraph
        try:
            self.FONTS_TO_CONVERT.index(p.style.font.name)
            p.style.font.complex_script = self.set_complex_font
            p.style.font.name = self.unicodeFont
        except ValueError:
            return

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
        run_map = self.mapRunsToParagraphTextPosisions(p.runs)

        startRuns = []
        rIndex = 0
        for sIndex in range(0, len(sentence_starts)):
            startPos = sentence_starts[sIndex]
            if rIndex >= len(run_map):
                x = 10
            while rIndex < len(run_map) and run_map[rIndex][1] < startPos:
                rIndex += 1
                if rIndex >= len(run_map):
                    break
            startRuns.append(rIndex)

        # Patch for capitals and punctuation at sentence starts.
        for sIndex in range(0, len(startRuns)):
            runId = startRuns[sIndex]
            if runId >= len(run_map):
                break
            run = run_map[runId][2]
            # This is the run.
            text = run.text
            offset = sentence_starts[sIndex] - run_map[runId][0]  # Where the text actually starts
            capped = text[offset:].capitalize()  # Capitalized portion
            firstPart = text[0:offset] # Before the capitalized section
            # Check for end character to prepend
            charEnd = sentence_ends[sIndex][1]
            if charEnd in self.pre_punctuation:
               newStart = self.pre_punctuation[charEnd]
            else:
                newStart = ''
            # Put text back in run
            try:
                run.text = firstPart + newStart + capped
            except:
                run.text = '*BROKEN* *Broken*'
        return

  # Given a start position in the paragraph text, return run and place there.
    def textPositionInRun(self, run_map, start):
        # TODO: Ignore some characters at start, e.g., digits, space, punctuation
        for map in run_map:
             if start >= map[0] and start <= map[1]:
                return (map[2], start - map[0])
        return (None, None)

    # Frequency processing for a paragraph's text
    def updateWordsFrequencies(self, para):
        pText = para.text
        words = self.wordSplitRegEx.split(pText)
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
        msgToSend = '%d paragraphs in %s\n' % (count, fileName)
        countSent = 0

    except BaseException as err:
        return 'Bad Phake converter. Err = %s' % err

    try:
        docConverter = ConvertDocx(converter, documentIn=doc,
                                   reportProgressFn=progressFn)

        if docConverter:
            result = docConverter.processDocx()
    except BaseException as err:
        return 'Error in docConverter. Err = %s' % err


def testPhakeStrings():
    t = ["cJwq AJwq",
         'vukqvWmgqmigqAaepaetecawoaeya',
         'ttqtikqmj',
         'hJwqcJgqhJgq',
         'xigqsigqRfa',
         'muthjwganEcugq',
         'cgqhnqetayW',
         ]
    expected = ['ꩡ︀ိုဝ︀် ဢ︀ိုဝ︀်',
                'ထ︀ုက︀်ထ︀ွ်မ︀င︀်မ︀ိင︀်ဢ︀ႃပ︀ေ︀ႃတ︀ေ︀ꩡ︀ေ︀ႃဝ︀ွႃယ︀ေ︀ႃ',
                'တ︀တ︀်တ︀ိက︀်မ︀ႝ',
                'ꩭိုဝ︀်ꩡ︀ိုင︀်ꩭိုင︀်',
                'ၵ︀ိင︀်ꩬ︀ိင︀်ၸ︀ြႃ',
                'မ︀ုတ︀ꩭႝဝ︀င︀ႃꩫ︀ၞ်ꩡ︀ုင︀်',
                'ꩡ︀င︀်ꩭꩫ︀်တ︀ေ︀ႃယ︀ွ်'
                ]

    converter = PhakeConverter()
    index = 0
    for text in t:
        result = converter.convertText(text, font_index=0)
                
        # print("%s --> %s" % (text, result))
        if expected[index] != result:
            print('!!! Expected %s but got %s' % (expected[index], result))
        index += 1

    return
   
def keyLen(x):
    return len(x)


def main(argv):
    converter = PhakeConverter()
    testPhakeStrings()



if __name__ == '__main__':
  main(sys.argv)
