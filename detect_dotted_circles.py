import uharfbuzz as hb


# 1. Define your input text (
text = "\u1c00\u1c36\u1c25"  # A space followed by a combining grave accent
text_good = "\u1c00\u1c25\u1c36"  # A space followed by a combining grave accent
font_path = "static/fonts/lep/unicode/NotoSansLepcha-Regular.ttf"  # Replace with a valid font path


def has_dotted_circle(text: str, font_path: str) -> bool:
    # 1. Load font and create HarfBuzz font object
    with open(font_path, "rb") as f:
        font_data = f.read()
    blob = hb.Blob(font_data)
    face = hb.Face(blob)
    font = hb.Font(face)

    # 2. Shape the text into a buffer
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)

    # 4. Check if the buffer contains the dotted circle glyph
    for info in buf.glyph_infos:
        gid = info.codepoint
        glyph_name = font.glyph_to_string(gid)  # Converts GID to its string representation

        # OpenType standard name is 'dottedcircle', sometimes 'uni25CC'
        if glyph_name in ("dottedcircle", "uni25CC"):
            return True

    return False

text_with_missing_base = "ั" # Thai mai-han-akat without a consonant

print(has_dotted_circle(text_good, font_path))
