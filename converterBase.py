# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Base class for Docx converters
from __future__ import absolute_import, division, print_function

import os
import re
import sys


thisDefaultOutputFont = 'NotoSansRegular'


class ConverterBase:
    def __init__(self, old_font_list=None, new_font=None,
                 default_output_font=thisDefaultOutputFont):
        self.forceFont = True  # May be used to set all font fields to the Unicode font

        self.encodingScripts = []  # If given, tells the Script of incoming characters
        self.oldFonts = []
        self.font_resize_factor = 1.0
        self.not_converted = {}

        self.old_font_name = None
        self.font_index = -1

        # This may be set up by the individual converter
        self.split_by_script = {}

        # Only convert fonts from the provided list. This can be overridden if needed.
        self.check_all_fonts = False

        if new_font:
            self.unicodeFont = new_font
        else:
            self.unicodeFont = default_output_font

        # The fonts detected for conversion
        for item in old_font_list:
            if isinstance(item, list):
                self.oldFonts.append(item[0])
                self.encodingScripts.append(item[1])
            else:
                self.oldFonts.append(item)

        # If set, sets output font to be a complex script
        # This is needed for a number of Unicode scripts
        self.set_complex_font = False

        # Dictionary of script or other identifiers for conversions
        # of individual characters.
        self.description = ''

        # Range of characters for simple alphabetic
        self.first = chr(0x20)
        self.last = chr(0x7f)
        self.first_lower = chr(0x61)
        self.last_lower = chr(0x81)
        self.first_upper = chr(0x41)
        self.last_upper = chr(0x61)
        self.lowerOffset = ord(self.first_lower) - ord(self.first_upper)

        self.encoding = None
        self.debug = False  # False
        self.lower_mode = True
        self.sentence_mode = True

        # Recording information on the document details
        # Word frequency of the converted words
        self.collectConvertedWordFrequency = False
        self.convertedWordFrequency = {}

        # For reordering rules
        self.pattern_replace_list = []

        # For communicating to specific instances
        self.current_tag = ''

        # If set, can convert output characters to U+ representations
        self.output_u_mode = False

    def preprocess(self, textIn, current_tag):
        # Possibly do some preprocessing on each line, maybe dependent on a tab
        # or a regular expression
        return textIn

    def get_outfile_name(self, infile_name):
        name_split = os.path.splitext(infile_name)
        out_file_name = name_split[0] + '_Unicode' + name_split[-1]
        return out_file_name

    def setScriptRange(self, first, last):
        self.first = chr(first)
        self.last = chr(last)

    def setUpperCaseRange(self, first_upper, last_upper):
        self.first_upper = chr(first_upper)
        self.last_upper = chr(last_upper)

    def setLowerCaseRange(self, first, last):
        self.first_lower = chr(first)
        self.last_lower = chr(last)
        self.lowerOffset = ord(self.first_lower) - ord(self.first_upper)

    def isRtl(self):
        # Override for RTL language
        return False

    def unicode_to_u_plus(char):
        # Gives the string version of a Unicode code point
        return "U+" + hex(ord(char))[2:].upper().zfill(4)

    def convertText(self, in_text, font_text_info=None, font_index=0, inputFont=None):
        return in_text

    def toLower(self, in_text):
        # Does this work for all scripts?
        return in_text.lower()

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        new_text = in_text
        for pair in self.pattern_replace_list:
            new_text = re.sub(pair[0], pair[1], new_text)
        return new_text

    def tokenizeText(self, textIn):
        # ASCII and whitespace characters
        if self.old_font_name and self.split_by_script and self.old_font_name in self.split_by_script:
            token_regex = self.split_by_script[self.old_font_name]
            return token_regex.split(textIn)

        if self.scriptIndex == 0:
            return [i for i in re.split(r'([\w\s;.])', textIn) if i]
        else:
            return textIn

    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Handles details of converting the text, including case conversion.
    def convertString(self, textIn, fontInfo,
                      conversion_map):
        # type: (object, object, object) -> object
        convertedList = []
        convertResult = ''

        tokens = self.tokenizeText(textIn)
        if not tokens:
            # print('????? WHY NO TOKENS in %s' % textIn)
            pass

        for c in tokens:
            # Special handling if needed
            if not c:
                continue
            out = c
            if c in conversion_map:
                out = conversion_map[c]
            else:
                key = '%s-%s' % (self.encoding, c)
                if not key in self.not_converted:
                    self.not_converted[key] = 1
                    #for i in range(len(c)):
                    #    print('** Code point %s' % hex(ord(c[i])))
                    #print('Cannot convert %s in %s' % (c, self.encoding))
                else:
                    self.not_converted[key] += 1

            # Special case for handling underlined text
            convertedList.append(out)

        convertResult = self.reorderText(''.join(convertedList))

        try:
            if self.lower_mode:
                convertResult = self.toLower(convertResult)
        except BaseException:
            pass

        return convertResult

    def setLowerMode(self, lower_expected):
        self.lower_mode = lower_expected

    def setSentenceMode(self, sentence_mode):
        self.lower_mode = sentence_mode

    def toSentenceCase(self, in_text):
        if not in_text:
            return in_text
        first = in_text[0].upper()
        return first + in_text[1:]

    # Implemented by specific class for language and script.
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
                text_to_convert = run.text
                font_name = None
                scriptIndex = 0
                font_name = run.font.name
                # TODO: Check if unknown font regions should be converted.
                try:
                    scriptIndex = self.FONTS_TO_CONVERT.index(font_name)
                except BaseException as error:
                    print('Unknown font error %s: %s for text %s' % (error, font_name, text_to_convert))
                    if not self.check_all_fonts:
                        # Unknown fonts should not be examined
                        continue
                new_text = text_to_convert
                try:
                    new_text = self.convertText(text_to_convert, None, scriptIndex)
                except BaseException as error:
                    print('p.text failure in convertText: %s for text %s' % (error, p.text))

                # Replace font in empty regions, too!
                if run.text == '' or new_text != run.text:
                    try:
                        # Special processing for some types of runs
                        new_text = self.special_run_handling(new_text)
                        print('TRY SPECIAL %s' % new_text)
                    except:
                        pass
                    if self.set_complex_font:
                        run.font.complex_script = True

                    run.text = new_text
                    run.font.name = self.unicodeFont
                    try:
                        new_font_size = int(run.font.size * self.font_resize_factor)
                        run.font.size = new_font_size
                    except TypeError:
                        # There may be no associated font
                        pass
            except ValueError as error:
                print('ValueError %s with p.text: %s' % (error, p.text))
                continue

        # Check on the font for the full paragraph
        try:
            self.FONTS_TO_CONVERT.index(p.style.font.name)
            p.style.font.name = self.unicodeFont
        except ValueError:
            pass

        if self.handle_sentences:
            self.processSentences(p)

        try:
            if self.collectConvertedWordFrequency:
                self.updateWordsFrequencies(p)
        except BaseException:
            pass  # Not a fatal error

        return

    # Methods for word frequency information
    def setFrequencyCollection(self, new_state):
        self.collectConvertedWordFrequency = new_state

    def clearWordFrequencies(self):
        self.convertedWordFrequency.clear()

    # Adds a word to the word frequency list
    def addWordToFrequencyList(self, word):
        if word in self.convertedWordFrequency:
            self.convertedWordFrequency[word] += 1
        else:
            self.convertedWordFrequency[word] = 1

    def updateWordsFrequencies(self, paragraph):
        # implemented by specific converter class
        return

    def getWordFrequencies(self):
        return self.convertedWordFrequency

    def getSortedWordList(self):
        if self.convertedWordFrequency:
            return sorted(
              self.convertedWordFrequency.items(),
              key=lambda x: x[1],
              reverse=True
            )
        else:
            return None

    def getWordListByAlpha(self):
        if self.convertedWordFrequency:
            return sorted(
              self.convertedWordFrequency.items(),
              key=lambda x: x[0],
              reverse=True
            )
        else:
            return None
