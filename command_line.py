#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import logging
import os
import sys

import docx
from docx import Document

from io import BytesIO
from io import StringIO

import adlamConversion
import ahomConversion
from mendeConverter import MendeConverter
import phkConversion

from convertDoc2 import ConvertDocx

from check_complex_script import checkComplex

converters = {}
converters['ff'] = adlamConversion.AdlamConverter()
converters['aho'] = ahomConversion.AhomConverter()
converters['phk'] = phkConversion.PhakeConverter()
converters['men'] = MendeConverter()

# get uploaded file into document form
def createDocFromFile(file_path):
    try:
        with open(file_path, 'rb') as file:
            text = file.read()
            data = BytesIO(text)
            count = len(text)
    except BaseException as err:
        print('Cannot open file %s. Err = %s' % (file_path, err))
        raise err

    try:
        doc = Document(data)
    except (KeyError, TypeError, RuntimeError) as err:
            logging.warning('%s. Cannot process file: %s',
                            err, file_path)
            raise err
    return doc, count, None



def convertThisDoc(lang, input_file_name):
    # First, check if a converter exists
    sentence_mode = False
    lang_converter = None

    check_complex_script = False
    lang_converter = converters[lang]
    sentence_mode = False

    # Special settings
    if lang == 'ff':
        sentence_mode = True

    if not lang_converter:
        logging.error('Unknown language code: %s', lang)
        return None

    # Now get the .docx file
    base_name = os.path.splitext(input_file_name)[0]
    if base_name.find('Unicode') > 0:
        return None

    out_file_name = base_name + '_Unicode.docx'

    if base_name.find('Unicode') > 0:
        return None

    try:
        doc, file_size, err = createDocFromFile(input_file_name)
    except KeyError as err:
        logging.warning('%s for file: %s',
                        err, input_file_name)
        raise err

    if not doc:
        logging.warning('Document %s does not open:\n . Err =%s', input_file_name, err)
        return None
    else:
        logging.info('Doc created from %s', input_file_name)

    lang_converter.setScriptIndex(0)
    lang_converter.setLowerMode(True)
    lang_converter.setSentenceMode(sentence_mode)
    lang_converter.lang_converter_filename = input_file_name

    new_progress_obj = None
    doc_converter = ConvertDocx(lang_converter, documentIn=doc,
                                reportProgressObj=new_progress_obj)

    if doc_converter:
        result = doc_converter.processDocx()

        # For some scripts
        if check_complex_script:
            checkComplex(lang, input_file_name, document=doc)
        doc.save(out_file_name)
    else:
        result = None

    # Special processing of this document by paragraph
    number_of_definitions = 0
    doc = doc_converter.document
    missing_english = []
    defs = []
    for p in doc.paragraphs:
        run_map = doc_converter.converter.map_runs_to_paragraph_text_positions(p)
        end_returns = doc_converter.converter.find_returns_in_paragraph(p)
        runs = p.runs
        start = 0
        for end in end_returns:
            # need to find the english words, i.e., the 4th set of runs with non-Aiton and non-Assamese text
            run_sets = get_run_sets(runs, start, end)
            try:
                # print('%d: %s' % (len(defs), run_sets[3]))
                defs.append(run_sets[3])
            except BaseException as err:
                logging.debug('%d: !!! %s' % (len(defs), run_sets))
                missing_english.append([len(defs), run_sets])

            start = end + 1

        number_of_definitions += len(end_returns)
    logging.info('Number of definitions: %s' % number_of_definitions)
    logging.info('MISSING ENGLISH %d' % len(missing_english))

    for item in missing_english:
        logging.debug('  %s' % item)
    print('-----------------')

    word_frequencies = None
    try:
        word_frequencies = lang_converter.getSortedWordList()
        if word_frequencies:
            # Do something with this information
            logging.info('Word frequencies as %d items', len(word_frequencies))
            for item in word_frequencies:
                logging.debug(item)
    except BaseException as err:
        logging.warning('FAILED TO GET WORD LIST: %s' % err)

    return result


def get_run_sets(runs, start, end):
    run_sets = []
    current_text = []
    current_font = 'Zero'  # Same as Times or other Latin font
    text_blocks = []
    for index in range(start, end):
        r = runs[index]

        new_font = r.font.name
        # Normalize the font
        if not (new_font == "Ramayana Unicode" or new_font == "Noto Serif Bengali" or new_font == "Aiton Script"):
            new_font = None  # All the same

        if new_font != current_font:
            # A switch in the meaning of the text
            # Capture the current set of text, removing surrounding spaces
            if current_text:
                text_blocks.append(''.join(current_text).strip())
            current_text = []

        current_font = new_font
        current_text.append(r.text)
    if current_text:
        text_blocks.append(''.join(current_text).strip())
    return text_blocks


def main(argv):
    if len(argv) < 3:
        print('Convert .docx files from font encodings to Unicode text')
        print('Usage: python3 command_line lang_code file1 file2 file ...')
        return

    lang = argv[1]

    # For each item in the list, [2:...]
    files = []
    for doc_path in argv[2:]:
        if os.path.isdir(doc_path):
            # Expand with glob
            files.extend(glob.glob(doc_path + "/*.docx"))
        else:
            files.append(doc_path)

    all_errors = []
    for file_path in files:
        # Skip anything already converted to Unicode
        unicode_in_name = file_path.find('_Unicode.')
        if unicode_in_name >= 0:
            # Only look at Unicode converted files
            continue
        print('Converting %s in document %s' % (lang, file_path))
        try:
            result = convertThisDoc(lang, file_path)
        except BaseException as err:
            logging.warning('KeyError: %s. Cannot process file: %s', err, file_path)
            all_errors.append(err)

    if len(all_errors) > 0:
        logging.error(all_errors)
    else:
        logging.info('No top level errors found')

if __name__ == '__main__':
    main(sys.argv)
