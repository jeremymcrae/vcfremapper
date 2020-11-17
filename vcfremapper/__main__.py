''' script to convert a VCF between coordinate systems
'''

import gzip
import sys
import tempfile
import argparse
from collections import defaultdict
import logging

from liftover import get_lifter
from pyfaidx import Fasta

from vcfremapper.vcf import VCF
from vcfremapper.remap import remap
from vcfremapper.sort_vcf import sort_vcf

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('vcf', nargs='?', default=sys.stdin.buffer)
    parser.add_argument('out', nargs='?', default=sys.stdout)
    parser.add_argument('--reference', required=True,
        help='path to reference genome, for the build being converted to.')
    parser.add_argument('--build-in', default='hg19', help='build to convert from')
    parser.add_argument('--build-out', default='hg38', help='build to convert to')
    parser.add_argument('--tempdir')
    
    return parser.parse_args()

def main():
    args = get_options()
    logging.basicConfig(format='%(asctime)s %(message)s')
    converter = get_lifter(args.build_in, args.build_out)
    genome = Fasta(args.reference, sequence_always_upper=True)
    
    vcf = VCF(gzip.open(args.vcf, 'rt'))
    temp = tempfile.NamedTemporaryFile('wt', suffix='.vcf', dir=args.tempdir)
    
    coords = defaultdict(dict)
    for var in vcf:
        # stash unaltered variant info, in case of errors
        chrom, pos, ref, alts = var.chrom, var.pos, var.ref, var.alts
        mapped = remap(converter, var, genome)
        if mapped is None:
            logging.warning('{}:{} {}->{}'.format(chrom, pos, ref, ','.join(alts)))
            continue
        
        # index the variants filepos, so we can quickly sort later
        coords[mapped.chrom][(mapped.pos, mapped.ref, tuple(mapped.alts))] = temp.tell()
        temp.write(str(mapped))
    
    temp.flush()
    prefixed = var.chrom.startswith('chr')
    try:
        sort_vcf(coords, temp, args.out, vcf.header)
    except (BrokenPipeError, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    main()
