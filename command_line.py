#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from io import StringIO

import glob
import logging
import os
import sys

import docx
from docx import Document

import adlamConversion
import ahomConversion
from mendeConverter import MendeConverter
import phkConversion

from convertDoc2 import ConvertDocx


# get uploaded file into document form
def createDocFromFile(file_path):
    try:
        file = open(file_path, 'rb')
        text = file.read()
        data = BytesIO(text)
        count = len(text)
        doc = Document(data)
        file.close()
        return doc, count
    except BaseException as err:
        print('Cannot create Docx for %s. Err = %s' % (file_path, err))
        return None, -1


def convertThisDoc(lang, inputFileName):
    base_name = os.path.splitext(inputFileName)[0]
    out_file_name = base_name + '_Unicode.docx'

    if base_name.find('Unicode') > 0:
        return None

    doc, file_size = createDocFromFile(inputFileName)

    if not doc:
        logging.warning('No document %s opened: %s', inputFileName, docx)
        return None
    else:
        logging.info('Doc created from %s', inputFileName)

    sentence_mode = False
    lang_converter = None
    if lang == 'ff':
        lang_converter = adlamConversion.AdlamConverter()
        sentence_mode = True
    elif lang == 'aho':
        lang_converter = ahomConversion.AhomConverter()
    elif lang == 'phk':
        lang_converter = phkConversion.PhakeConverter()
    elif lang == 'men':
        lang_converter = MendeConverter()
    if not lang_converter:
        return None

    lang_converter.setScriptIndex(0)
    lang_converter.setLowerMode(True)
    lang_converter.setSentenceMode(sentence_mode)
    try:
        paragraphs = doc.paragraphs
    except AttributeError:
        pass

    # msgToSend = '%d paragraphs in %s\n' % (count, inputFileName)

    new_progress_obj = None
    doc_converter = ConvertDocx(lang_converter, documentIn=doc,
                                reportProgressObj=new_progress_obj)
    
    if doc_converter:
        result = doc_converter.processDocx()
        doc.save(out_file_name)
    else:
        result = None

    word_frequencies = None
    try:
        word_frequencies = lang_converter.getSortedWordList()
        if word_frequencies:
            # Do something with this information
            for item in word_frequencies:
                print(item)
    except BaseException as err:
        logging.warning('FAILED TO GET WORD LIST: %s' % err)

    return result


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

    for file_path in files:
        print('Converting %s in document %s' % (lang, file_path))
        result = convertThisDoc(lang, file_path)


if __name__ == '__main__':
    main(sys.argv)
