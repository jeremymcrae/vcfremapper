
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

from vcfremapper.utils import prefix_chrom

transdict = maketrans('ACGTNacgtn*', 'TGCANtgcan*')
BASES = set(['A', 'C', 'G', 'T', 'N', '*', '.'])

def reverse(seq):
    ''' reverse a sequence
    '''
    return seq[::-1]

def complement(seq):
    ''' get the sequence complement
    '''
    return seq.translate(transdict)

def revcomp(seq):
    ''' reverse complement a sequence
    '''
    return reverse(complement(seq))

def check_reference(var, genome):
    ''' account for variants where the reference sequence has changed.
    
    This also requires GT, PL and AD fields, and various info fields to be
    adjusted, if present.
    '''
    
    _, chrom = prefix_chrom(var)
    
    end = var.pos + len(var.ref)
    ref_base = genome[chrom][var.pos:end].seq
    
    if ref_base == var.ref:
        return var
    
    if ref_base not in var.alts:
        return None
    
    idx = var.alts.index(ref_base)
    var.alts[idx] = var.ref
    var.ref = ref_base
    return var

def reverse_var(var, genome):
    ''' convert a variant that has changed strand
    '''
    
    if all(is_snv(var.ref, x) for x in var.alts):
        var = reverse_snv(var)
    elif len(var.alts) == 1 and is_indel(var.ref, var.alts[0]):
        var = reverse_indel(var, genome)
    elif is_cnv(var.ref, var.alts, var.info):
        var = reverse_cnv(var, genome)
    else:
        var = None
    
    if var is not None:
        var = check_reference(var, genome)
    
    return var

def reverse_snv(var):
    ''' reverse a SNV
    '''
    var.ref = revcomp(var.ref)
    var.alts = [revcomp(x) for x in var.alts]
    var.pos -= len(var.ref) - 1
    return var

def reverse_indel(var, genome):
    ''' reverse an indel (with only one alt allele)
    '''
    ref = revcomp(var.ref)
    alt = revcomp(var.alts[0])
    var.pos -= len(ref)
    _, chrom = prefix_chrom(var)
    
    if len(ref) > len(alt):  # handle deletions
        ref = ref[:-len(alt)]
        alt = genome[chrom][var.pos].seq
        ref = alt + ref
    elif len(alt) > len(ref):  # handle insertions
        alt = alt[:-len(ref)]
        ref = genome[chrom][var.pos].seq
        alt = ref + alt
    
    var.ref, var.alts = ref, [alt]
    
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
        (len(ref) == len(alt) and BASES.issuperset(set(alt) | set(ref)))

def is_indel(ref, alt):
    ''' check whether the ref and alt alleles are for an indel
    '''
    return (len(ref) > 1 or len(alt) > 1) and \
        (BASES.issuperset(set(alt) | set(ref)))

def is_cnv(ref, alt, info):
    return 'SVLEN' in info or 'DEL' in alt or 'DUP' in alt or 'INS' in alt
