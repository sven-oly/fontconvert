# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Ahom encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import logging
import re
import sys

from converterBase import ConverterBase

# Script index

thisDefaultOutputFont = 'Noto Serif Ahom'


def sub321(m):
    return m.group(3) + m.group(2) + m.group(1)


def sub21(m):
    return m.group(2) + m.group(1)

def sub21_with_space(m):
    return ' ' + m.group(2) + m.group(1)

def sub21_test(m):
    t1 = hex(ord(m.group(1)))
    t2 = hex(ord(m.group(2)))
    return m.group(2) + m.group(1)


def sub3dfor2c2c(m):
    return '\U0001173d'

# Character constants for conversion

class AhomConverter(ConverterBase):

    private_use_map = {
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

    # TODO: Change this from PHK to AHO rules
    dictionary_to_font = {
        'lx': ['Lexeme', 'Ahom'],
        'le': ['Lexeme Alternative Spelling', 'Ahom'],
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
        # TEMPORARY? 'dn': ['Definition Assamese', 'Assamese'],
        'dn': ['Definition Ahom', 'Ahom'],  # ???
        'dr': ['Romanization'],  # ???
        'rf': ['Reference [For example sentences taken from texts]'],
        'se': ['Example free translation English', 'Ahom'],
        'xv': ['Example Phake', 'Phake Script'],
        'xr': ['Example Phonetic', 'Banchob'],
        'xe': ['Example free translation English', 'Ahom'],
        'xn': ['Example free translation Assamese', 'Assamese'],
        'notes': ['Notes'],
    }

    # For splitting
    latn_regex = re.compile(
        r'(a|b)')

    def __init__(self, old_font_list=None, newFont=None,
                 defaultOutputFont=thisDefaultOutputFont):

        # self.FONTS_TO_CONVERT = [
        #     'Ahom', 'Ahom Manuscript'
        # ]
        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())

        self.thisDefaultOutputFont = 'Noto Serif Ahom'

        self.handle_sentences = False
        self.encoding = 0  # Default
        if old_font_list:
            self.encodingScripts = old_font_list
        else:
            self.encodingScripts = self.FONTS_TO_CONVERT

        self.oldFonts = self.encodingScripts

        self.font_resize_factors = [1.0, 1.3]

        # Default script = 'arab'
        self.scriptToConvert = 'Ahom'
        self.scriptIndex = 0

        if newFont:
            self.unicodeFont = newFont
        else:
            self.unicodeFont = defaultOutputFont
        self.setScriptRange(0x11700, 0x1173f)
        self.setUpperCaseRange(0x11700, 0x1174f)
        self.description = 'Converts Ahom font encoding to Unicode'

        self.defaultOutputFont = defaultOutputFont

        self.forceFont = True  # May be used to set all font fields to the Unicode font

        self.isRtl = False

        self.description = 'Converts Ahom font encoding to Unicode'
        self.ignore_start_of_sentence = re.compile(
            r'([\U00011700-\U0001173f])')

        self.encoding = None
        self.debug = False

        self.setLowerMode(True)
        self.setSentenceMode(True)

        self.end_of_sentence_pattern = re.compile(r'([\.\?\!\⸮\؟$])')

        # For inserting question and exclamation before sentences.
        self.pre_punctuation = {
        }

        # How words are split in Ahom text - split on non-Ahom text
        self.wordSplitRegEx = re.compile(r'\W+')

        self.collectConvertedWordFrequency = True
        self.convertedWordFrequency = {}

        self.not_converted = []

        self.pattern_replace_list = [

            [re.compile(r'([\U0001171e\U00011726])(\[U0001171d-\U0001171f])([\U00011700-\U0001171a\U00011731])'),
             sub321],
            [re.compile(r'([\U0001171e\U00011726])([\U00011700-\U0001171a\U00011731])'), sub21],
            [re.compile(r'(\U00011728)([\U0001171d-\U0001171f\U00011722-\U00011724\U00011726-\U0001172b])'), sub21],
            [re.compile(r'([\U00011722\U00011723\U00011729])([\U0001171d-\U0001171f\U00011726])'), sub21],
            [re.compile(r'(\U00011726)([\U0001171d-\U0001171f])'), sub21],
            [re.compile(r'([\U00011724\U00011725])([\U0001171d-\U0001171f\U00011722-\U00011723\U00011726-\U00011727\U00011729-\U0001172b])'), sub21],
            [re.compile(r'([\U00011720\U00011721])([\U0001171d-\U0001171f\U00011722-\U0001172b])'), sub21],
            # Apply this one again.
            [re.compile(r'(\U00011728)([\U0001171d-\U0001171f\U00011722-\U00011724\U00011726-\U0001172b])'), sub21],
            # Diacritics after space - invert order
            [re.compile(r'(\u0020)([\U0001171d-\U0001172b])'), sub21],
            # Double full stop \U0001173c to \U0001173d
            [re.compile(r'\U0001173c\U0001173c'), sub3dfor2c2c]
        ]

        # These are orders of combining marks that are not allowed.
        self.bad_diacritic_order = [
            re.compile(r'[\U0001171d\U00011726][\U0001171d-\U0001171f]'),
            re.compile(r'[\U0001171f][\U0001171e-\U0001171f]'),
            re.compile(r'\U0001171e[\U0001171ef]'),
            re.compile(r'[\U00011720\U00011721][\U0001171d-\U0001171f\U00011722-\U0001172b]'),
            re.compile(r'[\U00011722\U00011723][\U0001171d-\U0001171f\U00011726]'),
            re.compile(r'[\U00011724\U00011725][\U0001171d-\U0001171f\U00011722-\U00011723\U00011726-\U00011727\U00011729-\U0001172b]'),
            re.compile(r'[\U00011727\U00011729-\U0001172b][\U0001171d-\U0001171f\U00011726]'),
            re.compile(r'\U00011728[\U0001171d-\U0001171f\U00011722-\U00011723\U00011726-\U00011727\U00011729-\U0001172b]'),
        ]
        # Special case processing
        self.match_last_a = re.compile(r' a$')
        self.fix_assamese = re.compile(r'\u0020([\u09bf\u09c7\u09c8])([\u0980-\u09fe])')

        # Information on language detection
        self.detectLang = False
        self.ignoreLangs = []  # Language codes for not conversion
        print('AHOM CONVERTER CREATED')

    # TODO: check input and conversion tables for Unicode NFC normalization.

    def preprocess(self, textIn, current_tag=None):
        # Preprocesing text for special cases
        if current_tag:
            # Fixing special Assamese text
            textIn =  re.sub(self.fix_assamese, sub21_with_space, textIn)
        else:
            # Text for Ahom - special case
            textIn = self.match_last_a.sub('\u0020\U0001173c', textIn)
        return textIn

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        new_text = in_text
        for pair in self.pattern_replace_list:
            new_text = re.sub(pair[0], pair[1], new_text)
        return new_text

    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Split input into tokens for script conversion
    def tokenizeText(self, textIn):
        # Split input into tokens for script conversion
        # ASCII and whitespace characters
        if self.scriptIndex == 0:
           return [i for i in textIn]
          #  return [i for i in re.split('([\<\;\>\w\s\[\]])', textIn) if i]
        elif self.scriptIndex == 4:
            return textIn

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, textIn, fontTextInfo=None, fontIndex=-1, inputFont=None, line_count=-1):
        self.encoding = self.encodingScripts[fontIndex]
        # print('fontIndex %s, encoding = %s' % (fontIndex, self.encoding))
        if inputFont and fontIndex == -1:
            try:
                encoding_index = self.FONTS_TO_CONVERT.index(inputFont)
                fontIndex = encoding_index
            except ValueError:
                # We don't handle that font
                return None
        else:
            encoding_index = fontIndex
        encoding_map = {}
        if fontIndex < 2:
            # Compute the encoding map for the encoding fong
            encoding_map = self.private_use_map[self.encoding]
            self.token_splitter = self.latn_regex
        else:
            # UnknownConversion
            convertData = None
            encoding_map = None
            self.token_splitter = None

        if not fontTextInfo:
            # Only raw text, without formatting or structure information.

            if self.debug:
                print('****** TEXT = %s' % textIn)
            # Special preprocessing
            textIn = self.preprocess(textIn, None)

            result = self.convertString(textIn, None, encoding_map)
            if self.debug:
                print('   convertText result= %s' % (result))

            final_result = self.reorderText(result)
            was_bad = self.check_for_incorrect_diacritic_oder(final_result)
            if was_bad:
                logging.error('  Problem line is # %d: >\\%s%s<', line_count, self.current_tag, textIn)
                logging.error('    Converted = >%s<', final_result)
            return final_result

        # Take the data from the fontTextInfo field.
        convertList = []
        for item in fontTextInfo:
            tags = []
            for fmt in item[1]:
                loc = fmt.tag.find('}')
                tags.append(fmt.tag[loc + 1:])

            convertList.append(
                self.convertString(item[0], tags, encoding_map))
        if self.debug:
            print('  --> out  = %s' % ''.join(convertList))

        return self.reorderText(''.join(convertList))

    # Handles details of converting the text, including case conversion.
    def convertString(self, textIn, fontInfo,
                      conversion_map):
        # type: (object, object, object) -> object
        convertedList = []
        convertResult = ''

        tokens = self.tokenizeText(textIn)
        if not tokens and textIn:
            print('????? WHY NO TOKENS in %s' % textIn)

        if self.debug:
            print('------- Tokens %s' % tokens)

        if self.debug:
            print('$$$$$ text = %s, fontInfo = %s' % (textIn, fontInfo))  #fontInfo))
        for c in tokens:
          # Special handling if needed
          out = c
          if c in conversion_map:
            out = conversion_map[c]
          else:
              if self.debug:
                  print('----- input %s not found' % (c))

          # Special case for handling underlined text
          convertedList.append(out)

        convertResult = self.reorderText(''.join(convertedList))

        if self.lower_mode:
          convertResult = self.toLower(convertResult)

        return convertResult

    def computeSentenceStartsEnds(self, text):
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

    def mapRunsToParagraphTextPositions(self, runs):
        # Mapping of run starts & ends to text positions
        run_map = []
        pos = 0
        run_index = 0
        for run in runs:
            if run.text:
                run_length = len(run.text)
                run_map.append((pos, pos + len(run.text) - 1, run, run_index))
                pos += len(run.text)
            run_index += 1
        return run_map

    def processParagraphRuns(self, p):
        # Handle the text within each paragraph
        if not p.text:
            # Nothing to process
            return

        # Check on the language of the paragraph. May don't convert.
        if self.detectLang:
            detected = self.detectLang.classify(p.text.strip())
            # print('%s in %s' % (detected, p.text))
            if detected[0] in self.ignoreLangs:
                return

        for run in p.runs:
            if run.font.name in self.FONTS_TO_CONVERT:
                font_index = self.FONTS_TO_CONVERT.index(run.font.name)
                try:
                    run.text = self.convertText(run.text, None, font_index)

                    run.font.name = self.unicodeFont
                    new_font_size = int(run.font.size * self.font_resize_factors[font_index])
                    run.font.size = new_font_size
                except ValueError as error:
                    pass
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
            firstPart = text[0:offset]  # Before the capitalized section
            # Check for end character to prepend
            charEnd = sentence_ends[sIndex][1]
            if charEnd in self.pre_punctuation:
               newStart = self.pre_punctuation[charEnd]
            else:
                newStart = ''
            # Put text back in run
            try:
                run.text = firstPart + newStart + capped
            except E as error:
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

    def check_for_incorrect_diacritic_oder(self, text):
        index = 0
        any_bad_ones = False
        for bad_match in self.bad_diacritic_order:
            try:
                is_match = bad_match.search(text)
                if is_match:
                    logging.error("Suspect diacritic order with pattern %s on text %s",
                                  index, text)
                    any_bad_ones = True
            except BaseException as err:
                pass
            index += 1
        return any_bad_ones


