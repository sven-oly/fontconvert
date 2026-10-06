from fontTools.ttLib import TTFont
import unicodedata

directory_name = '/Users/craig/PycharmProjects/LanguageTools/static/fonts/'
font_name = 'Lepcha/Munsalong.ttf'
font_path = directory_name + font_name

def is_glyph_combining(font_path: str, glyph_name: str) -> bool:
    font = TTFont(font_path)
    
    # 1. First, check the GDEF table if it exists
    if "GDEF" in font and font["GDEF"].table and font["GDEF"].table.GlyphClassDef:
        class_defs = font["GDEF"].table.GlyphClassDef.classDefs
        print(f'class_defs = {class_defs}')
        if glyph_name in class_defs:
            # Class 3 specifically denotes Mark / Combining glyphs
            return class_defs[glyph_name] == 3

    # 2. Fallback: Reverse look up the code point from the cmap table
    cmap_table = font["cmap"].getBestCmap()
    if cmap_table:
        # Create a reverse map (glyph name -> code point)
        reverse_cmap = {name: code for code, name in cmap_table.items()}
        print(f'reverse_cmap = {reverse_cmap}')
        if glyph_name in reverse_cmap:
            codepoint = reverse_cmap[glyph_name]
            codepoint_char = chr(codepoint)
            print(f' CODE POINT {codepoint_char} {hex(codepoint)} category is: {unicodedata.category(chr(codepoint))}')
            # Check the Unicode character category (starts with 'M' for Mark)
            return unicodedata.category(chr(codepoint)).startswith('M')
            
    return False

# Example usage:
glyph_name = 'bracketright'

print(f'Info on font {font_path}:')
print(is_glyph_combining(font_path, glyph_name))
