
from vcfremapper.revcomp import reverse_var
from vcfremapper import CHROMS
from vcfremapper.utils import prefix_chrom

def get_new_coords(converter, chrom, pos):
    ''' find the remapped chrom, position and strand
    '''
    # try at the given site
    offset = 0
    converted = converter.convert_coordinate(chrom, pos)
    if converted == []:
        # try offset by one. Unclear why it works at one site, but not 1 bp away
        offset = 1
        converted = converter.convert_coordinate(chrom, pos + 1)
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
        var.chrom, var.pos, strand = get_new_coords(converter, chrom, var.pos)
    except ValueError:
        return None
    
    if not prefixed:
        var.chrom = var.chrom.strip('chr')
    
    if var.chrom not in CHROMS:
        return None
    
    if strand == '-':
        var = reverse_var(var, genome)
    
    return var
