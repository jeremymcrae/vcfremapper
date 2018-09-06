

import unittest
import tempfile
import os
import gzip
import shutil

from pyfaidx import Faidx

class get_options(object):
    ''' class to override get_otions from vcfremapper.__main__
    '''
    build_in = 'hg19'
    build_out = 'hg38'
    @classmethod
    def set_attr(cls, key, value):
        setattr(cls, key, value)

# awkwardly overrides the get_options function in vcfremapper.__main__, to
# give default arguments for 'main()'
import vcfremapper.__main__
vcfremapper.__main__.get_options = get_options
from vcfremapper.__main__ import main

class TestMain(unittest.TestCase):
    ''' test main script
    '''
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()

        # create a fasta file
        cls.fa = os.path.join(cls.dir, 'genome.fa')
        with open(cls.fa, mode='wt') as handle:
            handle.write('>chr1\n')
            handle.write('ACTGATGCTAGCTAGTATCTGACTCAGTAGCTCGAT\n')

        # index the fasta file
        fai = Faidx(cls.fa)
        fai.close()

        # set the final args that depend on the temp directory
        get_options.set_attr('tempdir', cls.dir)
        get_options.set_attr('reference', cls.fa)

        outvcf = os.path.join(cls.dir, 'out.vcf.gz')
        invcf = os.path.join(cls.dir, 'in.vcf.gz')
        get_options.set_attr('vcf', invcf)
        get_options.set_attr('out', outvcf)

        # write a VCF to be converted. This includes one variant which cannot be
        # converted. TODO: make a unit test to check for expected log output for
        # unconvertible variant
        with gzip.open(invcf, 'wt') as handle:
            handle.write('##fileformat=VCFv4.1\n' \
                '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n' \
                '1\t10\t.\tT\tG\t100\tPASS\tAC=100\n' \
                '1\t1000000\t.\tT\tG\t100\tPASS\tAC=100\n' \
                '1\t2000000\t.\tA\tG\t100\tPASS\tAC=100\n')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir)

    def test_main(self):
        ''' check that main works correctly
        '''

        main()
        with open(get_options.out, 'rt') as handle:
            data = handle.readlines()

        self.assertEqual(data, ['##fileformat=VCFv4.1\n',
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n',
            '1\t1064620\t.\tT\tG\t100\tPASS\tAC=100\n',
            '1\t2068561\t.\tA\tG\t100\tPASS\tAC=100\n'])
