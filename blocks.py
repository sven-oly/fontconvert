import unicodedata2

def lookup_block(char: str):
    try:
        return unicodedata2.block(char)
    except ValueError:
        return "Unknown Block"

print(lookup_block("A"))  # 'Basic Latin'
print(lookup_block("Д"))  # 'Cyrillic'
print(lookup_block("漢"))  # 'CJK Unified Ideographs'
print(lookup_block("✨"))  # 'Dingbats'

print(unicodedata2.name("A"))
