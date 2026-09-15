import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
from skimage.metrics import structural_similarity as ssim

from pathlib import Path

import unicodedata

import json
import logging
import os
import string
import sys

from font_analyze import get_supported_characters

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Location of the images rendered
font_base = Path('conversion_files')
lang_code = 'shn'
lang_font_path = font_base / lang_code
save_file = True
conversion_base = Path('conversion_files')

image_out_path = None

#increases the match score if the language name matches
# that of the unicode character name
LANG_BOOST_FACTOR = 1.3

# Holds the options for running matching for given language code
conversion_cases = {
    'shn': {
        'langCode': 'shn',
        'langNameEn': 'Shan',
        'font_a': Path("hacked") /  "SHAN.TTF",
        'font_b': Path("unicode") / "NotoSansMyanmar-Light.ttf",
        'font_c': Path("unicode") / "Padauk.ttf",
        'unicode_fonts': [],  # TODO: Get directory listing
        'unicode_range': [(0x1000, 0x104a),
                          (0x1075, 0x109a),
                          (0x109e, 0x10a0)
                          ]
    },
    'lep' : {
        'langCode': 'lep',
        'langNameEn': 'Lepcha',
        'font_a': Path("hacked") / "Shipmoo.ttf",
        'font_b':  Path("unicode") / "Mingzat-Regular.ttf",
        'unicode_fonts': [],  # TODO: Get directory listing
        # The Lepcha Unicode block
        'unicode_range': [(0x1c00, 0x1C4F)],
     }
}

