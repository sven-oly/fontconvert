import icu

def get_all_unicode_blocks():
    block_ranges = {}
    current_block = None
    start_cp = 0
    
    # Iterate through the valid Unicode space (up to 0x10FFFF)
    for cp in range(0x110000):
        # icu APIs accept the character string or integer code points
        block_enum = icu.Char.getIntPropertyValue(cp, icu.UProperty.BLOCK)
        
        if block_enum != current_block:
            if current_block is not None:
                # Save previous block details
                block_name = icu.Char.getPropertyValueName(icu.UProperty.BLOCK, current_block, icu.UPropertyNameChoice.LONG_PROPERTY_NAME)
                block_ranges[block_name] = (hex(start_cp), hex(cp - 1))
            
            start_cp = cp
            current_block = block_enum

    # Capture the last remaining block
    if current_block is not None:
        block_name = icu.Char.getPropertyValueName(icu.UProperty.BLOCK, current_block, icu.UPropertyNameChoice.LONG_PROPERTY_NAME)
        block_ranges[block_name] = (hex(start_cp), hex(0x10FFFF))
        
    return block_ranges

# Example usage
ranges = get_all_unicode_blocks()
print(f"Basic Latin Range: {ranges.get('Basic_Latin')}") 
# Output: Basic Latin Range: ('0x0', '0x7f')
