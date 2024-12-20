import copy
from enum import Enum
import logging
import sys

import command_line
import phkConversion

# Simple testing of assamese conversions

aiton_font_name = 'Aiton Script'
assamese_font_name = 'Assam New'
times_font_name = 'Times Roman'

class DictionaryMode(Enum):
    DictionaryNone = 0
    Aiton2English = 1
    English2Aiton = 2

class test_assamese():

    def __init__(self):
        self.as_font = 'Assam New'

        self.test_strings = [
            [['small branch'], ['[å¡§', 'ÊÃØ ±ÒÅ']],
            [[' type of rice'], ['¡Ò¡ ¢ÒF', 'àËμÒ']],
            [['to be stuck in the throat'], ['¡Ò§', 'å·å1Å ÅÒå¤  ̧ÃÒ']]
        ]
        return

def read_saved_file():
    input_strings = []
    filename = 'saved_assamese.txt'
    file = open(filename, mode='r', encoding='utf-8')
    if file:
        input_strings = file.readlines()
        return input_strings
    else:
        logging.error(' CANNOT READ FILE %s', filename)  # Rais an excpetion
        return None

def parse_definitions(doc):
    paragraphs = doc.paragraphs

    definitions = []  # List of 4 or 5 sections: Aiton, Latin, Assamese, Latin, [Assamese]

    a2e_definitions = []
    mode = DictionaryMode.Aiton2English  # Default

    for p in paragraphs:
        # Find a list of runs that ends with \n

        end_indices = []
        index = 0
        for r in p.runs:
            pos =  r.text.find('\n')
            if  r.text.find('\n') >= 0:
                end_indices.append(index)
            index += 1
        # one after the last item
        end_indices.append(len(p.runs))

        run_iterator = iter(p.runs)

        start = 0
        for n_index in end_indices:
            # Process the items in range start to (n_index-1)
            print(start, n_index)
            definition_a2e = parse_a2e(start, n_index, p.runs)
            a2e_definitions.append(definition_a2e)
            start = n_index + 1

        if p.text == 'Aiton - English':
            mode = DictionaryMode.Aiton2English
        elif p.text == 'English - Aiton':
            mode = DictionaryMode.English2Aiton

            return a2e_definitions

        english_word = ''
        try:
            while r := next(run_iterator):
                # Look for the lines in the definitions
                definition = {}
                if r.text == '\n':
                    r = next(run_iterator)

                font = r.font.name
                latin_text_0 = []
                if mode == DictionaryMode.English2Aiton:
                    while r and (font == times_font_name or font == None):
                        latin_text_0.append(r.text)
                        r = next(run_iterator)
                        font = r.font.name

                font = r.font.name
                aiton_text = []
                while r and font == aiton_font_name:
                    # Special case when more than one Aiton word is under a single English word
                    if mode == DictionaryMode.English2Aiton and not latin_text_0:
                        latin_text_0 = english_word
                    aiton_text.append(r.text)
                    r = next(run_iterator)
                    font = r.font.name

                latin_text_1 = []
                while r and (font == times_font_name or font == None):
                    latin_text_1.append(r.text)
                    r = next(run_iterator)
                    font = r.font.name

                assamese_text_1 = []
                while r and (font == assamese_font_name):
                    assamese_text_1.append(r.text)
                    r = next(run_iterator)
                    font = r.font.name

                latin_text_2 = []
                while r and (font == times_font_name or font == None):
                    latin_text_2.append(r.text)
                    r = next(run_iterator)
                    font = r.font.name

                assamese_text_2 = []
                while r and (font == assamese_font_name):
                    assamese_text_2.append(r.text)
                    try:
                        r = next(run_iterator)
                        font = r.font.name
                    except BaseException as err:
                        break

                definition['mode'] = mode
                definition['aiton'] = ''.join(aiton_text).strip()
                definition['latin_1'] = ''.join(latin_text_1).strip()
                definition['assamese_1'] = ''.join(assamese_text_1).strip()
                definition['latin_2'] = ''.join(latin_text_2).strip()
                definition['assamese_2'] = ''.join(assamese_text_2).strip()
                definition['latin_0'] = ''.join(latin_text_0).strip()

                # Special case:
                english_word = latin_text_0

                definitions.append(copy.deepcopy(definition))
        except BaseException as err:
            # End of the run or paragraph
            if not definition and mode == DictionaryMode.Aiton2English:
                definition['mode'] = mode
                definition['aiton'] = ''.join(aiton_text).strip()
                definition['latin_1'] = ''.join(latin_text_1).strip()
                definition['assamese_1'] = ''.join(assamese_text_1).strip()
                definition['latin_2'] = ''.join(latin_text_2).strip()
                definition['assamese_2'] = ''.join(assamese_text_2).strip()
                definition['latin_0'] = ''.join(latin_text_0).strip()
                definitions.append(copy.deepcopy(definition))

                definition = {}
            continue

    return definitions


def convert_definitions(definitions, converter, aiton_index, assamese_index):
    for definition in definitions:
        # Convert each field
        keys = definition.keys()
        for key, val in definition.items():
            old_val = definition
            if key == 'assamese_1' or key == 'assamese_2':
                definition[key] = converter.convertText(val, None, assamese_index, None)
            elif key == 'aiton':
                new_text = converter.convertText(val, None, aiton_index, None)
                definition[key] = new_text


