# Test Adlam and Latin conversions round tripping

import ff_sample_text
import adlamConversion

import difflib
import sys

def compareLatin(l0, l1):
    print('l0: %s' % l0)
    print('l1: %s' % l1)

    d = difflib.ndiff(l0, l1)
    print(''.join(d), end="")
    #sys.stdout.writelines(d)

def compareAdlam(al0, a1):
    # Convert differences to hex?
    return

def roundTripALA(converter):
    # Get Latin text
    latin0 = ff_sample_text.kaalden_latin_text0
    adlam0 = ff_sample_text.kaalden_adlam_text0

    adlam1 = converter.convertText(latin0,
                                   fontIndex=adlamConversion.LATIN2ADLAM)
    #print('ADLAM1 = %s' % adlam1)
    #compareAdlam(adlam0, aadlam1)

    # get Adlam text
    latin1 = converter.convertText(adlam0,
                                   fontIndex=adlamConversion.ADLAM2LATIN)
    #print('LATIN1 = %s' % latin1)

    # Compare latin0 and latin1
    compareLatin(latin0, latin1)
    # Compare adlam0 and adlam1

    adlam2 = converter.convertText(latin1,
                                   fontIndex=adlamConversion.LATIN2ADLAM)
    #print('ADLAM2 = %s' % adlam2)

    # convert back to Latin
    latin2 = converter.convertText(adlam2,
                                   fontIndex=adlamConversion.ADLAM2LATIN)

    #print('LATIN2 = %s' % latin2)
    # compare them
    return

def main(argv):
    converter = adlamConversion.AdlamConverter()
    roundTripALA(converter)

if __name__ == '__main__':
  main(sys.argv)
