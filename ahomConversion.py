# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Ahom encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import re
import sys

from converterBase import ConverterBase

# Script index

FONTS_TO_CONVERT = [
  'Ahom', 'Ahom Manuscript'
]

thisDefaultOutputFont = 'Noto Serif Ahom'


def sub321(m):
    return m.group(3) + m.group(2) + m.group(1)

def sub21(m):
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
            # 'w': '\U00011701',
            'x': '\U00011701',
            'y': '\U0001170A',
            'z': '\U00011731',

            'A': '\U00011712',
            'B': '\U00011718',
            'D': '\U00011714',
            'G': '\U00011717',
            'H': '\U0001173F',
            'I': '\U00011723',
            'J': '\U00011719',
            'M': '\U0001172A',
            # Medials
            'R': '\U0001171D',
            'S': '\U0001171E',
            'U': '\U00011725',
            
            # Punctuation
            ',': '\U0001173C',
            '.': '\U0001173D',
            ';': '\U00011720',
            '[': '\U00011702',
            ']': '\U00011727',
            '/': '\U0001173D',

            # Specified by hex values.
            '\u0020': ' ',
            
            '\u0022': '\"',
            '\u0023': '\u1046',
            '\u0024': '\U00011739',
            '\u0025': '\U00011736',
            '\u0026': '&',
            '\u0027': '\'',
            '\u0028': '(',
            '\u0029': ')',
            '\u002a': '*',
            '\u002b': '+',
            '\u002c': ',',
            '\u002e': '\U0001173C',

            '\u0030': '\U00011720',
            '\u0031': '\U00011721',
            '\u0032': '\U00011722',
            '\u0033': '\U00011723',
            '\u0034': '\U00011724',
            '\u0035': '\U00011725',
            '\u0036': '\U00011726',
            '\u0037': '\U00011727',
            '\u0038': '\U00011728',
            '\u0039': '\U00011729',
            '\u003a': ':',
            '\u003b': '\U00011720',
            '\u003c': '\u003c',
            '\u003d': '\u003d',
            '\u003e': '\u003e',
            '\u003f': '?',

            '\u0040': '\U0001173e',
            '\u0041': '\U00011712',
            '\u0042': '\U00011718',
            '\u0044': '\U00011714',
            '\u0045': '\U00011722',
            '\u0046': 'F',
            '\u0047': '\U00011717',
            '\u0048': 'H',
            '\u0049': '\U00011723',
            '\u004a': '\U00011719',
            '\u004b': '\U00011729',
            '\u004d': '\U0001172A',
            '\u004e': '\U00011710',
            '\u004f': '\U0001172a',

            '\u0051': '\U0001172b',
            '\u0052': '\U0001171e',
            '\u0053': 'S',
            '\u0055': '\U00011725',
            '\u0057': '\U00011729',
            '\u0059': '\U0001171d',
            '\u005b': '\U00011702',
            '\u005c': '\\',
            '\u005d': '\U00011727',

            '\u0060': '\U0001173c',
            '\u0061': '\U00011721',
            '\u0062': '\U00011708',
            '\u0063': '\U0001170b',
            '\u0064': '\U00011713',
            '\u0067': '\U00011715',

            '\u0077': '\U0001171f',
            '\u0077': '\U00011730',
            '\u007b': '{',
            '\u007c': '|',
            '\u007d': '}',
            '\u007e': '~',

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
            'a': '\U00011712',
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
            # 'w': '\U00011701',
            'x': '\U00011701',
            'y': '\U0001170A',
            'z': '\U00011731',

            'A': '',
            'B': '',
            'D': '',
            'G': '',
            'H': '',
            'I': '',
            'J': '',
            'M': '',
            # Medials
            'R': '',
            'S': '',
            'U':  '\U00011725',
            
            # Punctuation
            ',': '\U0001173C',
            '.': '\U0001173D',
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
            '\u002c': ',',
            '\u002e': '\U0001173c',

            '\u0030': '\U00011730',
            '\u0031': '\U00011731',
            '\u0032': '\U00011732',
            '\u0033': '\U00011733',
            '\u0034': '\U00011734',
            '\u0035': '\U00011735',
            '\u0036': '\U00011736',
            '\u0037': '\U00011737',
            '\u0038': '\U00011738',
            '\u0039': '\U00011739',
            '\u003a': '\U00011734',
            '\u003b': '\U00011720',
            '\u003c': '\U00011701',
            '\u003d': '\u003d',
            '\u003e': '\U00011728',
            '\u003f': '\U00011707\U0001171f',

            '\u0040': '\U0001173e',
            '\u0041': '\U00011712',
            '\u0042': '\U00011718',
            '\u0044': '\U00011714',
            '\u0045': '\U00011724',
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
            '\u0055': '\U00011725',
            '\u0057': '\U00011728',
            '\u0059': '\U0001171d',
            '\u005b': '\U00011702',
            '\u005c': '\\',
            '\u005d': '\U00011727',

            '\u0060': '\U0001173c',
            '\u0061': '\U00011721',
            '\u0062': '\U00011708',
            '\u0063': '\U0001170b',
            '\u0064': '\U00011713',
            '\u0067': '\U00011716',

            '\u0077': '\U0001171f',
            '\u0077': '\U0001172b',
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
    };

    # For splitting
    latn_regex = re.compile(
        r'(a|b)')

    def __init__(self, oldFontList=FONTS_TO_CONVERT, newFont=None,
              defaultOutputFont=thisDefaultOutputFont):

        self.handle_sentences = False
        self.encoding = 0  # Default
        self.encodingScripts = FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        self.oldFonts = []
        self.font_resize_factors = [1.0, 1.3]

        for item in oldFontList:
            if isinstance(item, list):
                self.oldFonts.append(item[0])
                self.encodingScripts.append(item[1])
            else:
                self.oldFonts.append(item)

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

        self.defaultOutputFont = "Noto Serif Ahom"

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

        # Information on language detection
        self.detectLang = False
        self.ignoreLangs = []  # Language codes for not conversion
        print('AHOM CONVERTER CREATED')

    # TODO: check input and conversion tables for Unicode NFC normalization.

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        # Vowel sign to right of consonants:

        # TODO: use this list of patterns and replacements in a loop
        pattern_replace_list = [
            [r'([\U0001171e[\U00011726])(\[U0001171d\U0001171f])([\U00011700-\U0001171a\U00011731])',
             sub321],
            [r'([\U0001171e\U00011726])([\U00011700-\U0001171a\U00011731])', sub21],
            [r'(\U00011728)([U00011727\U00011729])', sub21],
            [r'(\U00011726)([\U0001171d-\U0001171f])', sub21],
            [r'(\U00011724)([\U00011722\U00011729\U0001172b\U0001172a])', sub21],
            [r'(\U00011728)([\U0001172a])', sub21],
            # Diacritics after space - invert order
            [r'(\u0020)(\U0001172b)', sub21],
            # Double full stop \U0001173c to \U0001173d
            [r'\U0001173c\U0001173c', sub3dfor2c2c]
        ]

        ePattern = r'([\U0001171e\U00011726])(\[U0001171d\U0001171f])([\U00011700-\U0001171a\U00011731])'
        newText = re.sub(ePattern, sub321, in_text)

        ePattern = r'([\U0001171e\U00011726])([\U00011700-\U0001171a\U00011731])'
        newText = re.sub(ePattern, sub21, newText)

        ePattern = r'(\U00011728)([U00011727\U00011729])'
        newText = re.sub(ePattern, sub21, newText)

        # Move e-Vowel to right of medials
        ePattern = r'(\U00011726)([\U0001171d-\U0001171f])'
        newText = re.sub(ePattern, sub21, newText)

        ePattern = r'(\U00011724)([\U00011722\U00011729\U0001172b\U0001172a])'
        newText = re.sub(ePattern, sub21, newText)

        ePattern = r'(\U00011728)([\U0001172a])'
        newText = re.sub(ePattern, sub21, newText)

        # Diacritics after space - invert order
        ePattern = r'(\u0020)(\U0001172b)'
        newText = re.sub(ePattern, sub21, newText)

        # Double full stop \U0001173c to \U0001173d
        ePattern = r'\U0001173c\U0001173c'
        newText = re.sub(ePattern, sub3dfor2c2c, newText)

        return newText
        
    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Split input into tokens for script conversion
    def tokenizeText(self, textIn):
        # Split input into tokens for script conversion
        # ASCII and whitespace characters
        if self.scriptIndex == 0:
            return [i for i in re.split('([\w\s\[\]])', textIn) if i]
        elif self.scriptIndex == 4:
            return textIn

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, textIn, fontTextInfo=None, fontIndex=0):
        self.encoding = self.encodingScripts[fontIndex]
        # print('fontIndex %s, encoding = %s' % (fontIndex, self.encoding))
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
            result = self.convertString(textIn, None, encoding_map)
            if self.debug:
                print('   convertText result= %s' % (result))
            return self.reorderText(result)

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
          print('$$$$$ text = %s, fontInfo = %s' %
                (textIn, fontInfo))  #fontInfo))
        for c in tokens:
          # Special handling if needed
          out = c
          if c in conversion_map:
            out = conversion_map[c]
          else:
            if self.debug:
              print('----- input %s not found' %
                    (c))

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

    def mapRunsToParagraphTextPosisions(self, runs):
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
            if run.font.name in FONTS_TO_CONVERT:
                font_index = FONTS_TO_CONVERT.index(run.font.name)
                run.text = self.convertText(run.text, None, font_index)
                run.font.name = self.unicodeFont
                new_font_size = int(run.font.size * self.font_resize_factors[font_index])
                run.font.size = new_font_size

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


   
def keyLen(x):
    return len(x)

def convertAhomToLatin(converter, text):
    return

def roundTripALA(converter):
    # Get Latin text
    
    ahom = converter.convertText(latin2, fontIndex=LATIN2ADLAM)
    # get Adlam text
    latin2 = converter.convertText(adlam, fontIndex=LATIN2ADLAM)
    # convert to Latin
    ahom = converter.convertText(latin2, fontIndex=ADLAT2LATIN)
    # convert back to Ahom
    # convert to Latin2
    # compare them
    return

def main(argv):
    converter = AhomConverter()
    testAhomStrings()



if __name__ == '__main__':
  main(sys.argv)
