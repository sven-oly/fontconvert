# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert Tai Phake encoded text to Unicode.
from __future__ import absolute_import, division, print_function

import re
import sys

from converterBase import ConverterBase

# Script index

FONTS_TO_CONVERT = [
  'Phake Script', 'Phake Ramayana'
]

thisDefaultOutputFont = 'Noto Serif Myanmar Light'


def sub321(m):
    return m.group(3) + m.group(2) + m.group(1)

def sub21(m):
    return m.group(2) + m.group(1)

def sub3dfor2c2c(m):
    return '\U0001173d'

VARIANT_SELECTOR = '\uFE00'
def vsReplacer(matchobj):
    return matchobj.group(0) + VARIANT_SELECTOR

# Character constants for conversion
class PhakeConverter(ConverterBase):
    
    private_use_map = {
        'Phake Script': {
            "\t": '\t',
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
            "R": "ြ",
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
            "e": "ေ",
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
            "y": "ယ"
                 "",
            "z": "\uAA78",
            "@": "\ua9f2",
            "(": "(",
            ")": ")",
            "\u002f": "။",
            "\\": "၊",
            "[": "\u103c",
            "|": "\u103c",
            "]": "\u103c",
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
            "~": "~",
            " ": " "
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
            "R": "ြ",
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
            "e": "ေ",
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
            "[": "\u103c",
            "|": "\u103c",
            "]": "\u103c",
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
            "~": "~",
            " ": " "
        }        
    };

    # For splitting by ASCII characters
    # re.ASCII

    def __init__(self, oldFontList=FONTS_TO_CONVERT, newFont=None,
              defaultOutputFont=thisDefaultOutputFont):

        # These characters take variation sequence modifiers
        self.variation_sequence_code_points = re.compile(
            '([\u1000\u1002\u1004\u1010\u1011\u1015\u1019\u101a\u101c\u101d\u1022\u1031\u1075\u1078\u1080\uaa60\uaa61\uaa62\uaa63\uaa64\uaa65\uaa66\uaa6b\uaa6c\uaa6f\uaa7a])')

        self.add_variant_selectors = True
        self.handle_sentences = False

        self.encoding = 0  # Default
        self.encodingScripts = FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        self.oldFonts = []
        self.font_resize_factor = 0.65

        for item in oldFontList:
            if isinstance(item, list):
                self.oldFonts.append(item[0])
                self.encodingScripts.append(item[1])
            else:
                self.oldFonts.append(item)

        # Default script = 'Latn'
        self.scriptToConvert = 'Phake Script'
        self.scriptIndex = 0

        if newFont:
            self.unicodeFont = newFont
        else:
            self.unicodeFont = defaultOutputFont

        self.setScriptRange(0x1000, 0x106f)
        self.setUpperCaseRange(0x1000, 0x106f)
        self.description = 'Converts Phake font encoding to Unicode'

        self.defaultOutputFont = "Noto Serif Myanmar"

        self.forceFont = True  # May be used to set all font fields to the Unicode font

        self.isRtl = False

        self.description = 'Converts Phake font encoding to Unicode'
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

        # How words are split in Phake text - split on non-Phake text
        self.wordSplitRegEx = re.compile(r'(\W+)')

        self.collectConvertedWordFrequency = True
        self.convertedWordFrequency = {}

        # Information on language detection
        self.detectLang = False
        self.ignoreLangs = []  # Language codes for not conversion

    # TODO: check input and conversion tables for Unicode NFC normalization.

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        # e.g, vowel sign to right of consonants,.

        # TODO: Put in more conversions.
        pattern_replace_list = [
            [r'([\u1031\u103c]\ufe00?)([\u1000-\u1029\u1075-\u1081\uaa60-\uaa7a]\ufe00?)',
             sub21],
        ]

        newText = in_text
        for pair in pattern_replace_list:
            newText = re.sub(pair[0], pair[1], newText)

        return newText

    def add_variation_modifiers(self, text):
        out_text = re.sub(self.variation_sequence_code_points, vsReplacer, text);
        return out_text;

    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Split input into tokens for script conversion
    def tokenizeText(self, textIn):
        # ASCII and whitespace characters
        if self.scriptIndex == 0:
            return [i for i in re.split('([\w\s])', textIn) if i]
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

        if fontIndex < len(FONTS_TO_CONVERT):
            # Compute the encoding map for the encoding font
            encoding_map = self.private_use_map[self.encoding]
            self.token_splitter = re.compile('(\w)')
        else:
            # UnknownConversion 
            convertData = None
            encoding_map = None
            self.token_splitter = None

        if not fontTextInfo:
            # Only raw text, without formatting or structure information.
            result = self.convertString(textIn, None, encoding_map)

            result = self.reorderText(result)
            if self.add_variant_selectors:
                result = self.add_variation_modifiers(result)
            return result

        # Take the data from the fontTextInfo field.
        convertList = []
        for item in fontTextInfo:
            tags = []
            for fmt in item[1]:
                loc = fmt.tag.find('}')
                tags.append(fmt.tag[loc + 1:])

            convertList.append(
                self.convertString(item[0], tags, encoding_map))

        result = self.reorderText(''.join(convertList))
        if self.add_variant_selectors:
            result = self.add_variation_modifiers(result)

        return result

    # Handles details of converting the text, including case conversion.
    def convertString(self, textIn, fontInfo,
                      conversion_map):
        # type: (object, object, object) -> object
        convertedList = []
        convertResult = ''

        tokens = self.tokenizeText(textIn)
        if not tokens:
            print('????? WHY NO TOKENS in %s' % textIn)

        for c in tokens:
          # Special handling if needed
          out = c
          if c in conversion_map:
            out = conversion_map[c]
          else:
              for i in range(len(c)):
                  print('** Code point %s' % ord(c[i]))
              print('Cannot convert %s' % c)

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
                run.text = self.convertText(run.text, None, self.scriptIndex)
                run.font.name = self.unicodeFont
                new_font_size = int(run.font.size * self.font_resize_factor)
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
        result = converter.convertText(text, fontIndex=0)
                
        print("%s --> %s" % (text, result))
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