# TODO: Test more Ahom text!


def convertDocx(files):
    ahommConverter = ahomConversion.ahomConverter()

    try:
        ahomConverter.setScriptIndex(scriptIndex)
        ahomConverter.setLowerMode(True)
        ahoamConverter.setSentenceMode(True)
        paragraphs = doc.paragraphs
        count = len(paragraphs)
        msgToSend = '%d paragraphs in %s\n' % (count, fileName)
        countSent = 0

    except BaseException as err:
        return 'Bad Ahom converter. Err = %s' % err

    if app.debug:
        print('Created converter')

    try:
        docConverter = ConvertDocx(ahomConverter, documentIn=doc,
                                   reportProgressFn=progressFn)

        if docConverter:
            result = docConverter.processDocx()
    except BaseException as err:
        return 'Error in docConverter. Err = %s' % err


def simpleTests(converter):
    # Run simple single character tests
    logging.info('Simple tests')

    test = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
    expected = '𑜒 𑜘 C 𑜔 𑜢𑜤 𑜰𑜧 𑜗 𑜩 𑜣 𑜙 𑜕 L 𑜪 𑜐 O P𑜫  𑜝 𑜞 T 𑜥 V 𑜩𑜨 X 𑜝 Z'
    actual = converter.convertText(test)
    if actual != expected:
        logging.error('Failed:\n  expected %s\n  actual  %s', expected, actual)

    test = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
    expected = '𑜡 𑜈 𑜋 𑜓 𑜦 𑜇 𑜖 𑜑 𑜢 𑜩 𑜀 𑜎 𑜉 𑜃 𑜨 𑜆𑜫  𑜍 𑜏 𑜄 𑜤 𑜌 𑜰𑜫 𑜁 𑜊 z'
    actual = converter.convertText(test)
    if actual != expected:
        logging.error('Failed:\n  expected %s\n  actual  %s', expected, actual)

    test = '1 2 3 4 5 6 7 8 9 0'
    expected ='𑜱 𑜲 𑜳 𑜴 𑜵 𑜶 𑜷 𑜸 𑜹 𑜰'
    actual = converter.convertText(test)
    if actual != expected:
        logging.error('Failed:\n  expected %s\n  actual  %s', expected, actual)

    test = '` ~ ! @ # $ % ^ & * ( ) _ - + = [ { ] } \ | ; : \' \" , < . > / ?'
    expected = '𑜼 ~ ! 𑜾 𑜙 𑜹 𑜶 ^ & * ( ) _ - + = 𑜂 { 𑜧 } \ | 𑜠 𑜺 \' \" , 𑜁𑜟 𑜼 𑜨𑜡 𑜽 𑜐𑜟'
    actual = converter.convertText(test)
    if actual != expected:
        logging.error('Failed:\n  expected %s\n  actual  %s', expected, actual)


def main(argv):
    converter = AhomConverter()
    testAhomStrings(converter)

    simpleTests(converter)


if __name__ == '__main__':
    main(sys.argv)