class match_process:
    def __init__(self, lang_code):
        self.lang_code = lang_code
        self.unicode_fonts = None
        self.hacked_fonts = None

        self.this_case = conversion_cases[self.lang_code]
        self.lang_name = self.this_case['langNameEn']

        # This may be loaded from existing data
        self.best_matches_data = None

        self.conversion_data_path = None
        self.font_path = None

        self.candidate_pool = []
        self.candidate_info = {}

        self.a_images = []
        self.b_images = []

        self.save_file = True
        self.image_out_path = None

        return

    def load_best_matches(self):
        # TODO: load existing best_matches file if present

        return

    def save_best_matches(self):
        # TODO: implement to save in conversion data

        return

    def compute_matches(self):
        # Define paths to your local .ttf or .otf font files
        # Base for these fonts

        static_base = Path('static') / 'fonts' / self.lang_code
        conversion_base = Path('conversion_files')
        conversion_lang_path = conversion_base / self.lang_code
        lang_font_path = Path(conversion_base) / self.lang_code / 'fonts'
        # font matching
        font_a = static_base / self.this_case['font_a']  # lang_font_path / "hacked/SHAN.TTF"
        font_b = static_base / self.this_case['font_b']  # lang_font_path / "unicode/NotoSansMyanmar-Light.ttf"

        self.image_out_path = conversion_base / self.lang_code / 'images'

        # For character matching
        self.candidate_pool = []
        self.candidate_info = {}
        unicode_ranges = self.this_case['unicode_range']
        self.lang_name = self.this_case['langNameEn']

        for region in unicode_ranges:
            for code in range(region[0], region[1]):
                character = chr(code)
                self.candidate_pool.append(character)
                try:
                    unicode_name = unicodedata.name(character)
                except:
                    continue

                matches_lang_name = self.lang_name.casefold() in unicode_name.casefold()
                self.candidate_info[chr(code)] = {
                    'name': unicode_name,
                    'category': unicodedata.category(character),
                    'lang_match': matches_lang_name,  # set if the name matches the language name
                }

        # TODO: give a boost when the unicode name matches the language name
        # TODO: figure out what we might do with category data (Mc, Mn) vs. "L*"
        best_matches = self.find_best_matches(font_a, font_b)

        # We may have multiple sets of matching data, with different
        # hacked fonts and different Unicode fonts
        json_data = [{'lang_code': self.lang_code,
                      'font_a': str(font_a),
                      'font_b': str(font_b),
                      'best_matches': best_matches,
                      'unicode_ranges': self.candidate_pool,  # Limit to those actually matched?
                      }]

        # Save these matches in a file
        out_path = conversion_lang_path / 'best_matches.json'
        out_path.unlink(missing_ok=True)
        with open(out_path, 'w') as f:
            json.dump(json_data, f, indent=4)

        logger.debug('Best matches (%d) saved to %', len(best_matches), out_path)

    def find_best_match(self, target_char, source_font_path, candidate_font_path):
        """Compares a target character against a pool of candidates in another font."""

        # Render the target reference glyph
        target_img = self.render_and_crop_glyph(target_char, source_font_path)

        best_char = None
        best_score = -1  # SSIM ranges from -1 (completely different) to 1 (identical)

        score_results = []
        # Try combining character to reduce dotted matches
        for candidate in self.candidate_pool:
            to_render = '\u00a0' + candidate
            candidate_img = self.render_and_crop_glyph(to_render, candidate_font_path)

            # Calculate Structural Similarity Index (SSIM)
            score = ssim(target_img, candidate_img)
            # TODO: if the candidate is part of the language, bump by the factor

            score_results.append([candidate, score, hex(ord(candidate))])
            if score > best_score:
                best_score = score
                best_char = candidate

        score_results.sort(key=lambda x: x[1], reverse=True)
        top_10 = range(0, min(len(score_results), 10))
        for index in top_10:
            print(score_results[index])
        return best_char, best_score

    def find_best_matches(self, font_a, font_b):

        # Use standard alphanumeric characters if no specific pool is provided
        if self.candidate_pool is None:
            self.candidate_pool = string.ascii_letters + string.digits

        a_supported = get_supported_characters(font_a)
        char_list = [item['char'] for item in a_supported]
        self.a_images = self.get_all_images(str(font_a), char_list, 'hacked')
        self.b_images = self.get_all_images(str(font_b), self.candidate_pool, 'unicode')

        logger.info('Matching %d by %d: %d pairs', len(self.a_images), len(self.b_images),
                     len(self.a_images) * len(self.b_images))
        best_matches = {}
        for a_char in a_supported:
            char = a_char['char']
            index = hex(ord(char))
            best_matches[char] = self.get_best_match(char, self.a_images, self.b_images)

        # A dictionary of the top matches for each character in font a to font b
        return best_matches

    def get_all_images(self, source_font_path, char_list, encoding):
        all_target_images = {}
        for char in char_list:
            all_target_images[char] = self.render_and_crop_glyph(char, source_font_path)
        return all_target_images

    def get_best_match(self, target_char, font_a_images, font_b_images):
        target_img = font_a_images[target_char]
        best_score = -1  # SSIM ranges from -1 (completely different) to 1 (identical)

        score_results = []
        # Try combining character to reduce dotted matches
        for candidate in font_b_images.keys():
            to_render = '\u00a0' + candidate
            candidate_img = font_b_images[candidate]

            # Calculate Structural Similarity Index (SSIM)
            score = round(float(ssim(target_img, candidate_img)), 4)
            if candidate in self.candidate_info and self.candidate_info[candidate]['lang_match']:
                scored = score * LANG_BOOST_FACTOR
            score_results.append([candidate, score])
            if score > best_score:
                best_score = score

        score_results.sort(key=lambda x: x[1], reverse=True)
        top_10 = min(len(score_results), 10)

        return score_results[0:top_10]

    def render_and_crop_glyph(self, char, font_path, image_size=128, font_size=100):
        """Renders a character, crops it tightly to its bounding box, and resizes it."""
        # Create a grayscale canvas
        img = Image.new('L', (image_size * 2, image_size * 2), color=0)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(font_path)
        except IOError:
            raise FileNotFoundError(f"Could not load font at {font_path}")

        # Draw character in white
        draw.text((image_size // 4, image_size // 10), char, font=font, fill=255)
        if self.save_file:
            file_name = 'draw-%s.png' % hex(ord(char))
            file_path = Path(self.image_out_path) / file_name
            file_path.unlink(missing_ok=True)
            img.save(file_path)

        # Crop to the tightly bound content box to eliminate positional variance
        bbox = img.getbbox()
        if not bbox:
            # Return a blank canvas if the character is empty (like a space)
            return np.zeros((image_size, image_size), dtype=np.uint8)

        cropped = img.crop(bbox)

        # Resize back to a uniform standard square for direct pixel comparison
        resized = cropped.resize((image_size, image_size), Image.Resampling.LANCZOS)
        if self.save_file:
            file_name = 'resized-%s.png' % hex(ord(char))
            file_path = self.image_out_path / file_name
            if os.path.exists(file_path):
                os.remove(file_path)
            resized.save(file_path)
        return np.array(resized)


lang_code = 'lep'

# ==========================================
# EXAMPLE USAGE
# ==========================================
def main(argv):
    # Takes multiple lang codes
    lang_code_list = argv[1:]

    for lang_code in lang_code_list:
        print('COMPUTING best matches for lang code = %s' % lang_code)
        process_info = match_process(lang_code)
        process_info.compute_matches()

    return


if __name__ == '__main__':
    main(sys.argv)
