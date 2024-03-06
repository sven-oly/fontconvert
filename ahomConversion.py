# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Ahom encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import re
import sys

from converterBase import ConverterBase

# Script index

FONTS_TO_CONVERT = [
  ['Ahom', 'Ahom Manuscript'],
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
        'a': ['\U00011721', '\U00011712'],
        'b': ['\U00011708', '\U00011708'],
        'c': ['\U0001170B', '\U0001170B'],
        'd': ['\U00011713', '\U00011713'],
        'e': ['\U00011726', '\U00011726'],
        'f': ['\U00011707', '\U00011707'],
        'g': ['\U00011715', '\U00011715'],
        'h': ['\U00011711', '\U00011711'],
        'i': ['\U00011722', '\U00011722'],
        'j': ['\U00011729', '\U00011729'],
        'k': ['\U00011700', '\U00011700'],
        'l': ['\U0001170E', '\U0001170E'],
        'm': ['\U00011709', '\U00011709'],
        'n': ['\U00011703', '\U00011703'],
        'o': ['\U00011728', '\U00011728'],
        'p': ['\U00011706', '\U00011706'],
        'q': ['\U0001172B', '\U0001172B'],
        'r': ['\U0001170D', '\U0001170D'],
        's': ['\U0001170F', '\U0001170F'],
        't': ['\U00011704', '\U00011704'],
        'u': ['\U00011724', '\U00011724'],
        'v': ['\U0001170C', '\U0001170C'],
        # 'w': ['\U00011701', '\U00011701'],
        'x': ['\U00011701', '\U00011701'],
        'y': ['\U0001170A', '\U0001170A'],

        'A': ['\U00011712', ''],
        'B': ['\U00011718', ''],
        'D': ['\U00011714', ''],
        'G': ['\U00011717', ''],
        'H': ['\U0001173F'],
        'I': ['\U00011723', ''],
        'J': ['\U00011719', ''],
        'M': ['\U0001172A', ''],
        # Medials
        'R': ['\U0001171D', ''],
        'S': ['\U0001171E', ''],
        'U': ['\U00011725', ''],
        
        # Punctuation
        ',': ['\U0001173C'],
        '.': ['\U0001173D'],
        ';': ['\U00011720', ''],
        '[': ['\U00011702', ''],
        ']': ['\U00011727', ''],

        # Specified by hex values.
        '\u0020': [' ', ' ', ' '],  # Space
        '\u0021': ['!', '!', '\u1039\u1011'],  # !
        '\u0022': ['\"', '\"', '\"'],  # "
        '\u0023': ['\u1046', '\U00011719', '\U0001172a'],  # #
        '\u0024': ['\U00011739', '\U00011739', '\u102e'],  # $
        '\u0025': ['\U00011736', '\U00011736', '\U0001172f'],  # %
        '\u0026': ['&', '&', '\U00011729'],  # &
        '\u0027': ['\'', '\'', '\''],  # '
        '\u0028': ['(', '(', '('],  # (
        '\u0029': [')', ')', ')'],  # )
        '\u002a': ['*', '*', '*'],  # *
        '\u002b': ['+', '+', '????'],  # +
        '\u002c': [',', ',', ','],  # ,
        '\u002e': ['\U0001173C', '\U0001173c', '.'],  # .
        '\u002f': ['\u104b', '\U0001173d', '\u104b'],  # /
        
        '\u0030': ['\u1040', '\U00011730', '\u1040'],  # 0
        '\u0031': ['\u1041', '\U00011731', '\u1041'],  # 1
        '\u0032': ['\u1042', '\U00011732', '\u1042'],  # 2
        '\u0033': ['\u1043', '\U00011733', '\u1043'],  # 3
        '\u0034': ['\u1044', '\U00011734', '\u1044'],  # 4
        '\u0035': ['\u1045', '\U00011735', '\u1045'],  # 5
        '\u0036': ['\u1046', '\U00011736', '\u1046'],  # 6
        '\u0037': ['\u1047', '\U00011737', '\u1047'],  # 7
        '\u0038': ['\u1048', '\U00011738', '\u1048'],  # 8
        '\u0039': ['\u1049', '\U00011739', '\u1049'],  # 9
        '\u003a': [':', '\U0001173a', '\U00011734'],  # semicolon
        '\u003b': ['\U00011720', '\U00011720', '\U00011734'],  # semicolon
        '\u003c': ['\u003c', '\U00011701\U0001171f', '<'],  # <
        '\u003d': ['\u003d', '\u003d', '='],  # =
        '\u003e': ['\u003e', '\U00011728\U00011721', '>'],  # >
        '\u003f': ['?', '\U00011710\U0001171f', '?'],  # ?

        '\u0040': ['\U0001173e', '\U0001173e', '\uaa79'],  # @
        '\u0041': ['\U00011712', '\U00011712', '\U00011733\U00011705'],  # @
        '\u0042': ['\U00011718', '\U00011718', '\uaa70'],  # @
        '\u0044': ['\U00011714', '\U00011714', '\uaa70'],  # @
        '\u0045': ['\U00011722\U00011724', '\U00011722\U00011724', '\U00011733\U00011705'],  # E
        '\u0046': ['F', '\U00011730\U00011727', '\U00011733\U00011705'],  # @
        '\u0047': ['\U00011717', '\U00011717', '\u1087'],  # @
        '\u0048': ['H', '\U00011729', '\u1088'],  # @
        '\u0049': ['\U00011723', '\U00011723', '\u102e'],  # @
        '\u004a': ['\U00011719', '\U00011719', '\u102f'],  # @
        '\u004b': ['\U00011729', '\U00011715', '\U00011733\U00011705'],  # @
        '\u004d': ['\U0001172A', '\U0001172a', '\u1036'],  # M
        '\u004e': ['\U00011710', '\U00011710', '\U00011733\U00011705'],  # @
        '\u004f': ['\U0001172a', '\u004f', '\u1037'],  # @

        '\u0051': ['\U0001172b', '\U0001172b', '\U00011733\U00011705'],  # Q
        '\u0052': ['\U0001171e', '\U0001171d', '\U00011733\U00011705'],  # R
        '\u0053': ['S', '\U0001171e', '\U00011733\U00011705'],  # S
        '\u0055': ['\U00011725', '\U00011725', '\u1030'],  # U
        '\u0057': ['\U00011729\U00011728', '\U00011729\U00011728', '\U00011733\U00011705'],  # V
        '\u0059': ['\U0001171d', '\U0001171d', '\u103b'],  # X
        '\u005b': ['\U00011702', '\U00011702', '\U00011733\U00011705'],  # @
        '\u005c': ['\\', '\\', '\u104a'],  # @
        '\u005d': ['\U00011727', '\U00011727', '\U00011733\U00011705'],  # @

        '\u0060': ['\U0001173c', '\U0001173c', '\U00011733\U00011705'],  # @
        '\u0061': ['\U00011721', '\U00011721', '\U00011733\U00011705'],  # @
        '\u0062': ['\U00011708', '\U00011708', '\U00011733\U00011705'],  # @
        '\u0063': ['\U0001170b', '\U0001170b', '\U00011733\U00011705'],  # @
        '\u0064': ['\U00011713', '\U00011713', '\U00011733\U00011705'],  # @
        '\u0067': ['\U00011715', '\U00011716', '\U00011733\U00011705'],  # @

        '\u0077': ['\U0001171f', '\U0001171f', ''],  # w
        '\u0077': ['\U00011730\U0001172b', '\U00011730\U0001172b'],  # w
        '\u007b': ['{', '{'],  # @
        '\u007c': ['|', '|'],  # @
        '\u007d': ['}', '}'],  # @
        '\u007e': ['~', '~'],  # @

        '\u00a1': ['\U00011700', '\U00011705\U0001170a',
             '\U00011733\U00011705'],  # @
        '\u00a2': ['\U00011701', '\U00011701', '\U00011733\U00011705'],  # @
        '\u00a4': ['\U00011715', '¤', '\U00011733\U00011705'],  # @
        '\u00a5': ['\U00011729', '\U00011729', '\U00011733\U00011705'],  # @
        '\u00a6': ['\U00011717', '\U00011717', '\U00011733\U00011705'],  # @
        '\u00a7': ['\U00011702', '\U00011702', '\U00011733\U00011705'],  # @
        '\u00a8': ['\U0001170b', '\U0001170b', '\U00011733\U00011705'],  # @
        '\u00ac': ['\U00011719', '\U00011719', '\U00011733\U00011705'],  # @


        '\u00b4': ['\U00011713', '\U00011713', '\U00011733\U00011705'],  # @
        '\u00b5': ['\U00011704', '\U00011704', '\U00011733\U00011705'],  # @
        '\u00b6': ['\U0001170c', '\U0001170c', '\U00011733\U00011705'],  # @
        '\u00b7': ['·', '\U0001170c\U00011727', '\U00011733\U00011705'],  # @
        '\u00b8': ['\U00011714', '\U00011714', '\U00011733\U00011705'],  # @
        '\u00b9': ['\U00011703', '\U00011703', '\U00011733\U00011705'],  # @
        '\u00ba': ['\U00011708', '\U00011708', '\U00011733\U00011705'],  # @
        '\u00bb': ['\U00011706', '\U00011706', '\U00011733\U00011705'],  # @
        '\u00bc': ['\U00011707', '\U00011707', '\U00011733\U00011705'],  # @
        '\u00bd': ['\u00bd', '\U00011712', '\U00011733\U00011705'],  # @
        '\u00be': ['\u00be', '\U0001171f', '\U00011733\U00011705'],  # @
        '\u00bf': ['\U0001171d', '\U0001171d', '\U00011733\U00011705'],  # @

        '\u00c0': ['\U00011718', '\U00011718', '\U00011733\U00011705'],  # @
        '\u00c1': ['\U00011709', '\U00011709', '\U00011733\U00011705'],  # @
        '\u00c2': ['\U0001170e', '\U0001170e', '\U00011733\U00011705'],  # @
        '\u00c3': ['\U0001170d', '\U0001170d', '\U00011733\U00011705'],  # @
        '\u00c4': ['\U0001171e', '\U0001171e', '\U00011733\U00011705'],  # @
        '\u00c5': ['\U0001170e', '\U0001170e', '\U00011733\U00011705'],  # @
        '\u00c6': ['Æ', '\U0001170e', '\U00011733\U00011705'],  # @
        '\u00c7': ['\U00011730\U0001172b', '\U00011708\U0001171f', '\U00011733\U00011705'],  # @
        '\u00c8': ['\U0001172a', '\U0001172a', '\U00011733\U00011705'],  # @
        '\u00ca': ['\U0001170f', '\U0001170f', '\U00011733\U00011705'],  # @
        '\u00cb': ['\U00011711', '\U00011711', '\U00011733\U00011705'],  # @
        '\u00cd': ['\U00011712', '\U00011712', '\U00011733\U00011705'],  # @
        '\u00ce': ['\U0001172b', '\U0001172b', '\U00011733\U00011705'],  # @

        '\u00d0': ['\U00011720', '\U00011720', '\U00011733\U00011705'],  # @
        '\u00d2': ['\U00011721', '\U00011721', '\U00011733\U00011705'],  # @
        '\u00d4': ['\U00011722', '\U00011722', '\U00011733\U00011705'],  # @
        '\u00d5': ['\U00011723', '\U00011723', '\U00011733\U00011705'],  # @
        '\u00d6': ['\U00011729\U00011728', '\U00011729\U00011728', '\U00011733\U00011705'],  # @
        '\u00d7': ['\U00011722\U00011724', '\U00011722\U00011724', '\U00011733\U00011705'],  # @
        '\u00d8': ['\U00011724', '\U00011724', '\U00011733\U00011705'],  # @
        '\u00d9': ['\U00011725', '\U00011725', '\U00011733\U00011705'],  # @

        '\u00e0': ['\U00011726', '\U00011726', '\U00011733\U00011705'],  # @
        '\u00e1': ['\U0001172b', '\U0001172b', '\U00011733\U00011705'],  # @
        '\u00e2': ['\U00011728', '\U00011728', '\U00011733\U00011705'],  # @
        '\u00e3': ['\U00011727', '\U00011727', '\U00011733\U00011705'],  # @
        '\u00e4': ['\U00011729', '\U00011729', '\U00011733\U00011705'],  # @

        '\u00f1': ['\U00011731', '\U00011731', '\U00011733\U00011705'],  # @
        
        '\u0112': ['.', '.', '\U00011733\U00011705'],  # @
        '\u0160': ['\u030c', '\u030c', '\U00011733\U00011705'],  # @
        '\u0161': ['\U0001170f\u030c', '\U0001170f\u030c', '\U00011733\U00011705'],  # @
        '\u02c6': ['\u030c', '\u030c', '\U00011733\U00011705'],  # @
        '\u02c7': ['\u0302', '\u0302', '\U00011733\U00011705'],  # @
        '\u2022': ['\u2022', '\u2022', '\U00011733\U00011705'],  # @
        '\u2122': ['\u2122', '\U0001171e', '\U00011733\U00011705'],  # @
    }

    # For splitting
    latn_regex = re.compile(
        r'(a|b)')
 
 
    def __init__(self, oldFontList=FONTS_TO_CONVERT, newFont=None,
              defaultOutputFont=thisDefaultOutputFont):

        print('AHOM CONVERTER CREATED')
        self.encoding = 0  # Default
        self.encodingScripts = FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        self.oldFonts = []

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

        self.isRtl = True

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
        self.wordSplitRegEx = re.compile(r'\W')

        self.collectConvertedWordFrequency = True
        self.convertedWordFrequency = {}

        # Information on language detection
        self.detectLang = False
        self.ignoreLangs = []  # Language codes for not conversion

    # TODO: check input and conversion tables for Unicode NFC normalization.

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        # Vowel sign to right of consonants:

        # TODO: use up list of patterns and replacements.
        pattern_replace_list = [
            [r'([\U0001171e[\U00011726])(\[U0001171d\U0001171f])([\U000117-\U000117a])',
             sub321],
            [r'([\U0001171e\U00011726])([\U00011700-\U0001171a])', sub21],
            [r'(\U00011728)([U00011727\U00011729])', sub21],
        ]

        ePattern = r'([\U0001171e\U00011726])(\[U0001171d\U0001171f])([\U00011700-\U0001171a])'
        newText = re.sub(ePattern, sub321, in_text)

        ePattern = r'([\U0001171e\U00011726])([\U00011700-\U0001171a])'
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
        if self.scriptIndex == 0:
            # Split into Arabic characters
            return [*textIn]
        elif self.scriptIndex == 3:
            # Latin - break into tokens using a regular expression
            # Remove empty strings
            return [i for i in self.token_splitter.split(textIn) if i]
        elif self.scriptIndex == 4:
            return [i for i in self.token_splitter.split(textIn) if i]

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
            # encoding_map = self.private_use_map[self.encoding]
            for v in self.private_use_map.keys():
                encoding_map[v] = self.private_use_map[v][encoding_index]
            self.token_splitter = self.latn_regex
        else:
            # UnknownConversion from 
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
        if not tokens:
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
            run.text = self.convertText(run.text, None, self.scriptIndex)
            run.font.name = self.unicodeFont

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
def testConvert():
  # Debug!
  testcases = {
    'latn': {
        'fontIndex': 3,  # For latin
        'toLower': False,
        'sentenceCase': True,
        'tests': [
          ['KAALDEN GOONGA : “Maa laaɓ, ñamlel ko joɓel!',
           "𞥞 𞤑𞤀𞥄𞤂𞤁𞤉𞤐 𞤘𞤌𞥅𞤐'𞤘𞤀 : “𞤃𞤢𞥄 𞤤𞤢𞥄𞤩⹁ 𞤻𞤢𞤥𞤤𞤫𞤤 𞤳𞤮 𞤶𞤮𞤩𞤫𞤤!"
           ],
        ],
    },
    'arab': {
        'fontIndex': 0,
        'toLower': True,
        'sentenceCase': True,
        'tests': [
            ['بثب!', '𞥞𞤀𞤤𞤢!'],
            ['بثب?', '𞥟𞤀𞤤𞤢?'],
            ["قظكتضكتضك يبكڄضك ض پ‍بث‍‌ب سنث‍بص",
             '𞤏𞤭𞤲𞤣𞤫𞤲𞤣𞤫𞤲 𞤶𞤢𞤲𞤺𞤫𞤲 𞤫 𞤸𞤢𞤤𞤢 𞤨𞤵𞤤𞤢𞤪'
            ],
            [ 'لنجسظڇبث لنجسظڇبث بثب پضخثبث قبغبÃكëڄبث گبصلظ!',
             '𞥞𞤑𞤵𞤥𞤨𞤭𞤼𞤢𞤤 𞤳𞤵𞤥𞤨𞤭𞤼𞤢𞤤 𞤢𞤤𞤢 𞤸𞤫𞤧𞤤𞤢𞤤 𞤱𞤢𞤯𞤢•𞤲•𞤺𞤢𞤤 𞤦𞤢𞤪𞤳𞤭!'
            ],
            ['لنجسظڇبث لنجسظڇبث بثب پضخثبث قبغبÃكëڄبث گبصل?',
             '𞥟𞤑𞤵𞤥𞤨𞤭𞤼𞤢𞤤 𞤳𞤵𞤥𞤨𞤭𞤼𞤢𞤤 𞤢𞤤𞤢 𞤸𞤫𞤧𞤤𞤢𞤤 𞤱𞤢𞤯𞤢•𞤲•𞤺𞤢𞤤 𞤦𞤢𞤪𞤳?'
             ]
        ]
    },
  }

  converter = AhomConverter(FONTS_TO_CONVERT, thisDefaultOutputFont)
  for script in testcases:
      fontIndex = testcases[script]['fontIndex']
      toLower = testcases[script]['toLower']
      sentenceCase = testcases[script]['sentenceCase']
      for test in testcases[script]['tests']:
          input = test[0]
          expected = test[1]
          result = converter.convertText(input,
                                         fontIndex=fontIndex)
          if result != expected:
              print ('** Unexpected results: \n  expected(%d) = %s\n  Result(%d)   = %s' % (
                  len(expected), expected, len(result), result))
              print('Old text = %s' % input)
          else:
              print ('* PASSES * %s case %s  ' % (script, expected))

              
