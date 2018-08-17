
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

from vcfremapper.utils import prefix_chrom

transdict = maketrans('ACGTNacgtn*', 'TGCANtgcan*')
BASES = set(['A', 'C', 'G', 'T', 'N', '*'])

def revcomp(seq):
    ''' reverse complement a sequence
    '''
    return seq.translate(transdict)[::-1]

def reverse_var(var, genome):
    ''' convert a variant that has changed strand
    '''
    var.pos += 2
    var.ref = revcomp(var.ref)
    
    if all(is_snv(var.ref, x) for x in var.alts):
        var = reverse_snv(var)
    elif len(var.alts) == 1 and is_indel(var.ref, var.alts[0]):
        reverse_indel(var, genome)
    elif is_cnv(var.ref, var.alts, var.info):
        reverse_cnv(var, genome)
    
    # TODO: account for variants where the reference sequence has changed. This
    # TODO: also requires GT, PL and AD fields, and various info fields to be
    # TODO: adjusted, if present.
    
    return var

def reverse_snv(var):
    ''' reverse a SNV
    '''
    var.alts = [ revcomp(x) for x in var.alts ]
    return var

def reverse_indel(var, genome):
    ''' reverse an indel (with only one alt allele)
    '''
    
    ref, alt = var.ref, var.alts[0]
    var.pos -= len(ref)
    alt = revcomp(alt)
    _, chrom = prefix_chrom(var)
    
    if len(ref) > len(alt):  # handle deletions
        ref = ref.rstrip(alt)
        alt = genome[chrom][var.pos].seq
        ref = alt + ref
    elif len(alt) > len(ref):  # handle insertions
        alt = alt.rstrip(ref)
        ref = genome[chrom][var.pos].seq
        alt = ref + alt
    
    var.ref, var.alt = ref, alt
    
    # TODO: reject indels spanning multiple mapping regions. We could remap the
    # TODO: start position, then add the length to get a predicted end position.
    # TODO: Then check if this is different from an end position determined by
    # TODO: getting an original end position, then remapping.
    
    return var

def reverse_cnv(var, genome):
    ''' reverse a CNV
    '''
    _, chrom = prefix_chrom(var)
    var.pos -= int(var.info['SVLEN'])
    var.ref = genome[chrom][var.pos].seq
    
    # TODO: reject CNVs spanning multiple mapping regions
    
    return var

def is_snv(ref, alt):
    ''' check whether the ref and alt alleles are for a SNV
    '''
    return (len(ref) == 1 and len(alt) == 1) or \
        (len(ref) == len(alt) and set(ref) in BASES and set(alt) in bases)

def is_indel(ref, alt):
    ''' check whether the ref and alt alleles are for an indel
    '''
    return len(ref) > 1 or len(alt) > 1 and \
        (set(ref) in BASES and set(alt) in bases)

def is_cnv(ref, alt, info):
    return 'SVLEN' in info
