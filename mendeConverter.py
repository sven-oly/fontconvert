# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert font encoded Mende Kikakui text to Unicode.
from __future__ import absolute_import, division, print_function

import logging
import os
import re
import sys

from converterBase import ConverterBase

class MendeConverter(ConverterBase):
    private_use_map = {
        'JG Mende':  {
            # From Private Use Area to Unicode
            '\ue000': '\U0001E88C',
            '\ue002': '\U0001E88D',
            '\ue005': '\U0001E88E',
            '\ue008': '\U0001E88F',
            '\ue009': '\U0001E890',
            '\ue00c': '\U0001E892',
            '\ue00d': '\U0001E891',
            '\ue00f': '\U0001E808',
            '\ue011': '\U0001E809',
            '\ue013': '\U0001E80A',
            '\ue015': '\U0001E80B',
            '\ue017': '\U0001E80C',
            '\ue019': '\U0001E80E',
            '\ue01b': '\U0001E80D',
            '\ue01d': '\U0001E810',
            '\ue01f': '\U0001E811',
            '\ue020': '\U0001E812',
            '\ue022': '\U0001E80F',
            '\ue025': '\U0001E893',
            '\ue027': '\U0001E894',
            '\ue029': '\U0001E895',
            '\ue02b': '\U0001E897',
            '\ue02d': '\U0001E898',
            '\ue02f': '\U0001E89E',
            '\ue031': '\U0001E89D',
            '\ue033': '\U0001E89B',
            '\ue035': '\U0001E896',
            '\ue036': '\U0001E89C',
            '\ue039': '\U0001E899',
            '\ue03a': '\U0001E89A',
            '\ue03b': '\U0001E81B',
            '\ue03d': '\U0001E81C',
            '\ue03f': '\U0001E81D',
            '\ue041': '\U0001E81E',
            '\ue043': '\U0001E81F',
            '\ue044': '\U0001E821',
            '\ue046': '\U0001E820',
            '\ue049': '\U0001E89F',
            '\ue04a': '\U0001E8A0',
            '\ue04d': '\U0001E8A1',
            '\ue04f': '\U0001E8A2',
            '\ue050': '\U0001E8A3',
            '\ue053': '\U0001E8A5',
            '\ue055': '\U0001E8A4',
            '\ue056': '\U0001E8A6',
            '\ue05b': '\U0001E8AA',
            '\ue058': '\U0001E8A7',
            '\ue059': '\U0001E8A8',
            '\ue05a': '\U0001E8A9',
            '\ue05e': '\U0001E8AC',
            '\ue05f': '\U0001E8AB',
            '\ue061': '\U0001E85A',
            '\ue062': '\U0001E85B',
            '\ue063': '\U0001E85C',
            '\ue065': '\U0001E85D',
            '\ue066': '\U0001E85E',
            '\ue068': '\U0001E860',
            '\ue069': '\U0001E85F',
            '\ue06a': '\U0001E862',
            '\ue06c': '\U0001E8B9',
            '\ue06d': '\U0001E8BA',
            '\ue06f': '\U0001E8BB',
            '\ue071': '\U0001E8BC',
            '\ue073': '\U0001E8BD',
            '\ue075': '\U0001E8BF',
            '\ue077': '\U0001E8BE',
            '\ue079': '\U0001E844',
            '\ue07b': '\U0001E845',
            '\ue07d': '\U0001E846',
            '\ue07f': '\U0001E847',
            '\ue081': '\U0001E848',
            '\ue083': '\U0001E84A',
            '\ue084': '\U0001E849',
            '\ue086': '\U0001E836',
            '\ue089': '\U0001E837',
            '\ue08b': '\U0001E8AD',
            '\ue08f': '\U0001E839',
            '\ue091': '\U0001E83A',
            '\ue094': '\U0001E83C',
            '\ue098': '\U0001E83D',
            '\ue09a': '\U0001E8AE',
            '\ue09d': '\U0001E8AF',
            '\ue09e': '\U0001E8B0',
            '\ue0a0': '\U0001E8B1',
            '\ue0a2': '\U0001E8B2',
            '\ue0a5': '\U0001E843',
#            '\ue0a7': '\U0001E83B',  # Not sure what works with this Unicode value?
            '\ue0a7': '\U0001E8B3',
            '\ue0aa': '\U0001E83E',
            '\ue0ac': '\U0001E83F',
            '\ue0ae': '\U0001E840',
            '\ue0af': '\U0001E841',
            '\ue0b1': '\U0001E8B4',
            '\ue0b3': '\U0001E842',
            '\ue0b4': '\U0001E82E',
            '\ue0b6': '\U0001E82F',
            '\ue0b8': '\U0001E830',
            '\ue0ba': '\U0001E831',
            '\ue0bf': '\U0001E834',
            '\ue0c0': '\U0001E833',
            '\ue0c2': '\U0001E84B',
            '\ue0c4': '\U0001E84C',
            '\ue0c6': '\U0001E84D',
            '\ue0c8': '\U0001E84E',
            '\ue0ca': '\U0001E84F',
            '\ue0ce': '\U0001E852',
            '\ue0cf': '\U0001E8B5',
            '\ue0d1': '\U0001E8B6',
            '\ue0d3': '\U0001E8B7',
            '\ue0d8': '\U0001E8B8',
            '\ue0da': '\U0001E853',
      #       '\ue0db': '\U0001E850',
            '\ue0db': '\U0001E854',
            '\ue0dc': '\U0001E855',
            '\ue0dd': '\U0001E856',
            '\ue0e1': '\U0001E857',
            '\ue0e4': '\U0001E858',
            '\ue0e6': '\U0001E883',
            '\ue0e8': '\U0001E87E',
            '\ue0ea': '\U0001E879',
            '\ue0ec': '\U0001E87A',
            '\ue0ef': '\U0001E880',
            '\ue0f0': '\U0001E882',
            '\ue0f2': '\U0001E87C',
            '\ue0f4': '\U0001E87F',
            '\ue0f6': '\U0001E877',
            '\ue0f8': '\U0001E884',
            '\ue0fb': '\U0001E885',
            '\ue0fd': '\U0001E886',
            '\ue0ff': '\U0001E87B',
            '\ue101': '\U0001E87D',
            '\ue103': '\U0001E881',
            '\ue105': '\U0001E888',
            '\ue107': '\U0001E887',
            '\ue109': '\U0001E800',
            '\ue10b': '\U0001E801',
            '\ue10d': '\U0001E802',
            '\ue10f': '\U0001E803',
            '\ue111': '\U0001E804',
            '\ue112': '\U0001E806',
            '\ue114': '\U0001E805',
            '\ue116': '\U0001E807',
            '\ue117': '\U0001E868',
            '\ue118': '\U0001E869',
            '\ue119': '\U0001E86A',
            '\ue11c': '\U0001E86B',
            '\ue11d': '\U0001E86C',
            '\ue11f': '\U0001E86E',
            '\ue122': '\U0001E86D',
            '\ue123': '\U0001E86F',
            '\ue125': '\U0001E870',
            '\ue127': '\U0001E822',
            '\ue128': '\U0001E823',
            '\ue12a': '\U0001E824',
            '\ue12c': '\U0001E825',
            '\ue12e': '\U0001E826',
            '\ue130': '\U0001E828',
            '\ue132': '\U0001E827',
            '\ue133': '\U0001E829',
            '\ue134': '\U0001E871',
            '\ue136': '\U0001E872',
            '\ue138': '\U0001E873',
            '\ue13a': '\U0001E874',
            '\ue13c': '\U0001E88A',
            '\ue13e': '\U0001E876',
            '\ue140': '\U0001E814',
            '\ue141': '\U0001E815',
            '\ue142': '\U0001E816',
            '\ue143': '\U0001E817',
            '\ue144': '\U0001E818',
            '\ue145': '\U0001E819',
            '\ue147': '\U0001E81A',
            '\ue149': '\U0001E863',
            '\ue14a': '\U0001E864',
            '\ue14b': '\U0001E865',
            '\ue14c': '\U0001E866',
            '\ue14e': '\U0001E867',
            '\ue150': '\U0001E8C0',
            '\ue151': '\U0001E8C1',
            '\ue152': '\U0001E8C2',
            '\ue154': '\U0001E8C3',
            '\ue156': '\U0001E8C4',
            '\ue158': '\U0001E878',
            '\ue15a': '\U0001E889',
            '\ue15c': '\U0001E88B',
            '\ue15d': '\U0001E82B',
            '\ue160': '\U0001E82D',
            '\ue161': '\U0001E82A',
            '\ue08d': '\U0001E838',
            '\ue0bc': '\U0001E832',
            # No conversion to these Unicode values
            'X': 'U0001E813',
            'X': 'U0001E82C',
            'X': 'U0001E835',
            'X': 'U0001E851',
            'X': 'U0001E859',
            'X': 'U0001E861',
            'X': 'U0001E875',
            'X': 'U0001E8C7',
            'X': 'U0001E8C8',
            'X': 'U0001E8C9',
            'X': 'U0001E8CA',
            'X': 'U0001E8CB',
            'X': 'U0001E8CC',
            'X': 'U0001E8CD',
            'X': 'U0001E8CE',
            'X': 'U0001E8CF',
            'X': 'U0001E8D0',
            'X': 'U0001E8D1',
            'X': 'U0001E8D2',
            'X': 'U0001E8D3',
            'X': 'U0001E8D4',
            'X': 'U0001E8D5',
            'X': 'U0001E8D6',
        # Possible convert other JGMende PUA points to Arabic range?
            #// For missing values converted to Arabic Presentation Forms A,
            #// Add +1B50 to get the value in that modified Kikakui Sans Pro font.
        }
    }

    def __init__(self, oldFontList=None, newFont=None,
                 defaultOutputFont=None):
        self.scriptIndex = 0   # Default value
        self.private_use_map['Kikakui Sans Pro'] = self.private_use_map['JG Mende']
        self.FONTS_TO_CONVERT = list(self.private_use_map.keys())
        self.check_all_fonts = True

        self.unicodeFont = 'Noto Sans Mende Kikakui'
        if defaultOutputFont:
                self.thisDefaultOutputFont = defaultOutputFont
        else:
            self.thisDefaultOutputFont = 'Noto Serif Mende Kikakui'

        # If true, the converter will also look for strings representing
        # code points, without "\"
        self.convert_hex_codes = True
        self.re_unicode = re.compile('[uU]\+([0-9a-fA-F]+)')

        self.handle_sentences = False
        self.detectLang = False

        self.font_resize_factor = 1.0

        self.not_converted = {}
        self.collectConvertedWordFrequency = True
        self.convertedWordFrequency = {}

        self.encoding = 0  # Default
        self.encodingScripts = self.FONTS_TO_CONVERT  # If given, tells the Script of incoming characters
        if oldFontList:
            self.oldFonts = self.FONTS_TO_CONVERT
        else:
            self.oldFonts = oldFontList
            
        self.font_resize_factor = 1.0

        self.token_splitter = re.compile('[ a-zA-Z0-9\ue000-\ue162]')

        # Default script = 'Latn'

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, textIn, fontTextInfo=None,
                    fontIndex=0, inputFont=None):
        self.encoding = self.encodingScripts[fontIndex]
        # print('fontIndex %s, encoding = %s' % (fontIndex, self.encoding))
        encoding_index = fontIndex
        encoding_map = {}

        if inputFont:
            try:
                fontIndex = self.FONTS_TO_CONVERT.index(inputFont)
            except:
                # Font not found. Return the text
                return textIn
        else:
            inputFont = self.FONTS_TO_CONVERT[fontIndex]

        if fontIndex < len(self.FONTS_TO_CONVERT):
            self.encoding = inputFont
            # Compute the encoding map for the encoding font
            encoding_map = self.private_use_map[inputFont]
            self.token_splitter = re.compile('[ a-zA-Z0-9\ue000-\ue162]')
        else:
            # UnknownConversion - just return unchanged text
            encoding_map = None
            self.token_splitter = None
            return textIn

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

    # Consider the font information if relevant, e.g., underlining.
    # fontTextInfo: a list of font data for this code, including
    # formatting for each piece.
    def convertText(self, textIn, fontTextInfo=None,
                    fontIndex=0, inputFont=None):
        self.encoding = self.encodingScripts[fontIndex]
        # print('fontIndex %s, encoding = %s' % (fontIndex, self.encoding))
        encoding_index = fontIndex
        encoding_map = {}

        if inputFont:
            try:
                fontIndex = self.FONTS_TO_CONVERT.index(inputFont)
            except:
                # Font not found. Return the text
                return textIn
        else:
            inputFont = self.FONTS_TO_CONVERT[fontIndex]

        if fontIndex < len(self.FONTS_TO_CONVERT):
            self.encoding = inputFont
            # Compute the encoding map for the encoding font
            encoding_map = self.private_use_map[inputFont]
            self.current_encoding_map = encoding_map
            self.token_splitter = re.compile('[ a-zA-Z0-9\ue000-\ue162]')
        else:
            # UnknownConversion - just return unchanged text
            encoding_map = None
            self.token_splitter = None
            return textIn

        if not fontTextInfo:
            # Only raw text, without formatting or structure information.

            if self.convert_hex_codes:
                textIn = self.convertStringHexCodes(textIn, None, encoding_map)

            # Then process other characters
            result = self.convertString(textIn, None, encoding_map)

            result = self.reorderText(result)

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

    def tokenizeText(self, textIn):
        return [x for x in textIn]
        #return self.token_splitter.split(textIn)
    def subHexCode(self, m):
        # Look up the match in the encoding map
        hex_val = m.group(1)
        old_char = chr(int(hex_val,16))

        if old_char in self.current_encoding_map:
            new_char = self.current_encoding_map[old_char]
            new_hex = hex(ord(new_char))
            return new_hex.replace('0x', 'U+')
        # if present, replace with the text form
        # Otherwise, leave it
        return m.group(0)

    def convertStringHexCodes(self, textIn, font, encoding_map):
        # Look for "U+" codes in the line
        re_unicode = 'U+[0-9a-fA-F]+'

        textOut = self.re_unicode.sub(self.subHexCode, textIn)

        return textOut

    def special_run_handling(self, new_text):
        # Insert RTL marker in from
        new_text = '\u202E' + new_text
        return new_text

