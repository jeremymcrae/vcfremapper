''' script to convert a VCF between coordinate systems
'''

import gzip
import os
import sys
import tempfile
import argparse
from collections import defaultdict

from pyliftover import LiftOver

from vcfremapper.vcf import VCF
from vcfremapper.remap import remap
from vcfremapper.sort_vcf import sort_vcf

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('vcf', nargs='?', default=sys.stdin.buffer)
    parser.add_argument('out', nargs='?', default=sys.stdout)
    parser.add_argument('--build-in', default='hg19', help='build to convert from')
    parser.add_argument('--build-out', default='hg38', help='build to convert to')
    parser.add_argument('--tempdir', default='/scratch')
    
    return parser.parse_args()

def main():
    args = get_options()
    converter = LiftOver(args.build_in, args.build_out)
    
    vcf = VCF(gzip.open(args.vcf, 'rt'))
    temp = tempfile.TemporaryFile('wt', dir=args.tempdir)
    
    coords = defaultdict(dict)
    for var in vcf:
        mapped = remap(converter, var)
        if mapped is None:
            continue
        
        # index the variants filepos, so we can quickly sort later
        coords[mapped.chrom][mapped.pos] = temp.tell()
        temp.write(str(mapped))
    
    prefixed = var.chrom.startswith('chr')
    try:
        sort_vcf(coords, temp, args.out, vcf.header, prefixed)
    except (BrokenPipeError, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    main()