def save_definitions(definitions):
    # Convert each definition and save in files

    # Open output files
    aiton2english_out = open('aiton2english.txt', 'w')
    english_out = open('english2aiton.txt', 'w')

    for definition in definitions:
        if definition['mode'] == DictionaryMode.Aiton2English:
            aiton2english_out.write('%s; %s; %s; %s; %s\n' % (
                                    definition['aiton'],
                                    definition['latin_1'],
                                    definition['assamese_1'],
                                    definition['latin_2'],
                                    definition['assamese_1'],
                                    ))
        else:
            english_out.write('%s; %s; %s; %s; %s\n' % (
                              definition['latin_0'],
                              definition['aiton'],
                              definition['latin_1'],
                              definition['assamese_1'],
                              definition['latin_2'],
                              ))
    aiton2english_out.close()
    english_out.close()


def parse_a2e(start, end, runs):
    # Get the text and the fonts for each set of runs
    run_sets = []
    current_text = []
    current_font = None
    for index in range(start, end):
        r = runs[index]

        new_font = r.font.name
        if new_font != current_font:
            if current_text:
                run_sets.append([current_font, ''.join(current_text)])
            current_text = []
        current_font = new_font
        current_text.append(r.text)
    if current_text:
        run_sets.append([current_font,  ''.join(current_text)])
    return run_sets


def read_assamese_words(tester, filename, converter, assamese_index):
    doc, size = command_line.createDocFromFile(filename)

    aiton_index = 2
    a2e_definitions = parse_definitions(doc)

    # Update convert_definitions to use the fonts with each
    convert_definitions(definitions, converter, aiton_index, assamese_index)
    save_definitions(definitions)

    # return definitions

    # find the assamese text strings
    try:
        paragraphs = doc.paragraphs
    except AttributeError:
        pass

    as_font = tester.as_font
    aiton_font_name = 'Aiton Script'
    after_aiton = False
    in_first_assam = False
    after_first_assam = False
    en_text = []
    assamese_strings = []

    return_list = []
    index = 0
    for p in paragraphs:
        assamese_line_data = []
        runs = p.runs
        for run in runs:
            if not run.text or run.text == '':
                continue
            run_font_name = run.font.name
            if run_font_name == aiton_font_name:
                assamese_raw = ' '.join(assamese_strings)
                result = converter.convertText(
                    assamese_raw, None, assamese_index, None)
                sindex = '%d' % index
                line_out = '; '.join([sindex, ' '.join(en_text).strip(), assamese_raw, result]).replace('\n', '')
                if line_out:
                    return_list.append(line_out.replace('\n', '') + '\n')
                    index += 1
                after_aiton = True
                in_first_assam = False
                after_first_assam = False
                en_text = []
                assamese_strings = []
            if run_font_name == "Times New Roman":
                pass
            if run_font_name == as_font:
                if not in_first_assam and not after_first_assam:
                    in_first_assam = True
                assamese_strings.append(run.text)
            if run_font_name == None:
                if in_first_assam:
                    in_first_assam = False
                    after_first_assam = True
                    en_text.append(run.text)
                if after_first_assam:
                    en_text.append(run.text)
    # Save the newly converted results.
    with open('saved_assamese.txt', 'w') as f:
        f.writelines(return_list)
    return return_list

def main(args):
    filename = args[1]
    logging.getLogger().setLevel(logging.DEBUG)

    tester = test_assamese()
    strings_to_test = tester.test_strings

    converter = phkConversion.PhakeConverter()
    old_fonts = list(converter.private_use_map.keys())
    as_font = tester.as_font
    assamese_index = old_fonts.index(as_font)
    converter.old_font_name = as_font

    # All the Assamese from the input file
    strings_to_test = []
    if len(args) > 2 and args[2] == "--redo":
        # Read all the originals and reconvert them all
        strings_to_test = read_assamese_words(
            tester, filename, converter, assamese_index)
    else:
        # Just compute the short list based on
        all_inputs = read_saved_file()
        test_indices = [1, 3,4,8,12, 16, 87, 5670]  # Get from parameter?
        for index in test_indices:
            strings_to_test.append(all_inputs[index])

    changed_list= []
    unchanged_list = []
    for inline in strings_to_test:
        data_in = inline.split(';')
        str_index = data_in[0]
        en_in = data_in[1]
        assamese_coded = data_in[2].strip()
        assamese_old = data_in[3].strip()
        text_to_convert = ' '.join(assamese_coded)
        result = converter.convertText(
            assamese_coded, None, assamese_index, None)
        if result == assamese_old:
            # logging.info('%s: %s %s UNCHANGED', str_index, en_in, result)
            unchanged_list.append(inline)
        else:
            logging.debug('%s: %s %s CHANGED --> %s', str_index, en_in, assamese_old, result)

            changed_list.append(inline)

    # report
    logging.debug('!! %d unchanged, %d changed', len(unchanged_list), len(changed_list))


if __name__ == '__main__':
    main(sys.argv)

