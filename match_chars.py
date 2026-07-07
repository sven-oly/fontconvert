import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
from skimage.metrics import structural_similarity as ssim

import os
import sys

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
    file_path = 'draw-' + char + '.png'
    if os.path.exists(file_path):
        os.remove(file_path)
    img.save(file_path)

    # Crop to the tightly bound content box to eliminate positional variance
    bbox = img.getbbox()
    if not bbox:
        # Return a blank canvas if the character is empty (like a space)
        return np.zeros((image_size, image_size), dtype=np.uint8)
        
    cropped = img.crop(bbox)

    # Resize back to a uniform standard square for direct pixel comparison
    resized = cropped.resize((image_size, image_size), Image.Resampling.LANCZOS)
    file_path = 'resized-' + char + '.png'
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

# ==========================================
# EXAMPLE USAGE
# ==========================================
if __name__ == "__main__":
    # Define paths to your local .ttf or .otf font files
    # font_a = "/System/Library/Fonts/Supplemental/Arial.ttf"
    # font_b = "/System/Library/Fonts/Helvetica.ttc"

    # Shan font matching
    font_a = "static/fonts/Shan/hacked/SHAN.TTF"
    font_b = "static/fonts/Shan/unicode/NotoSansMyanmar-Regular.ttf"
    # Define what you are searching for
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = chr(0x61)
    
    # For Shan character matching
    candidate_pool = []
    for code in range(0x1000, 0x1080):
        candidate_pool.append(chr(code))
    try:
        match, confidence = find_best_match(target, font_a, font_b, candidate_pool)
        best_code_point = hex(ord(match))
        print(f"Target '{target}' in Font A best matches '{match}' ('{best_code_point}') in Font B.")
        print(f"Confidence Score (SSIM): {confidence:.4f}")
    except FileNotFoundError as e:
        print(e)
        print("[Notice] Please update the font paths with valid .ttf files on your system.")
