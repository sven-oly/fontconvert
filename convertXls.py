# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function

from copy import copy

import os
import re
import sys

# Read and process MS Excel documents from on script into another
# Unicode characters.

# https://openpyxl.readthedocs.io/en/default/tutorial.html
from openpyxl import Workbook
from openpyxl import load_workbook

import convertUtil

import adlamConversion

class cellData():
    def __init__(self):
        self.text = ''

class convertWorkbook():
    def __init__(self, input_path, output_dir, converter, debug=False):
        self.oldFonts = []
        self.input_path = input_path
        self.output_dir = output_dir
        self.converter = converter
        self.old_fonts = converter.oldFonts  # List of font names
        self.unicode_font = converter.unicodeFont
        self.cells_to_convert = ['c2', 'c3', 'c1987']
        self.cell_ranges = [['c2', 'c1987']]
        self.workbook = None

        if self.input_path:
            self.workbook = load_workbook(filename=self.input_path)
        # The sheets
        for sheet in self.workbook:
            print(sheet.title)

    def process(self):
      
        print('process path = %s, output_dir = %s\n' % (
          self.input_path, self.output_dir))

        # Get the first sheet
        sheets = self.workbook.sheetnames
        ws = self.workbook[sheets[0]]

        self.converter.setScriptIndex(adlamConversion.LATIN2ADLAM)
        # Get the range to convert.
        # for cell in self.cells_to_convert:
        #     latin = ws[cell].value
        #     adlam = self.converter.convertText(latin, fontIndex=adlamConversion.LATIN2ADLAM)
        #     ws[cell] = adlam
        # Special case
        cells = []
        for range1 in self.cell_ranges:
            cells = ws[range1[0]:range1[1]]

        for cell in cells:
            the_cell = cell[0]
            latin = the_cell.value
            adlam = self.converter.convertText(latin, fontIndex=adlamConversion.LATIN2ADLAM)
            the_cell.value = adlam
            # TODO: Set the font
            old_font = the_cell.font
            new_font = copy(old_font)
            new_font.name = self.converter.defaultOutputFont
            the_cell.font = new_font

    def processText(self):
        # Get the converter
        # For each item in the range specified, check the font information

        # Convert contents if needed

        # For each sheet, create copy
        # For each cell, convert the cell(s) as neeed

        # Save the new .xlsx file.
        return


    def info(self):
        # Get the workbook
        # chartsheets: list of all of them
        self.workbook = Woorbook
        #
        return


# For standalone and testing.
def main(argv):
    global debug_output

    args = convertUtil.parseArgs()

    debug_output = True
    paths_to_doc = args.filenames
    print('ARGS = %s' % args)

    for path in paths_to_doc:
        extension = os.path.splitext(path)[-1]

        converter = adlamConversion.AdlamConverter()
        if extension == '.xlsx':
            processor = convertWorkbook(path, args.output_dir, converter, debug_output)
            processor.process()
            out_file_name = 'OUTPUT.xlsx'  # Temporary
            processor.workbook.save(out_file_name)
        else:
            print('!!! Not processing file %s !' % path)


if __name__ == "__main__":
    main(sys.argv)
