#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from io import StringIO

import logging
import os
import sys

import docx
from docx.enum.style import WD_STYLE_TYPE

import adlamConversion
import ahomConversion
import phkConversion

from convertDoc2 import ConvertDocx

from docx import Document
from docx.enum.style import WD_STYLE_TYPE


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
    new_doc = None
    
    baseName = os.path.splitext(inputFileName)[0]
    outFileName = baseName + '_Unicode.docx'


    doc, fileSize = createDocFromFile(inputFileName)

    if not doc:
        logging.warning('No document opened: %s', docx)
    else:
        logging.info('Doc created from %s', inputFileName)

    langConvert = None
    sentence_mode = False
    if lang =='ff':
        langConverter = adlamConversion.AdlamConverter()
        sentence_mode = True
    elif lang == 'aho':
        langConverter = ahomConversion.AhomConverter()
    elif lang == 'phk':
        langConverter = phkConversion.PhakeConverter()

    langConverter.setScriptIndex(0)
    langConverter.setLowerMode(True)
    langConverter.setSentenceMode(sentence_mode)
    paragraphs = doc.paragraphs
    count = len(paragraphs)
    msgToSend = '%d paragraphs in %s\n' % (count, inputFileName)
    countSent = 0

    newProgressObj = None
    docConverter = ConvertDocx(langConverter, documentIn=doc,
                               reportProgressObj=newProgressObj)
    
    if docConverter:
        result = docConverter.processDocx()
        doc.save(outFileName)
    else:
        result = None

    wordFrequencies = None
    try:
        wordFrequencies = langConverter.getSortedWordList()
        if wordFrequencies:
            # Do something with this information
            words = [x[0] for x in wordFrequencies]
            for item in wordFrequencies:
                print(item)
    except BaseException as err:
        print('FAILED TO GET WORD LIST: %s' % err)
        words = None
        
    return result

def main(argv):
    lang = argv[1]
    doc_path = argv[2]

    result = convertThisDoc(lang, doc_path)


if __name__ == '__main__':
    main(sys.argv)
