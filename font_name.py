from fontTools.ttLib import TTFont

# Load your font file (supports .ttf, .otf, .woff, .woff2)
font = TTFont("static/fonts/nv/hacked/Timenrn_.ttf")

# Access the 'name' table
name_table = font["name"]

# Get standard name IDs:
# nameID 1 = Font Family Name
# nameID 4 = Full Font Name
family_name = name_table.getDebugName(1)
full_name = name_table.getDebugName(4)

print(f"Family Name: {family_name}")
print(f"Full Name: {full_name}")
