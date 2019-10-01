
from vcfremapper.revcomp import reverse_var
from vcfremapper import CHROMS
from vcfremapper.utils import prefix_chrom

def get_new_coords(converter, chrom, pos):
    ''' find the remapped chrom, position and strand
    '''
    # try at the given site, but use zero-indexed position
    converted = converter[chrom][pos-1]
    if converted == []:
        raise ValueError("can't convert {}:{}".format(chrom, pos))
    
    return converted[0][:3]

def remap(converter, var, genome):
    ''' converts variant coordinates between genome versions
    
    Args:
        converter: pyLiftover.LiftOver object, for the from and to genome builds
        var: variant to be converted
        genome: pyfaidx.Fasta object for reference genome being converted to
    '''
    prefixed, chrom = prefix_chrom(var)
    
    try:
        chrom, pos, strand = get_new_coords(converter, chrom, var.pos)
    except ValueError:
        return None
    
    if not prefixed:
        chrom = chrom.strip('chr')
    
    if chrom not in CHROMS:
        return None
    
    # set updated coords, and convert back from 0-indexed position
    var.chrom = chrom
    var.pos = pos
    
    if strand == '-':
        var = reverse_var(var, genome)
    
    if var is not None:
        var.pos += 1
    return var
