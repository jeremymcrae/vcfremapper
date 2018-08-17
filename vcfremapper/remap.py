
from vcfremapper.revcomp import revcomp

def remap(converter, var):
    ''' converts variant coordinates between genome versions
    '''
    prefixed = var.chrom.startswith('chr')
    chrom = var.chrom if prefixed else 'chr{}'.format(var.chrom)
    
    # try at the given site
    offset = 0
    converted = converter.convert_coordinate(chrom, var.pos)
    if converted == []:
        # try offset by one. Unclear why it works at one site, but not 1 bp away
        offset = 1
        converted = converter.convert_coordinate(chrom, var.pos + 1)
        if converted == []:
            return None
    
    var.chrom, var.pos, strand, _ = converted[0]
    if not prefixed:
        var.chrom = var.chrom.strip('chr')
    
    if strand == '-':
        var.pos += 2 # check 1: 324375
        var.ref = revcomp(var.ref)
        var.alts = [ revcomp(x) for x in var.alts ]
    
    return var
