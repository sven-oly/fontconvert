#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Convert fonts in a dictionary .txt file, based on the individual tags for each section

# Command line: python run_dict_convert <lang_tag> <dict_file_name>
# Get the language converter
# Check if there's a dictionary_to_font in the class

# Open the input dictionary as read only
# Create new UNICODE name for the file

# Read dictionary file line by line. If starting with a tag, set current tag
# If not, keep current tag

# if current tag and text in the input line, run conversion on that
#   if has tag, output the tag
#   replace line with converted text.

# Close output file


from io import BytesIO
from io import StringIO

import logging
import os
import sys

import adlamConversion
import ahomConversion
import phkConversion


def convertDictionary(file_path, converter):
    if not converter:
        return None

    dict_to_font = None
    try:
        dict_to_font = converter.dictionary_to_font
    except:
        print('Converter has no dictionary_to_font info')
        return None

    try:
        file = open(file_path, 'rb')
        lines = file.readlines()
        in_count = len(lines)
        print("%d lines in input file %s" % (in_count, file_path))
        file.close()
    except BaseException as err:
        print('Cannot open input file for %s. Err = %s' % (file_path, err))
        return None, -1

    count = 0
    out_lines = []
    current_tag = ''
    for line in lines:
        if chr(line[0]) == '\u005c':
            has_tag = True
            sline = ''
            try:
                # Get into Unicode
                sline = line[1:].decode('8859')  # Maybe not utf-8
                sline.replace('\r\n', '')
            except UnicodeDecodeError as error:
                # Maybe a code outside of ASCII, e.g, 0xb9
                pass

            space_pos = sline.find(' ')
            current_tag = sline[0:space_pos]
            text = sline[space_pos:].replace('\r\n', '')
            # print('Tag %s for text \"%s\"' % (current_tag, text))

            out_line = process_line(current_tag, True, text, converter)

            # print('%s %s --> %s' % (count, current_tag, out_line))

            count += 1
        else:
            # Continuation line. Handle without a tag
            has_tag = False
            sline = line.decode('8859').replace('\r\n', '')  # Maybe not UTF-8?

            out_line = process_line(current_tag, False, sline, converter)

        out_lines.append(out_line)

    return out_lines

def process_line(current_tag, has_tag, line, converter):
    # TODO: handle return line
    if current_tag in converter.dictionary_to_font:
        tag_info = converter.dictionary_to_font[current_tag]
        if len(tag_info) > 1:
            input_font = tag_info[-1]
            # print('tag %s font %s' % (current_tag, input_font))
            text_out = converter.convertText(line, inputFont=input_font)
        else:
            text_out = line
    else:
        # Unchanged line
        text_out = line

    if has_tag:
        out_line = '\\%s %s' % (current_tag, text_out)
    else:
        out_line = text_out
    return out_line
def convertThisDictionary(lang, inputFileName):
    # Takes a dictionary, creating output file
    baseName = os.path.splitext(inputFileName)[0]
    outFileName = baseName + '_Unicode.docx'

    result = False

    langConverter = None
    sentence_mode = False
    if lang =='ff':
        langConverter = adlamConversion.AdlamConverter()
        sentence_mode = True
    elif lang == 'aho':
        langConverter = ahomConversion.AhomConverter()
    elif lang == 'phk':
        langConverter = phkConversion.PhakeConverter()

    if not langConverter:
        print('No converter found for lang %s' % (lang))
        return

    langConverter.setScriptIndex(0)
    langConverter.setLowerMode(True)
    langConverter.setSentenceMode(sentence_mode)

    out_lines = convertDictionary(inputFileName, langConverter)

    if out_lines:
        print('%s OUTLINES' % len(out_lines))

        out_file = open(outFileName, 'w')
        # HOW TO OUTPUT CORRECTLY? out_file.writelines(out_lines)
        out_file.writelines('\n'.join(out_lines))
        result = True
    else:
        print("CANNOT CONVERT %s" % inputFileName)

    # Report list of missed conversion
    if langConverter.not_converted:
        print(" Values not converted:")
        for key in langConverter.not_converted.keys():
            print('  %s: %d' % (key, langConverter.not_converted[key] ))

    return result

def main(argv):
    lang = argv[1]
    doc_path = argv[2]

    result = convertThisDictionary(lang, doc_path)

if __name__ == '__main__':
    main(sys.argv)
