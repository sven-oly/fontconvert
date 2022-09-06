# -*- coding: utf-8 -*-

#
# Convert list of Office files (.docx, .xslx, .pptx) files from
# old text encoding to Unicode.

import os
import re
import sys

from adlamConversion import AdlamConverter
from convertDoc2 import ConvertDocx
import convertOffice

from docx import Document

# For conversion from Arabic encoding or Latin

import convertUtil

defaultOutputFont = "Noto Sans Adlam New"

def main(argv):

    args = convertUtil.parseArgs()
    if args.font:
      newUnicodeFont = args.font
    else:
      newUnicodeFont = adlamConversion.defaultOutputFont

    # Other Latin fonts to convert?
    paths_to_doc = args.filenames

    # List of [fontName, encodingScript]
    FONTS_TO_CONVERT = [
        ['Fulfulde - Aissata', 'arab'],
        ['Fulfulde - Fuuta' , 'arab'],
        ['Fulfulde - Pulaar', 'arab'],
        ['Times New Roman', 'latn'],
    ]

    # Get the converter To Adlam.
    # TODO: Set up way to convert Latin Fula to Adlam, too!
    converter = AdlamConverter(newFont=newUnicodeFont)  # FONTS_TO_CONVERT, newUnicodeFont)
    # Set up parameters for conversion
    converter.setLowerMode(args.lower)
    converter.setSentenceMode(args.sentence)

    for input in paths_to_doc:
      
        doc = Document(input)
        
        docConverter = ConvertDocx(converter, doc)
        docConverter.processDocx()
        # convertOffice.convertOffice(input, args.output_dir, converter, version=2)

        outFileName = os.path.splitext(input)[0] + '_Unicode.docx'

        try:
            doc.save(outFileName)
        except BaseException as err:
            return 'Cannot save file %d. Err = %s' % (outFileName, err)
        sortedWords = converter.getSortedWordList()
        if sortedWords:
            print('WordFrequencies')
            for item in sortedWords:
                print(item)


if __name__ == "__main__":
  main(sys.argv)
