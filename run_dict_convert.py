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
#   if the line has a tag, output the tag
#   replace line with converted text.

# Close output file


from io import BytesIO
from io import StringIO

import logging
import os
import re
import sys

import adlamConversion
import ahomConversion
import phkConversion


def convert_dictionary(file_path, converter):
    if not converter:
        return None

    try:
        dict_to_font = converter.dictionary_to_font
    except BaseException:
        print('Converter has no dictionary_to_font info')
        return None

    try:
        file = open(file_path, 'rb')
        #file = open(file_path, 'r')
        lines = file.readlines()
        in_count = len(lines)
        print("%d lines in input file %s" % (in_count, file_path))
        file.close()
    except BaseException as err:
        print('Cannot open input file for %s. Err = %s' % (file_path, err))
        return None, -1

    new_lines = reconnect_lines(lines)

    count = 0
    out_lines = []
    current_tag = ''
    preconverted_lines = []
    text = ''
    for line in lines:
        if chr(line[0]) == '\u005c':
            has_tag = True
            sline = ''
            try:
                # Get into Unicode
                sline = line[1:].decode('utf-8')  # Maybe not utf-8
                sline.replace('\r', '').replace('\n', '')
            except UnicodeDecodeError as error:
                # Maybe a code outside of ASCII, e.g, 0xb9
                pass

            space_pos = sline.find(' ')
            current_tag = sline[0:space_pos].replace('\r', '').replace('\n', '')

            # Output preconverted_lines, if any.
            if preconverted_lines:
                out_lines.extend(preconverted_lines)
                preconverted_lines = []

            text = sline[space_pos:].replace('\r', '').replace('\n', '')
            # print('Tag %s for text \"%s\"' % (current_tag, text))

            changed, out_line = process_line(current_tag, True, text, converter)
            if not changed:
                out_line = '\\%s %s' % (current_tag, text)
            else:
                preconverted_lines.append('\\%sx %s' % (current_tag, text))
        else:
            # Continuation line. Handle without a tag
            has_tag = False
            try:
                sline = line.decode('utf-8').replace('\r', '').replace('\n', '')  # Maybe not UTF-8?
            except UnicodeDecodeError as err:
                sline = re.sub(r'[\x80-\xff]', '???', line.decode('latin-1')).replace('\r\n', '')


            changed, out_line = process_line(current_tag, False, sline, converter)
            if not changed:
                outline = '%s' % text
            else:
                preconverted_lines.append('%s' % sline)

        count += 1  # line number - 1
        out_lines.append(out_line)

    if preconverted_lines:
        out_lines.extend(preconverted_lines)
        preconverted_lines = []
    return out_lines


def process_line(current_tag, has_tag, line, converter):
    # TODO: handle return line
    changed = False
    text_out = line  # default

    if current_tag in converter.dictionary_to_font :
        # Save the current line as uncoverted with 'x' appended to the tag
        tag_info = converter.dictionary_to_font[current_tag]
        if len(tag_info) > 1:
            input_font = tag_info[-1]
            try:
                font_index = converter.FONTS_TO_CONVERT.index(input_font)
                text_out = converter.convertText(line, fontIndex=font_index, inputFont=input_font)
                if text_out:
                    changed = True
                else:
                    text_out = line  # Unconverted
            except:
                # This font is not handled by this converter.
                pass

    if has_tag:
        out_line = '\\%s %s' % (current_tag, text_out)
    else:
        out_line = text_out

    result_line = out_line
    if result_line:
        result_line = out_line.replace('\n', '')
    return changed, result_line


def convertThisDictionary(lang, input_file_name):
    # Takes a dictionary, creating output file
    file_name_split = os.path.splitext(input_file_name)
    out_file_name = file_name_split[0] + '_Unicode' + file_name_split[-1]

    result = False

    lang_converter = None
    sentence_mode = False
    if lang =='ff':
        lang_converter = adlamConversion.AdlamConverter()
        sentence_mode = True
    elif lang == 'aho':
        lang_converter = ahomConversion.AhomConverter()
    elif lang == 'phk':
        lang_converter = phkConversion.PhakeConverter()

    if not lang_converter:
        print('No converter found for lang %s' % lang)
        return

    lang_converter.setScriptIndex(0)
    lang_converter.setLowerMode(True)
    lang_converter.setSentenceMode(sentence_mode)

    out_lines = convert_dictionary(input_file_name, lang_converter)

    if out_lines:
        print('%s OUTLINES' % len(out_lines))

        out_file = open(out_file_name, 'w')
        # HOW TO OUTPUT CORRECTLY?
        for outline in out_lines:
            if outline:
                out_file.write(outline + '\n')
            else:
                try:
                    out_file.write('\n')
                except TypeError as error:
                    logging.error('%s Problem with line %s', error, outline)
        result = True
    else:
        print("CANNOT CONVERT %s" % input_file_name)

    # Report list of missed conversion
    if lang_converter.not_converted:
        print(" Values not converted:")
        for key in lang_converter.not_converted.keys():
            key_parts = key.split('-', 1)
            print('  %s \"%s\": %d' % (key_parts[0],
                                       key_parts[1],
                                       lang_converter.not_converted[key]))

    return result


def reconnect_lines(lines):
    # For any line with content that is just after a tagged line,
    # reconnect it with the previous
    lines_out = []
    prev_line = ''
    index = 0
    for line in lines:
        try:
            sline = line.decode('utf-8').replace('\r\n', '')  # Maybe not utf-8
        except UnicodeDecodeError as error:
            sline = re.sub(r'[\x80-\xff]', '???', line.decode('latin-1')).replace('\r\n', '')
            continue
        if sline and sline[0] == '\u005c':
            # A new tag line found
            if prev_line:
                lines_out.append(prev_line)  # Generate the previous one
                has_tag = True
            prev_line = sline
        else:
            if len(sline) > 0:  # this must be a continuation line
                combined = prev_line + ' ' + sline
                lines_out.append(combined.replace('  ', ' '))  # Remove double spaces
                prev_line = ''
            else:
                if prev_line:
                    lines_out.append(prev_line)
                    prev_line = ''
                lines_out.append(sline)  # The empty line
        index += 1

    if prev_line:
        lines_out.append(prev_line)
    return lines_out



def main(argv):
    lang = argv[1]
    doc_path = argv[2]

    result = convertThisDictionary(lang, doc_path)


if __name__ == '__main__':
    main(sys.argv)
