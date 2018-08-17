
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

transdict = maketrans('ACGTNacgtn*', 'TGCANtgcan*')

def revcomp(seq):
    ''' reverse complement a sequence
    '''
    return seq.translate(transdict)[::-1]
