from logging.handlers import SysLogHandler

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
from skimage.metrics import structural_similarity as ssim

from pathlib import Path

import json
import os
import sys

from font_analyze import get_supported_characters

# Location of the images rendered
font_base = Path('static/fonts')
lang_dir = 'Shan'
lang_font_path = font_base / lang_dir
save_file = True


def render_and_crop_glyph(char, font_path, image_size=128, font_size=100):
    """Renders a character, crops it tightly to its bounding box, and resizes it."""
    # Create a grayscale canvas
    img = Image.new('L', (image_size* 2, image_size * 2), color=0)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        raise FileNotFoundError(f"Could not load font at {font_path}")
        
    # Draw character in white
    draw.text((image_size // 4, image_size // 10), char, font=font, fill=255)
    if save_file:
        file_name = 'images/draw-%s.png' % char
        file_path = lang_font_path / file_name
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
    if save_file:
        file_name = 'images/resized-%s.png' % char
        file_path = lang_font_path / file_name
        if os.path.exists(file_path):
            os.remove(file_path)
        resized.save(file_path)
    return np.array(resized)

def find_best_match(target_char, source_font_path, candidate_font_path, candidate_pool=None):
    """Compares a target character against a pool of candidates in another font."""
    # Use standard alphanumeric characters if no specific pool is provided
    if candidate_pool is None:
        import string
        candidate_pool = string.ascii_letters + string.digits
        
    # Render the target reference glyph
    target_img = render_and_crop_glyph(target_char, source_font_path)
    
    best_char = None
    best_score = -1  # SSIM ranges from -1 (completely different) to 1 (identical)

    score_results = []
    # Try combining character to reduce dotted matches
    for candidate in candidate_pool:
        to_render = '\u00a0' + candidate
        candidate_img = render_and_crop_glyph(to_render, candidate_font_path)
        
        # Calculate Structural Similarity Index (SSIM)
        score = ssim(target_img, candidate_img)

        score_results.append([candidate, score, hex(ord(candidate))])
        if score > best_score:
            best_score = score
            best_char = candidate

    score_results.sort(key=lambda x: x[1], reverse=True)
    top_10 = range(0, min(len(score_results), 10))
    for index in top_10:
        print(score_results[index])
    return best_char, best_score


def get_all_images(source_font_path, char_list):
    all_target_images = {}
    for char in char_list:
        all_target_images[char] = render_and_crop_glyph(char, source_font_path)
    return all_target_images

def get_best_match(target_char, font_a_images, font_b_images):
    target_img = font_a_images[target_char]
    best_score = -1  # SSIM ranges from -1 (completely different) to 1 (identical)

    score_results = []
    # Try combining character to reduce dotted matches
    for candidate in font_b_images.keys():
        to_render = '\u00a0' + candidate
        candidate_img = font_b_images[candidate]

        # Calculate Structural Similarity Index (SSIM)
        score = round(float(ssim(target_img, candidate_img)), 4)

        score_results.append([candidate, score])
        if score > best_score:
            best_score = score

    score_results.sort(key=lambda x: x[1], reverse=True)
    top_10 = min(len(score_results), 10)

    return score_results[0:top_10]

def find_best_matches(font_a, font_b, font_b_candidates):
    a_supported = get_supported_characters(font_a)
    char_list = [item['char'] for item in a_supported]
    a_images = get_all_images(font_a, char_list)
    b_images = get_all_images(font_b, font_b_candidates)

    best_matches = {}
    for a_char in a_supported:
        char = a_char['char']
        index = hex(ord(char))
        best_matches[char] = get_best_match(char, a_images, b_images)

    # A dictionary of the top matches for each character in font a to font b
    return best_matches

# ==========================================
# EXAMPLE USAGE
# ==========================================
def main(argv):

    # Define paths to your local .ttf or .otf font files
    # font_a = "/System/Library/Fonts/Supplemental/Arial.ttf"
    # font_b = "/System/Library/Fonts/Helvetica.ttc"

    # Base for these fonts
    font_base = 'static/fonts'
    lang_base = 'Shan'
    # Shan font matching
    font_a = lang_font_path / "hacked/SHAN.TTF"
    font_b = lang_font_path / "unicode/NotoSansMyanmar-Light.ttf"
    # font_b = "static/fonts/Shan/unicode/Padauk.ttf"

    supported = get_supported_characters(font_a)

    # For Shan character matching
    candidate_pool = []
    for code in range(0x1000, 0x1049):
        candidate_pool.append(chr(code))
    for code in range(0x1075, 0x1099):
        candidate_pool.append(chr(code))
    candidate_pool.append(chr(0x109e))
    candidate_pool.append(chr(0x109e))

    if len(argv) > 1 and argv[1] == 'ALL':
        best_matches = find_best_matches(font_a, font_b, candidate_pool)

        json_data = {'font_a': str(font_a),
                     'font_b': str(font_b),
                     'best_matches': best_matches}

        # Save these matches in a file
        out_path = lang_font_path / 'best_matches.json'
        out_path.unlink(missing_ok=True)
        with open(out_path, 'w') as f:
            json.dump(json_data, f, indent=4)

        #
        # out_file.write('%s --> %s' % (font_a, font_b))
        # for key in best_matches.keys():
        #     out_file.write('"%s" %s\n' % (key, best_matches[key]))
        # out_file.close()
        return

    # Define what you are searching for
    if len(argv) > 1:
        target = argv[1]
    else:
        target = chr(0x61)

    try:
        match, confidence = find_best_match(target, font_a, font_b, candidate_pool)
        best_code_point = hex(ord(match))
        print(f"Target '{target}' in Font A best matches '{match}' ('{best_code_point}') in Font B.")
        print(f"Confidence Score (SSIM): {confidence:.4f}")
    except FileNotFoundError as e:
        print(e)
        print("[Notice] Please update the font paths with valid .ttf files on your system.")

if __name__ == '__main__':
    main(sys.argv)
