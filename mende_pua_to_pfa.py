# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Convert JG Mendu PUA code points to range
# of Arabic Preseentation Forms A
# 2025-01-01

import os.path
import re
import sys

PUA_TO_PFA_offset = 0x1b50
PUA_TO_PFA_offset = 0x1b50

PUA_pattern = re.compile(r'[uU]\+([eE][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])')
PUA_pattern2 = re.compile(r'[uU]([eE][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])')

def update_code_point(m):
    old_code = int(m.group(1), 16)
    new_code = old_code + PUA_TO_PFA_offset
    new_code_point = 'U+' + hex(new_code)[2:]
    return new_code_point

def update_code_point2(m):
    old_code = int(m.group(1), 16)
    new_code = old_code + PUA_TO_PFA_offset
    new_code_point = 'u' + hex(new_code)[2:]
    return new_code_point

def main(argv):
    if len(argv) >= 2:
        file_name = argv[1]

    with open(file_name, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_line = PUA_pattern2.sub(update_code_point2, line)
        new_lines.append(new_line)
        print(new_line)

    out_filename = file_name + '.converted'
    with open(out_filename, 'w') as out_file:
        for new_line in new_lines:
            out_file.write(new_line)

if __name__ == '__main__':
    main(sys.argv)