def testParagraph():
    # Checks how paragraph operations work, e.g., split, inserting punctuation
    # at front.
    test_paragraphs = [
        '٣)- فضٍقن غظٍ غعع لعكڄظ: ثبصبث⹁ ثبصض⹁ پضثٌع⹁ لضثٌض⹁ ٻبَكڄعث⹁ ٻبَثظ⹁ ثضڄٌبث⹁ ثضڄغض⹁ ثضلٌظپظ⹁ ثضلغض⹁ ثضلٌظ⹁ ثضلٌضٍثض⹁ تضقڄبث⹁ تضقثض⹁ ض لع طـبڇظغَ ض غظٍ لعكڄظ تعق غعع؟',
        '٣)- فضٍقن غظٍ غعع لعكڄظ: ثبصبث⹁ ثبصض⹁ پضثٌع⹁ لضثٌض⹁ ٻبَكڄعث⹁ ٻبَثظ⹁ ثضڄٌبث⹁ ثضڄغض⹁ ثضلٌظپظ⹁ ثضلغض⹁ ثضلٌظ⹁ ثضلٌضٍثض⹁ تضقڄبث⹁ تضقثض⹁ ض لع طـبڇظغَ ض غظٍ لعكڄظ تعق غعع!',
        '  ?ض جظخبث: لبص ض جظخبث: لبص .ض جظخبث: لبص!'

    ]
    adlamConverter = AdlamConverter(FONTS_TO_CONVERT, thisDefaultOutputFont)
    for test in test_paragraphs:
        result = adlamConverter.findSentencesInParagraph(test)


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


def testAhomStrings():
    t = ["dahom", "babcfbc", "def hik",  "cjkl mno ar", 'kMo koM', 'Rk', 'kRY', '``']
    expected = ['𑜓𑜡𑜑𑜨𑜉',
                '𑜈𑜡𑜈𑜋𑜇𑜈𑜋',
                '𑜓𑜇𑜦 𑜑𑜢𑜀',
                '𑜋𑜩𑜀𑜎 𑜉𑜃𑜨 𑜡𑜍',
                '𑜀𑜪𑜨 𑜀𑜪𑜨',
                '𑜀𑜞',
                '𑜀𑜞𑜝',
                '𑜽'
    ]
    

    converter = AhomConverter()
    index = 0
    for text in t:
        result = converter.convertText(text, fontIndex=0)
                
        print("%s --> %s" % (text, result))
        if expected[index] != result:
            print('!!! Expected %s but got %s' % (expected[index], result))
        index += 1
    
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
    #convertDocFiles(argv[2:])
    testAhomStrings()
    #testConvert()
    #testParagraph()


if __name__ == '__main__':
  main(sys.argv)
