import sys

from good_results_sgp import good_results_sgp
from preconverted_assamese import sgp_assamese_info

def assamese_convert_dictionary():
    # Get preconverted as dictionary of input to index
    preconv_to_unicode = {}
    num_dups = 0
    for precon in sgp_assamese_info:
        str_index = '%d' % precon[0]
        precon_data = precon[2]
        try:
            unicode_out = good_results_sgp[str_index]
            if precon[2] in preconv_to_unicode:
                num_dups += 1
            preconv_to_unicode[precon[2]] = unicode_out
        except:
            preconv_to_unicode[precon[2]] = None
            
        print('%s : %s' % (precon[0] ,preconv_to_unicode[precon_data]))
    print('%d duplicates found' % num_dups)
    return preconv_to_unicode

def main(args):
    conversion_dict = assamese_convert_dictionary()

    print(conversion_dict)

    
if __name__ == "__main__":
    main(sys.argv)
