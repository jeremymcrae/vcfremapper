
def prefix_chrom(var):
    ''' add "chr" prefix to chrom if absent. Also show whether prefix in initial
    '''
    prefixed = var.chrom.startswith('chr')
    chrom = var.chrom if prefixed else 'chr{}'.format(var.chrom)
    
    return prefixed, chrom
