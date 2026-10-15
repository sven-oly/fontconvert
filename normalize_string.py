import sys

import unicodedata

# Create a string with a base character 'a' followed by two diacritics out of numeric order:
# 1. Combining Diaeresis (\u0308) - (CCC = 230, Typographic Above)
# 2. Combining Dot Below  (\u0323) - (CCC = 220, Typographic Below)


def print_character_properties(text_string):
    for char in text_string:
        name = unicodedata.name(char)
        ccc = unicodedata.combining(char) # Returns the integer CCC value
        print(f"  {repr(char)} : {name:<24} -> CCC = {ccc}")

        
def get_result(input_str):
        
    print("--- Original Sequence ---")
    print_character_properties(input_str)

    # Apply NFD normalization, which enforces canonical combining order
    normalized_str = unicodedata.normalize('NFD', input_str)

    print("\n--- After NFD Normalization (Reordered) ---")
    print_character_properties(normalized_str)

    
def main(argv):
    if len(argv) > 1:
        input_string = argv[1]
        get_result(input_string)

        
if __name__ == '__main__':
    main(sys.argv)    
