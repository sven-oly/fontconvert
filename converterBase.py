# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Base class for Docx converters
from __future__ import absolute_import, division, print_function

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

    def convertText(self, in_text, font_text_info=None, font_index=0):
        return in_text

    def toLower(self, in_text):
        # Does this work for all scripts?
        return in_text.lower()

    def convertString(self, in_text, font_info, conversion_map):
        return in_text

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