def testStrings(converter):
    t = ["\ue0db",
         '\ue0e1\ue0e4',
         ]
    expected = ['\u202e\U0001E854',
                ]

    index = 0
    success_count = 0
    for text in t:
        result = converter.convertText(text, fontIndex=0)
                
        # print("%s --> %s" % (text, result))
        if expected[index] != result:
            print('!!! Expected %s but got %s' % (expected[index], result))
        else:
            success_count += 1
        index += 1

    print('%d of %d strings were converted correctly' % (
        success_count, len(t)))
    return


# Reads a file, converting from JGMende font to Unicode
# Optionally checking for code points without \U
def convert_text_file(converter, infile_name):
    outfile_name = converter.get_outfile_name(infile_name)

    try:
        infile = open(infile_name, mode='r', encoding='UTF-8')
        outfile = open(outfile_name, mode='w', encoding='UTF-8')
    except BaseException as err:
        logging.error('%s. File open error: %s, %s', err, infile_name, outfile_name)
        return None

    # For each line in the input, convert text and output

    lines = infile.readlines()

    outlines = []
    input_font = 'JG Mende'
    for line in lines:
        text_out = converter.convertText(line, inputFont=input_font)
        outlines.append(text_out)

    try:
        outfile.writelines(outlines)
        outfile.close()
    except BaseException as err:
        logging.error('%s. Problem saving output file %s', err, outfile)

    return

def main(argv):
    infile_name = None
    if len(argv) > 1:
        infile_name = argv[1]

    converter = MendeConverter()

    if infile_name:
        convert_text_file(converter, infile_name)
    else:
        testStrings(converter)

if __name__ == '__main__':
  main(sys.argv)




    
