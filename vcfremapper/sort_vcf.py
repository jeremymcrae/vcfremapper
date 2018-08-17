
import gzip

def sort_vcf(coords, handle, outpath, header, prefixed):
    ''' write a sorted VCF
    
    We previously indexed variant file offsets by chromosome and position, so we
    can sort variant coordinates, then pull out the variant line for a given
    position.
    
    Args:
        coords: index of variant positions by file offsets, as nested dict e.g.
            dict[chrom][pos] = offset
        handle: file handle for indexed file, where we know the variant offsets
        outpath: path to write VCF to (or writeable file handle)
        header: header lines for the output VCF
        prefixed: whether the chromosome strings are prefixed with 'chr'
    '''
    
    CHROMS = list(map(str, range(1, 23))) + ['X', 'Y', 'MT']
    if prefixed:
        CHROMS = [ 'chr{}'.format(x) for x in CHROMS ]
    
    seeker = open(handle.name, 'rt')
    
    try:
        output = open(outpath, 'wt')
    except TypeError:
        output = outpath
    
    output.writelines(header)
    for chrom in CHROMS:
        if chrom not in coords:
            continue
        
        for pos in sorted(coords[chrom]):
            seeker.seek(coords[chrom][pos])
            output.write(seeker.readline())
