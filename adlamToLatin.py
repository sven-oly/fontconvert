# -*- coding: utf-8 -*-

import re
import sys

#ADLaM to Latin	transliteration

class adlamToLatinConvert() :
    def __init__(self):
    
        self.adlam_to_latin_map = {
            "𞤀": 'A',
            "𞤢": 'a',
            "𞤀𞥄": 'AA',
            "𞤀𞥄": 'Aa',
            "𞤢𞥄": 'aa',
            "𞤄": 'B',
            "𞤦": 'b',
            "𞤄𞥆": 'BB',
            "𞤄𞥆": 'Bb',
            "𞤦𞥆": 'bb',
            "𞤇": 'Ɓ',
            "𞤩": 'ɓ',
            "𞤇𞥆": 'ƁƁ',
            "𞤇𞥆": 'Ɓɓ',
            "𞤩𞥆": 'ɓɓ',
            "𞤇": 'BH',
            "𞤇": 'Bh',
            "𞤇𞥆": 'BBH',
            "𞤇𞥆": 'Bbh',
            "𞤩": 'bh',
            "𞤩𞥆": 'bbh',
            "𞤕": 'C',
            "𞤷": 'c',
            "𞤕𞥆": 'CC',
            "𞤕𞥆": 'Cc',
            "𞤷𞥆": 'cc',
            "𞤁": 'D',
            "𞤣": 'd',
            "𞤁𞥆": 'DD',
            "𞤁𞥆": 'Dd',
            "𞤣𞥆": 'dd',
            "𞤍": ' Ɗ',
            "𞤯": 'ɗ',
            "𞤍𞥆": ' ƊƊ',
            "𞤍𞥆": ' Ɗɗ',
            "𞤯𞥆": 'ɗɗ',
            "𞤍": 'DH',
            "𞤯": 'dh',
            "𞤍𞥆": 'DDH',
            "𞤍𞥆": 'Ddh',
            "𞤯𞥆": 'ddh',
            "𞤉": 'E',
            "𞤫": 'e',
            "𞤉𞥅": 'EE',
            "𞤉𞥅": 'Ee',
            "𞤫𞥅": 'ee',
            "𞤊": 'F',
            "𞤬": 'f',
            "𞤊𞥆": 'FF',
            "𞤊𞥆": 'Ff',
            "𞤬𞥆": 'ff',
            "𞤘": 'G',
            "𞤺": 'g',
            "𞤘𞥆": 'GG',
            "𞤘𞥆": 'Gg',
            "𞤺𞥆": 'gg',
            "𞤞": 'GB',
            "𞥀": 'gb',
            "𞤞𞥆": 'GGB',
            "𞤞𞥆": 'Ggb',
            "𞥀𞥆": 'ggb',
            "𞤖": 'H',
            "𞤸": 'h',
            "𞤖𞥆": 'HH',
            "𞤖𞥆": 'Hh',
            "𞤸𞥆": 'hh',
            "𞤋": 'I',
            "𞤭": 'i',
            "𞤋𞥅": 'II',
            "𞤋𞥅": 'Ii',
            "𞤭𞥅": 'ii',
            "𞤔": 'J',
            "𞤶": 'j',
            "𞤔𞥆": 'JJ',
            "𞤔𞥆": 'Jj',
            "𞤶𞥆": 'jj',
            "𞤑": 'K',
            "𞤳": 'k',
            "𞤑𞥆": 'KK',
            "𞤑𞥆": 'Kk',
            "𞤳𞥆": 'kk',
            "𞤝": 'KH',
            "𞤿": 'kh',
            "𞤝𞥆": 'KKH',
            "𞤝𞥆": 'Kkh',
            "𞤿𞥆": 'kkh',
            "𞤝": 'X',
            "𞤿": 'x',
            "𞤝𞥆": 'XX',
            "𞤝𞥆": 'Xx',
            "𞤿𞥆": 'xx',
            "𞤂": 'L',
            "𞤤": 'l',
            "𞤂𞥆": 'LL',
            "𞤂𞥆": 'Ll',
            "𞤤𞥆": 'll',
            "𞤃": 'M',
            "𞤥": 'm',
            "𞤃𞥆": 'MM',
            "𞤃𞥆": 'Mm',
            "𞤥𞥆": 'mm',
            "𞤐": 'N',
            "𞤲": 'n',
            "𞤐𞥆": 'NN',
            "𞤐𞥆": 'Nn',
            "𞤲𞥆": 'nn',
            "𞤛": 'Ŋ',
            "𞤽": 'ŋ',
            "𞤛𞥆": 'ŊŊ',
            "𞤛𞥆": 'Ŋŋ',
            "𞤽𞥆": 'ŋŋ',
            "𞤛": 'NH',
            "𞤽": 'nh',
            "𞤛𞥆": 'NNH',
            "𞤛𞥆": 'Nnh',
            "𞤽𞥆": 'nnh',
            "𞤙": 'Ñ',
            "𞤻": 'ñ',
            "𞤙𞥆": 'ÑÑ',
            "𞤙𞥆": 'Ññ',
            "𞤻𞥆": 'ññ',
            "𞤙": 'NY',
            "𞤻": 'ny',
            "𞤙𞥆": 'NNY',
            "𞤙𞥆": 'Nny',
            "𞤻𞥆": 'nny',
            "𞤌": 'O',
            "𞤮": 'o',
            "𞤌𞥅": 'OO',
            "𞤌𞥅": 'Oo',
            "𞤮𞥅": 'oo',
            "𞤆": 'P',
            "𞤨": 'p',
            "𞤆𞥆": 'PP',
            "𞤆𞥆": 'Pp',
            "𞤨𞥆": 'pp',
            "𞤠": 'KP',
            "𞥂": 'kp',
            "𞤠𞥆": 'KKP',
            "𞤠𞥆": 'Kkp',
            "𞥂𞥆": 'kkp',
            "𞤗": 'Q',
            "𞤹": 'q',
            "𞤗𞥆": 'QQ',
            "𞤗𞥆": 'Qq',
            "𞤹𞥆": 'qq',
            "𞤗": 'GH',
            "𞤹": 'gh',
            "𞤗𞥆": 'GGH',
            "𞤗𞥆": 'Ggh',
            "𞤹𞥆": 'ggh',
            "𞤈": 'R',
            "𞤪": 'r',
            "𞤈𞥆": 'RR',
            "𞤈𞥆": 'Rr',
            "𞤪𞥆": 'rr',
            "𞤅": 'S',
            "𞤧": 's',
            "𞤅𞥆": 'SS',
            "𞤅𞥆": 'Ss',
            "𞤧𞥆": 'ss',
            "𞤡": 'SH',
            "𞥃": 'Sh',
            "𞤡𞥆": 'SSH',
            "𞤡𞥆": 'Ssh',
            "𞥃𞥆": 'ssh',
            "𞤚": 'T',
            "𞤼": 't',
            "𞤚𞥆": 'TT',
            "𞤚𞥆": 'Tt',
            "𞤼𞥆": 'tt',
            "𞤓": 'U',
            "𞤵": 'u',
            "𞤓𞥅": 'UU',
            "𞤓𞥅": 'Uu',
            "𞤵𞥅": 'uu',
            "𞤜": 'V',
            "𞤾": 'v',
            "𞤜𞥆": 'VV',
            "𞤜𞥆": 'Vv',
            "𞤾𞥆": 'vv',
            "𞤏": 'W',
            "𞤱": 'w',
            "𞤏𞥆": 'WW',
            "𞤏𞥆": 'Ww',
            "𞤱𞥆": 'ww',
            "𞤒": 'Y',
            "𞤴": 'y',
            "𞤒𞥆": 'YY',
            "𞤒𞥆": 'Yy',
            "𞤴𞥆": 'yy',
            "𞤎": 'Ƴ',
            "𞤰": 'ƴ',
            "𞤎𞥆": 'ƳƳ',
            "𞤎𞥆": 'Ƴƴ',
            "𞤰𞥆": 'ƴƴ',
            "𞤎": 'YH',
            "𞤰": 'yh',
            "𞤎𞥆": 'YYH',
            "𞤎𞥆": 'Yyh',
            "𞤰𞥆": 'yyh',
            "𞤟": 'Z',
            "𞥁": 'z',
            "𞤟𞥆": 'ZZ',
            "𞤟𞥆": 'Zz',
            "𞥁𞥆": 'zz',
            "𞤐'𞤁": 'ND',
            "𞤐'𞤁": 'Nd',
            "𞤲'𞤣": 'nd',
            "𞤐'𞤄": 'MB',
            "𞤐'𞤄": 'Mb',
            "𞤲'𞤦": 'mb',
            "𞤐'𞤔": 'NJ',
            "𞤐'𞤔": 'Nj',
            "𞤲'𞤶": 'nj',
            "𞤐'𞤘": 'NG',
            "𞤐'𞤘": 'Ng',
            "𞤲'𞤺": 'ng',
            "𞤲𞤣": 'nnd',
            "𞤥𞤦": 'mmb',
            "𞤲𞤶": 'nnj',
            "𞤲𞤺": 'nng',
            "𞥐": '0',
            "𞥑": '1',
            "𞥒": '2',
            "𞥓": '3',
            "𞥔": '4',
            "𞥕": '5',
            "𞥖": '6',
            "𞥗": '7',
            "𞥘": '8',
            "𞥙": '9',
            "!": '!',

    "𞤀𞤁𞤂𞤢𞤃": 'Laten',
            "𞤀𞥄𞤐𞤁": 'AAND',
            "𞤀𞥄𞤲𞤣": 'Aand',
            "𞤢𞥄𞤲𞤣": 'aand',
            "𞤀𞥄𞤐𞤄": 'AAMB',
            "𞤀𞥄𞤲𞤦": 'Aamb',
            "𞤢𞥄𞤲𞤦": 'aamb',
            "𞤀𞥄𞤐𞤔": 'AANJ',
            "𞤀𞥄𞤲𞤶": 'Aanj',
            "𞤢𞥄𞤲𞤶": 'aanj',
            "𞤀𞥄𞤐𞤘": 'AANG',
            "𞤀𞥄𞤲𞤺": 'Aang',
            "𞤢𞥄𞤲𞤺": 'aang',
            "𞤉𞥅𞤐𞤁": 'EEND',
            "𞤉𞥅𞤲𞤣": 'Eend',
            "𞤫𞥅𞤲𞤣": 'eend',
            "𞤉𞥅𞤐𞤄": 'EEMB',
            "𞤉𞥅𞤲𞤦": 'Eemb',
            "𞤫𞥅𞤲𞤦": 'eemb',
            "𞤉𞥅𞤐𞤔": 'EENJ',
            "𞤉𞥅𞤲𞤶": 'Eenj',
            "𞤫𞥅𞤲𞤶": 'eenj',
            "𞤉𞥅𞤐𞤘": 'EENG',
            "𞤉𞥅𞤲𞤺": 'Eeng',
            "𞤫𞥅𞤲𞤺": 'eeng',
            "𞤋𞥅𞤐𞤁": 'IIND',
            "𞤋𞥅𞤲𞤣": 'Iind',
            "𞤭𞥅𞤲𞤣": 'iind',
            "𞤋𞥅𞤐𞤄": 'IIMB',
            "𞤋𞥅𞤲𞤦": 'Iimb',
            "𞤭𞥅𞤲𞤦": 'iimb',
            "𞤋𞥅𞤐𞤔": 'IINJ',
            "𞤋𞥅𞤲𞤶": 'Iinj',
            "𞤭𞥅𞤲𞤶": 'iinj',
            "𞤋𞥅𞤐𞤘": 'IING',
            "𞤋𞥅𞤲𞤺": 'Iing',
            "𞤭𞥅𞤲𞤺": 'iing',
            "𞤌𞥅𞤐𞤁": 'OOND',
            "𞤌𞥅𞤲𞤣": 'Oond',
            "𞤮𞥅𞤲𞤣": 'oond',
            "𞤌𞥅𞤐𞤄": 'OOMB',
            "𞤌𞥅𞤲𞤦": 'Oomb',
            "𞤮𞥅𞤲𞤦": 'oomb',
            "𞤌𞥅𞤐𞤔": 'OONJ',
            "𞤌𞥅𞤲𞤶": 'Oonj',
            "𞤮𞥅𞤲𞤶": 'oonj',
            "𞤌𞥅𞤐𞤘": 'OONG',
            "𞤌𞥅𞤲𞤺": 'Oong',
            "𞤮𞥅𞤲𞤺": 'oong',
            "𞤓𞥅𞤐𞤁": 'UUND',
            "𞤓𞥅𞤲𞤣": 'Uund',
            "𞤵𞥅𞤲𞤣": 'uund',
            "𞤓𞥅𞤐𞤄": 'UUMB',
            "𞤓𞥅𞤲𞤦": 'Uumb',
            "𞤵𞥅𞤲𞤦": 'uumb',
            "𞤓𞥅𞤐𞤔": 'UUNJ',
            "𞤓𞥅𞤲𞤶": 'Uunj',
            "𞤵𞥅𞤲𞤶": 'uunj',
            "𞤓𞥅𞤐𞤘": 'UUNG',
            "𞤓𞥅𞤲𞤺": 'Uung',
            "𞤵𞥅𞤲𞤺": 'uung    ',

    "𞤐𞤁": 'ND',
            "𞤐𞤣": 'Nd',
            "𞤲𞤣": 'nd',
            "𞤐𞤄": 'MB',
            "𞤐𞤦": 'Mb',
            "𞤲𞤦": 'mb',
            "𞤐𞤔": 'NJ',
            "𞤐𞤶": 'Nj',
            "𞤲𞤶": 'nj',
            "𞤐𞤘": 'NG',
            "𞤐𞤺": 'Ng',
            "𞤲𞤺": 'ng    ',

    "𞥇": '-',
            "𞤢𞤢": 'a\'a',
            "𞤫𞤫": 'e\'e',
            "𞤭𞤭": 'i\'i',
            "𞤮𞤮": 'o\'o',
            "𞤵𞤵": 'u\'u',
            "𞤀𞤀": 'A\'a',
            "𞤉𞤉": 'E\'e',
            "𞤋𞤋": 'I\'i',
            "𞤌𞤌": 'O\'o',
            "𞤓𞤓": 'U\'u',
            "𞤀𞤀": 'A\'A',
            "𞤉𞤉": 'E\'E',
            "𞤋𞤋": 'I\'I',
            "𞤌𞤌": 'O\'O',
            "𞤓𞤓": 'U\'U    ',
        }

        # Using escaped characters
        self.regex_string = '\U0001E900\U0001E901\U0001E902\U0001E922\U0001E903|\U0001E900\U0001E944\U0001E910\U0001E901|\U0001E900\U0001E944\U0001E932\U0001E923|\U0001E922\U0001E944\U0001E932\U0001E923|\U0001E900\U0001E944\U0001E910\U0001E904|\U0001E900\U0001E944\U0001E932\U0001E926|\U0001E922\U0001E944\U0001E932\U0001E926|\U0001E900\U0001E944\U0001E910\U0001E914|\U0001E900\U0001E944\U0001E932\U0001E936|\U0001E922\U0001E944\U0001E932\U0001E936|\U0001E900\U0001E944\U0001E910\U0001E918|\U0001E900\U0001E944\U0001E932\U0001E93A|\U0001E922\U0001E944\U0001E932\U0001E93A|\U0001E909\U0001E945\U0001E910\U0001E901|\U0001E909\U0001E945\U0001E932\U0001E923|\U0001E92B\U0001E945\U0001E932\U0001E923|\U0001E909\U0001E945\U0001E910\U0001E904|\U0001E909\U0001E945\U0001E932\U0001E926|\U0001E92B\U0001E945\U0001E932\U0001E926|\U0001E909\U0001E945\U0001E910\U0001E914|\U0001E909\U0001E945\U0001E932\U0001E936|\U0001E92B\U0001E945\U0001E932\U0001E936|\U0001E909\U0001E945\U0001E910\U0001E918|\U0001E909\U0001E945\U0001E932\U0001E93A|\U0001E92B\U0001E945\U0001E932\U0001E93A|\U0001E90B\U0001E945\U0001E910\U0001E901|\U0001E90B\U0001E945\U0001E932\U0001E923|\U0001E92D\U0001E945\U0001E932\U0001E923|\U0001E90B\U0001E945\U0001E910\U0001E904|\U0001E90B\U0001E945\U0001E932\U0001E926|\U0001E92D\U0001E945\U0001E932\U0001E926|\U0001E90B\U0001E945\U0001E910\U0001E914|\U0001E90B\U0001E945\U0001E932\U0001E936|\U0001E92D\U0001E945\U0001E932\U0001E936|\U0001E90B\U0001E945\U0001E910\U0001E918|\U0001E90B\U0001E945\U0001E932\U0001E93A|\U0001E92D\U0001E945\U0001E932\U0001E93A|\U0001E90C\U0001E945\U0001E910\U0001E901|\U0001E90C\U0001E945\U0001E932\U0001E923|\U0001E92E\U0001E945\U0001E932\U0001E923|\U0001E90C\U0001E945\U0001E910\U0001E904|\U0001E90C\U0001E945\U0001E932\U0001E926|\U0001E92E\U0001E945\U0001E932\U0001E926|\U0001E90C\U0001E945\U0001E910\U0001E914|\U0001E90C\U0001E945\U0001E932\U0001E936|\U0001E92E\U0001E945\U0001E932\U0001E936|\U0001E90C\U0001E945\U0001E910\U0001E918|\U0001E90C\U0001E945\U0001E932\U0001E93A|\U0001E92E\U0001E945\U0001E932\U0001E93A|\U0001E913\U0001E945\U0001E910\U0001E901|\U0001E913\U0001E945\U0001E932\U0001E923|\U0001E935\U0001E945\U0001E932\U0001E923|\U0001E913\U0001E945\U0001E910\U0001E904|\U0001E913\U0001E945\U0001E932\U0001E926|\U0001E935\U0001E945\U0001E932\U0001E926|\U0001E913\U0001E945\U0001E910\U0001E914|\U0001E913\U0001E945\U0001E932\U0001E936|\U0001E935\U0001E945\U0001E932\U0001E936|\U0001E913\U0001E945\U0001E910\U0001E918|\U0001E913\U0001E945\U0001E932\U0001E93A|\U0001E935\U0001E945\U0001E932\U0001E93A|\U0001E910\u0027\U0001E901|\U0001E932\u0027\U0001E923|\U0001E910\u0027\U0001E904|\U0001E932\u0027\U0001E926|\U0001E910\u0027\U0001E914|\U0001E932\u0027\U0001E936|\U0001E910\u0027\U0001E918|\U0001E932\u0027\U0001E93A|\U0001E900\U0001E944|\U0001E922\U0001E944|\U0001E904\U0001E946|\U0001E926\U0001E946|\U0001E907\U0001E946|\U0001E929\U0001E946|\U0001E915\U0001E946|\U0001E937\U0001E946|\U0001E901\U0001E946|\U0001E923\U0001E946|\U0001E90D\U0001E946|\U0001E92F\U0001E946|\U0001E909\U0001E945|\U0001E92B\U0001E945|\U0001E90A\U0001E946|\U0001E92C\U0001E946|\U0001E918\U0001E946|\U0001E93A\U0001E946|\U0001E91E\U0001E946|\U0001E940\U0001E946|\U0001E916\U0001E946|\U0001E938\U0001E946|\U0001E90B\U0001E945|\U0001E92D\U0001E945|\U0001E914\U0001E946|\U0001E936\U0001E946|\U0001E911\U0001E946|\U0001E933\U0001E946|\U0001E91D\U0001E946|\U0001E93F\U0001E946|\U0001E902\U0001E946|\U0001E924\U0001E946|\U0001E903\U0001E946|\U0001E925\U0001E946|\U0001E910\U0001E946|\U0001E932\U0001E946|\U0001E91B\U0001E946|\U0001E93D\U0001E946|\U0001E919\U0001E946|\U0001E93B\U0001E946|\U0001E90C\U0001E945|\U0001E92E\U0001E945|\U0001E906\U0001E946|\U0001E928\U0001E946|\U0001E920\U0001E946|\U0001E942\U0001E946|\U0001E917\U0001E946|\U0001E939\U0001E946|\U0001E908\U0001E946|\U0001E92A\U0001E946|\U0001E905\U0001E946|\U0001E927\U0001E946|\U0001E921\U0001E946|\U0001E943\U0001E946|\U0001E91A\U0001E946|\U0001E93C\U0001E946|\U0001E913\U0001E945|\U0001E935\U0001E945|\U0001E91C\U0001E946|\U0001E93E\U0001E946|\U0001E90F\U0001E946|\U0001E931\U0001E946|\U0001E912\U0001E946|\U0001E934\U0001E946|\U0001E90E\U0001E946|\U0001E930\U0001E946|\U0001E91F\U0001E946|\U0001E941\U0001E946|\U0001E932\U0001E923|\U0001E925\U0001E926|\U0001E932\U0001E936|\U0001E932\U0001E93A|\U0001E910\U0001E901|\U0001E910\U0001E923|\U0001E910\U0001E904|\U0001E910\U0001E926|\U0001E932\U0001E926|\U0001E910\U0001E914|\U0001E910\U0001E936|\U0001E910\U0001E918|\U0001E910\U0001E93A|\U0001E922\U0001E922|\U0001E92B\U0001E92B|\U0001E92D\U0001E92D|\U0001E92E\U0001E92E|\U0001E935\U0001E935|\U0001E900\U0001E900|\U0001E909\U0001E909|\U0001E90B\U0001E90B|\U0001E90C\U0001E90C|\U0001E913\U0001E913|\U0001E900|\U0001E922|\U0001E904|\U0001E926|\U0001E907|\U0001E929|\U0001E915|\U0001E937|\U0001E901|\U0001E923|\U0001E90D|\U0001E92F|\U0001E909|\U0001E92B|\U0001E90A|\U0001E92C|\U0001E918|\U0001E93A|\U0001E91E|\U0001E940|\U0001E916|\U0001E938|\U0001E90B|\U0001E92D|\U0001E914|\U0001E936|\U0001E911|\U0001E933|\U0001E91D|\U0001E93F|\U0001E902|\U0001E924|\U0001E903|\U0001E925|\U0001E910|\U0001E932|\U0001E91B|\U0001E93D|\U0001E919|\U0001E93B|\U0001E90C|\U0001E92E|\U0001E906|\U0001E928|\U0001E920|\U0001E942|\U0001E917|\U0001E939|\U0001E908|\U0001E92A|\U0001E905|\U0001E927|\U0001E921|\U0001E943|\U0001E91A|\U0001E93C|\U0001E913|\U0001E935|\U0001E91C|\U0001E93E|\U0001E90F|\U0001E931|\U0001E912|\U0001E934|\U0001E90E|\U0001E930|\U0001E91F|\U0001E941|\U0001E950|\U0001E951|\U0001E952|\U0001E953|\U0001E954|\U0001E955|\U0001E956|\U0001E957|\U0001E958|\U0001E959|\u0021|\U0001E947'

        self.adlam_split_regex = re.compile(self.regex_string)
        
        self. AllAdlamToLatin="""𞤀	A
𞤢	a
𞤀𞥄	AA
𞤀𞥄	Aa
𞤢𞥄	aa
𞤄	B
𞤦	b
𞤄𞥆	BB
𞤄𞥆	Bb
𞤦𞥆	bb
𞤇	Ɓ
𞤩	ɓ
𞤇𞥆	ƁƁ
𞤇𞥆	Ɓɓ
𞤩𞥆	ɓɓ
𞤇	BH
𞤇	Bh
𞤇𞥆	BBH
𞤇𞥆	Bbh
𞤩	bh
𞤩𞥆	bbh
𞤕	C
𞤷	c
𞤕𞥆	CC
𞤕𞥆	Cc
𞤷𞥆	cc
𞤁	D
𞤣	d
𞤁𞥆	DD
𞤁𞥆	Dd
𞤣𞥆	dd
𞤍	 Ɗ
𞤯	ɗ
𞤍𞥆	 ƊƊ
𞤍𞥆	 Ɗɗ
𞤯𞥆	ɗɗ
𞤍	DH
𞤯	dh
𞤍𞥆	DDH
𞤍𞥆	Ddh
𞤯𞥆	ddh
𞤉	E
𞤫	e
𞤉𞥅	EE
𞤉𞥅	Ee
𞤫𞥅	ee
𞤊	F
𞤬	f
𞤊𞥆	FF
𞤊𞥆	Ff
𞤬𞥆	ff
𞤘	G
𞤺	g
𞤘𞥆	GG
𞤘𞥆	Gg
𞤺𞥆	gg
𞤞	GB
𞥀	gb
𞤞𞥆	GGB
𞤞𞥆	Ggb
𞥀𞥆	ggb
𞤖	H
𞤸	h
𞤖𞥆	HH
𞤖𞥆	Hh
𞤸𞥆	hh
𞤋	I
𞤭	i
𞤋𞥅	II
𞤋𞥅	Ii
𞤭𞥅	ii
𞤔	J
𞤶	j
𞤔𞥆	JJ
𞤔𞥆	Jj
𞤶𞥆	jj
𞤑	K
𞤳	k
𞤑𞥆	KK
𞤑𞥆	Kk
𞤳𞥆	kk
𞤝	KH
𞤿	kh
𞤝𞥆	KKH
𞤝𞥆	Kkh
𞤿𞥆	kkh
𞤝	X
𞤿	x
𞤝𞥆	XX
𞤝𞥆	Xx
𞤿𞥆	xx
𞤂	L
𞤤	l
𞤂𞥆	LL
𞤂𞥆	Ll
𞤤𞥆	ll
𞤃	M
𞤥	m
𞤃𞥆	MM
𞤃𞥆	Mm
𞤥𞥆	mm
𞤐	N
𞤲	n
𞤐𞥆	NN
𞤐𞥆	Nn
𞤲𞥆	nn
𞤛	Ŋ
𞤽	ŋ
𞤛𞥆	ŊŊ
𞤛𞥆	Ŋŋ
𞤽𞥆	ŋŋ
𞤛	NH
𞤽	nh
𞤛𞥆	NNH
𞤛𞥆	Nnh
𞤽𞥆	nnh
𞤙	Ñ
𞤻	ñ
𞤙𞥆	ÑÑ
𞤙𞥆	Ññ
𞤻𞥆	ññ
𞤙	NY
𞤻	ny
𞤙𞥆	NNY
𞤙𞥆	Nny
𞤻𞥆	nny
𞤌	O
𞤮	o
𞤌𞥅	OO
𞤌𞥅	Oo
𞤮𞥅	oo
𞤆	P
𞤨	p
𞤆𞥆	PP
𞤆𞥆	Pp
𞤨𞥆	pp
𞤠	KP
𞥂	kp
𞤠𞥆	KKP
𞤠𞥆	Kkp
𞥂𞥆	kkp
𞤗	Q
𞤹	q
𞤗𞥆	QQ
𞤗𞥆	Qq
𞤹𞥆	qq
𞤗	GH
𞤹	gh
𞤗𞥆	GGH
𞤗𞥆	Ggh
𞤹𞥆	ggh
𞤈	R
𞤪	r
𞤈𞥆	RR
𞤈𞥆	Rr
𞤪𞥆	rr
𞤅	S
𞤧	s
𞤅𞥆	SS
𞤅𞥆	Ss
𞤧𞥆	ss
𞤡	SH
𞥃	Sh
𞤡𞥆	SSH
𞤡𞥆	Ssh
𞥃𞥆	ssh
𞤚	T
𞤼	t
𞤚𞥆	TT
𞤚𞥆	Tt
𞤼𞥆	tt
𞤓	U
𞤵	u
𞤓𞥅	UU
𞤓𞥅	Uu
𞤵𞥅	uu
𞤜	V
𞤾	v
𞤜𞥆	VV
𞤜𞥆	Vv
𞤾𞥆	vv
𞤏	W
𞤱	w
𞤏𞥆	WW
𞤏𞥆	Ww
𞤱𞥆	ww
𞤒	Y
𞤴	y
𞤒𞥆	YY
𞤒𞥆	Yy
𞤴𞥆	yy
𞤎	Ƴ
𞤰	ƴ
𞤎𞥆	ƳƳ
𞤎𞥆	Ƴƴ
𞤰𞥆	ƴƴ
𞤎	YH
𞤰	yh
𞤎𞥆	YYH
𞤎𞥆	Yyh
𞤰𞥆	yyh
𞤟	Z
𞥁	z
𞤟𞥆	ZZ
𞤟𞥆	Zz
𞥁𞥆	zz
𞤐'𞤁	ND
𞤐'𞤁	Nd
𞤲'𞤣	nd
𞤐'𞤄	MB
𞤐'𞤄	Mb
𞤲'𞤦	mb
𞤐'𞤔	NJ
𞤐'𞤔	Nj
𞤲'𞤶	nj
𞤐'𞤘	NG
𞤐'𞤘	Ng
𞤲'𞤺	ng
𞤲𞤣	nnd
𞤥𞤦	mmb
𞤲𞤶	nnj
𞤲𞤺	nng
𞥐	0
𞥑	1
𞥒	2
𞥓	3
𞥔	4
𞥕	5
𞥖	6
𞥗	7
𞥘	8
𞥙	9
!	!
𞥞	!
?	?
𞥟	?
⹁	,
⁏	;
.	.
𞤀𞥄𞤐𞤁	AAND
𞤀𞥄𞤲𞤣	Aand
𞤢𞥄𞤲𞤣	aand
𞤀𞥄𞤐𞤄	AAMB
𞤀𞥄𞤲𞤦	Aamb
𞤢𞥄𞤲𞤦	aamb
𞤀𞥄𞤐𞤔	AANJ
𞤀𞥄𞤲𞤶	Aanj
𞤢𞥄𞤲𞤶	aanj
𞤀𞥄𞤐𞤘	AANG
𞤀𞥄𞤲𞤺	Aang
𞤢𞥄𞤲𞤺	aang
𞤉𞥅𞤐𞤁	EEND
𞤉𞥅𞤲𞤣	Eend
𞤫𞥅𞤲𞤣	eend
𞤉𞥅𞤐𞤄	EEMB
𞤉𞥅𞤲𞤦	Eemb
𞤫𞥅𞤲𞤦	eemb
𞤉𞥅𞤐𞤔	EENJ
𞤉𞥅𞤲𞤶	Eenj
𞤫𞥅𞤲𞤶	eenj
𞤉𞥅𞤐𞤘	EENG
𞤉𞥅𞤲𞤺	Eeng
𞤫𞥅𞤲𞤺	eeng
𞤋𞥅𞤐𞤁	IIND
𞤋𞥅𞤲𞤣	Iind
𞤭𞥅𞤲𞤣	iind
𞤋𞥅𞤐𞤄	IIMB
𞤋𞥅𞤲𞤦	Iimb
𞤭𞥅𞤲𞤦	iimb
𞤋𞥅𞤐𞤔	IINJ
𞤋𞥅𞤲𞤶	Iinj
𞤭𞥅𞤲𞤶	iinj
𞤋𞥅𞤐𞤘	IING
𞤋𞥅𞤲𞤺	Iing
𞤭𞥅𞤲𞤺	iing
𞤌𞥅𞤐𞤁	OOND
𞤌𞥅𞤲𞤣	Oond
𞤮𞥅𞤲𞤣	oond
𞤌𞥅𞤐𞤄	OOMB
𞤌𞥅𞤲𞤦	Oomb
𞤮𞥅𞤲𞤦	oomb
𞤌𞥅𞤐𞤔	OONJ
𞤌𞥅𞤲𞤶	Oonj
𞤮𞥅𞤲𞤶	oonj
𞤌𞥅𞤐𞤘	OONG
𞤌𞥅𞤲𞤺	Oong
𞤮𞥅𞤲𞤺	oong
𞤓𞥅𞤐𞤁	UUND
𞤓𞥅𞤲𞤣	Uund
𞤵𞥅𞤲𞤣	uund
𞤓𞥅𞤐𞤄	UUMB
𞤓𞥅𞤲𞤦	Uumb
𞤵𞥅𞤲𞤦	uumb
𞤓𞥅𞤐𞤔	UUNJ
𞤓𞥅𞤲𞤶	Uunj
𞤵𞥅𞤲𞤶	uunj
𞤓𞥅𞤐𞤘	UUNG
𞤓𞥅𞤲𞤺	Uung
𞤵𞥅𞤲𞤺	uung
𞤐𞤁	ND
𞤐𞤣	Nd
𞤲𞤣	nd
𞤐𞤄	MB
𞤐𞤦	Mb
𞤲𞤦	mb
𞤐𞤔	NJ
𞤐𞤶	Nj
𞤲𞤶	nj
𞤐𞤘	NG
𞤐𞤺	Ng
𞤲𞤺	ng
𞥇	-
𞤢𞤢	a\'a
𞤫𞤫	e\'e
𞤭𞤭	i\'i
𞤮𞤮	o\'o
𞤵𞤵	u\'u
𞤀𞤀	A\'a
𞤉𞤉	E\'e
𞤋𞤋	I\'i
𞤌𞤌	O\'o
𞤓𞤓	U\'u
𞤀𞤀	A\'A
𞤉𞤉	E\'E
𞤋𞤋	I\'I
𞤌𞤌	O\'O
𞤓𞤓	U\'U
"""

    def allTo2Maps(self):
        # Generates two AdlamToLatin mappings, one for ASCII mapping and another
        # for mappings using non-ASCII latin characters
        self.ascii_map = {}
        nonascii_results = []
        rex = re.compile(r'\t')
        i = 1
        for line in self.AllAdlamToLatin.split('\n'):
            result = line.split('\t') # rex.split(line)
            # print('%3d %s' % (i, result))
            if len(result) < 2:
                continue
            self.ascii_map[result[0]] = result[1]
            new_val = result[1].encode("ascii", "ignore")
            if new_val.decode() != result[1]:
                # Contains non-ASCII letters
                # print('different: %s', result)
                nonascii_results.append(result)
                i += 1
              
        # Replace those for non-ascii output
        self.nonascii_map = self.ascii_map
        for result in nonascii_results:
            self.nonascii_map[result[0]] = result[1]

    
def revRegEx():
    # The order is correct.
    # However, both ASCII and non-ASCII Latin representation
     a2l =adlamToLatinConvert()
     s = a2l.regex_string.split('|')
     s_sort = sorted(s, key=lambda x : len(x), reverse=True)
     print(s_sort)
     print

def nonLatin():
     a2l =adlamToLatinConvert()
     items =a2l.adlam_to_latin_map.items()
     for item in items:
         print(item)
         val = item[1]
         new_val =item[1].encode("ascii", "ignore")
         updated_str = new_val.decode()
         if val != updated_str:
             print('NON-ASCII: %s -> %s' % (val, updated_str))

def printKeys(argv):
    keys = adlam_to_latin_map.keys()
    k_U = []
    for k in keys:
        chs = [str('\\U%08x' % ord(c)) for c in [k]]  # c in k.split()]
        k_U.append(chs)
    print(k_U)
    keys_sorted = sorted(keys, key=lambda x: len(x), reverse=True)
    print(keys_sorted)
    print('|'.join(keys_sorted))

def main(arg):
    a2l =adlamToLatinConvert()
    a2l.allTo2Maps()
    # nonLatin()
    #revRegEx()
    return

if __name__ == '__main__':
  main(sys.argv)

