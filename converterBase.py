# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Base class for Docx converters
from __future__ import absolute_import, division, print_function

from collections import defaultdict

import logging
import os
import re

logger = logging.getLogger('converterBase')
logger.setLevel(logging.DEBUG)

thisDefaultOutputFont = 'NotoSansRegular'

class ConverterBase:
    def __init__(self, lang_code='unk',
                 old_font_list=None, new_font=None,
                 font_substitution_options=None,
                 default_output_font=thisDefaultOutputFont):

        self.defaultOutputFont = default_output_font
        self.thisDefaultOutputFont = default_output_font

        self.font_substitution_options = font_substitution_options
        self.font_replacements = {}
        self.font_substitution = {}
        all_output_fonts = []
        for key in self.font_substitution_options.keys():
            self.font_replacements[key] = self.font_substitution_options[key][0]
            self.font_substitution[key] = self.font_substitution_options[key][0]
            all_output_fonts.extend(self.font_substitution_options[key])
        self.OUTPUT_FONTS = set(all_output_fonts)

        self.lang_code = lang_code
        # Remember what's being converted
        self.lang_converter_filename = None
        self.forceFont = True  # May be used to set all font fields to the Unicode font

        self.encodingScripts = []  # If given, tells the Script of incoming characters
        self.encodingScript = []
        self.encodingScript = []
        if old_font_list:
            self.encodingScripts = old_font_list
        else:
            self.encodingScripts = self.FONTS_TO_CONVERT

        self.isRtl = False

        self.oldFonts = []
        self.font_resize_factor = 1.0
        self.not_converted = {}

        self.font_index = -1
        self.scriptIndex = 0  # Default

        # Information on language detection
        self.detectLang = False  # Generally not used
        self.ignoreLangs = []  # Language codes for not conversion
        self.lang_detector = None

        # This may be used for special formatting, e.g., keep a paragraph with next
        self.custom_paragraph_style = None

        self.handle_sentences = False

        self.add_variant_selectors = False
        # This may be set up by the individual converter
        self.split_by_script = {}

        # Only convert fonts from the provided list. This can be overridden if needed.
        self.check_all_fonts = False

        if new_font:
            self.unicodeFont = new_font
        else:
            self.unicodeFont = default_output_font

        self.current_table = None

        self.set_complex_font = False

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
        self.sentence_mode = False

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
        self.not_converted_context = defaultdict(list)

        # Other options
        self.remove_returns_in_block = False
        self.download_as_zip = False

        # Special case for handling paragraphs to be kept on the same page
        self.check_to_keep_paragraphs_with_next = False  # TEMPORARY True
        self.paragraphs_to_update_with_keep = []
        self.in_keep_with_next_group = False
        self.paragraphs_to_update_with_keep = []

    def preprocess(self, text_in, current_tag):
        # Possibly do some preprocessing on each line, maybe dependent on a tab
        # or a regular expression
        return text_in

    def get_outfile_name(self, infile_name):
        name_split = os.path.splitext(infile_name)
        out_file_name = name_split[0] + '_Unicode' + name_split[-1]
        return out_file_name

    def set_script_range(self, first, last):
        self.first = chr(first)
        self.last = chr(last)

    def set_upper_case_range(self, first_upper, last_upper):
        self.first_upper = chr(first_upper)
        self.last_upper = chr(last_upper)

    def set_lower_case_range(self, first, last):
        self.first_lower = chr(first)
        self.last_lower = chr(last)
        self.lowerOffset = ord(self.first_lower) - ord(self.first_upper)

    def is_rtl(self):
        # Override for RTL language
        return False

    def unicode_to_u_plus(self, char):
        # Gives the string version of a Unicode code point
        return "U+" + hex(ord(char))[2:].upper().zfill(4)

    def convertText(self, text_in, font_text_info=None, font_index=0, input_font=None):
        # Basic converter that takes an encoding map and applies that to the input text.
        # Take the data from the fontTextInfo field.
        convert_list = []
        if input_font not in self.private_use_map:
            return text_in
        encoding_map = self.private_use_map[input_font]
        tags = []
        result = self.convertString(text_in,None, encoding_map)

        return result

    def toLower(self, in_text):
        # Does this work for all scripts?
        return in_text.lower()

    def reorderText(self, in_text):
        # Next, move some code points in context to get proper Unicode ordering.
        new_text = in_text
        for pair in self.pattern_replace_list:
            try:
                new_text = re.sub(pair[0], pair[1], new_text)
            except BaseException as err:
                pass
        return new_text

    def tokenizeText(self, text_in):
        # New: split into Unicode characters. Simple.
        return list(text_in)

    def setScriptIndex(self, newIndex=0):
        # 0 = '', 1 = 'latn'
        self.scriptIndex = newIndex
        self.scriptToConvert = self.encodingScripts[self.scriptIndex]

    # Handles details of converting the text, including case conversion.
    def convertString(self, text_in, font_info,
                      conversion_map):
        # type: (object, object, object) -> object
        convertedList = []
        convertResult = ''

        tokens = self.tokenizeText(text_in)
        if not tokens:
            # print('????? WHY NO TOKENS in %s' % text_in)
            pass

        for c in tokens:
            # Special handling if needed
            if not c:
                continue
            out = c
            if c in conversion_map:
                out = conversion_map[c]
            else:
                out = c  # Don't remove things that are not defined.
                try:
                    key = '%s %s %s' % (self.encoding, c, hex(ord(c)))
                except:
                    logger.error('Cannot convert sequence >>%s<< in font %s. File = %s',
                                  c, font_info, self.lang_converter_filename)
                    out = c
                    continue
                if key not in self.not_converted:
                    self.not_converted[key] = 1
                    #for i in range(len(c)):
                    #    print('** Code point %s' % hex(ord(c[i])))
                    #print('Cannot convert %s in %s' % (c, self.encoding))
                else:
                    self.not_converted[key] += 1
                self.not_converted_context[key].append(text_in)

            # Special case for handling underlined text
            convertedList.append(out)

        try:
            convertResult = self.reorderText(''.join(convertedList))
        except TypeError as e:
            pass

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

        # Check the language of the paragraph. May not convert.
        # Disabled
        if self.detectLang:
            detected = self.lang_detector.classify(p.text.strip())
            logger.debug('processing paragraph detected lang: "%s"', detected)
            if self.debug:
                print('self.detectLang: %s. Found %s in %s' % (self.detectLang,detected, p.text))
            if detected[0] in self.ignoreLangs:
                logger.debug('ignoring lang %s in  %s', detected[0], self.ignoreLangs)
                print('IGNORING detected lang %s in %s' % (detected, p.text))
                return

        paragraph_was_converted = False
        for run in p.runs:
            try:
                text_to_convert = run.text
                scriptIndex = 0
                old_font_name = run.font.name
                try:
                    scriptIndex = self.FONTS_TO_CONVERT.index(old_font_name)
                except BaseException as error:
                    logger.warning('Unknown font %s: "%s" for text %s' % (error, old_font_name, text_to_convert))
                    if not self.check_all_fonts:
                        # Unknown fonts should not be examined
                        continue
                new_text = text_to_convert

                try:
                    new_text = self.convertText(text_to_convert, None, scriptIndex, input_font=old_font_name)
                except BaseException as error:
                    logging.error('p.text failure in convertText: %s for text %s' % (error, p.text))

                # Replace font in empty regions, too!
                if run.text == '' or new_text != run.text:
                    paragraph_was_converted = True
                    try:
                        # Special processing for some types of runs
                        new_text = self.special_run_handling(new_text)
                    except:
                        logging.warning('TRY SPECIAL FAILS %s' % new_text)
                        pass
                    if self.set_complex_font:
                        run.font.complex_script = True
                    # And reset the text to the converted value and
                    # the font to the selected replacement
                    run.text = new_text
                    new_font_name = self.unicodeFont
                    try:
                        new_font_name = self.get_substitute_font_for(old_font_name)
                    except BaseException as error:
                        # The default
                        pass
                    run.font.name = new_font_name

                    try:
                        new_font_size = int(run.font.size * self.font_resize_factor)
                        run.font.size = new_font_size
                    except TypeError as t_error:
                        # There may be no associated font
                        pass
            except ValueError as error:
                logging.error('ValueError %s with p.text: %s', error, p.text)
                continue

        # Check on the font for the full paragraph
        if not paragraph_was_converted:
            return

        # try:
        #     old_font_name = p.style.font.name
        #     try:
        #         p.style.font.name = self.get_substitute_font_for(old_font_name)
        #     except:
        #         p.style.font.name = self.unicodeFont
        # except ValueError as error:
        #     logger.warning('STYLE OLD FONT fails!')
        #     pass

        if self.handle_sentences:
            self.processSentences(p)

        try:
            if self.collectConvertedWordFrequency:
                self.updateWordsFrequencies(p)
        except BaseException:
            pass  # Not a fatal error

        return

    def processSentences(selfp):
        # This is converter-specific
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

    def map_runs_to_paragraph_text_positions(self, paragraph):
        # Mapping of run starts & ends to text positions
        run_map = []
        pos = 0
        run_index = 0
        for run in paragraph.runs:
            if run.text:
                run_map.append((pos, pos + len(run.text) - 1, run, run_index))
                pos += len(run.text)
            run_index += 1
        return run_map

    def find_returns_in_paragraph(self, p):
        # Gives the ending indices of the runs that have \n
        # in this paragraph.
        # Used to find ends of some types of structures in a document
        end_indices = []
        index = 0
        for r in p.runs:
            if r.text.find('\n') >= 0:
                end_indices.append(index)
            index += 1
        # one after the last item
        end_indices.append(len(p.runs))
        return end_indices

    def special_run_handling(self, text):
        # No special handling!
        return text

    def get_substitute_fonts(self):
        # Returns dictionary of fonts that are available for conversion / substitution
        return self.font_substitution_options

    def get_substitute_font_for(self, old_font):
        if old_font in self.font_replacements:
            return self.font_replacements[old_font]
        else:
            logger.warning('!!!!! Cannot get substitute font for: %s', old_font)
            new_font_name = None
            return new_font_name

    def set_substitute_font(self, old_font, new_font):
        self.font_replacements[old_font] = new_font
        logger.warning('SET SUB FONT (%s): %s -> %s', self.lang_code, old_font, new_font)
        logger.warning('  +++ replacements is %s', self.font_replacements)

    # Regex-based conversions for reordering, etc.
    # Swap order of two items
    def sub21(self, m):
        return m.group(2) + m.group(1)


