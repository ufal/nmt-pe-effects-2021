#!/usr/bin/env python3
# PE, WMT0818
MT_BLEU = {
    'src': (0, 0),
    'ref': (100, 100),
    'm01': (25.35, 19.07),
    'm02': (31.61, 22.44),
    'm03': (33.09, 23.86),
    'm04': (33.63, 24.42),
    'm05': (35.22, 26.25),
    'm06': (35.68, 26.64),
    'm07': (36.58, 28.14),
    'm08': (36.41, 28.84),
    'm09': (37.40, 28.72),
    'm10': (37.44, 28.95),
    'm11': (37.37, 28.46),
    'google': (37.56, 26.06),
    'microsoft': (33.06, 26.30),
}

def pretty_mt_name(mt):
    # Online 1, Online 2
    if mt == 'microsoft':
        return 'MS'
    if mt == 'google':
        return 'GGLE'
    return mt.upper()


MAX_WORD_TIME = 20
MAX_SENT_TIME = MAX_WORD_TIME*20

def f1(x, y):
    return 0 if (x+y) == 0 else 2*x*y/(x+y)