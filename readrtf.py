from striprtf.striprtf import rtf_to_text

import sys

def processLine(text):
    return rtf_to_text(text)

def readRtf(filename):
    with open(filename) as infile:
        for line in infile:
            result = processLine(line)
            print(result)

def main(args):
    readRtf(arg[1])

if __name__ == "__main__":
    main(sys.argv)
