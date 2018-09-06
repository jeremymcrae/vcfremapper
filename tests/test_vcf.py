
import unittest

from vcfremapper.vcf import VCF
from vcfremapper.variant import Variant

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

class TestVcf(unittest.TestCase):
    ''' test VCF class
    '''
    
    def setUp(self):
        self.handle = StringIO('##fileformat=VCFv4.1\n' \
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n' \
            '1\t100\t.\tA\tG\t100\tPASS\tAC=100\n')
        
    
    def test_vcf__init__(self):
        ''' check initialising a VCF
        '''
        
        vcf = VCF(self.handle)
        self.assertEqual(list(vcf.header), \
            ['##fileformat=VCFv4.1\n',
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'])
    
    def test_vcf__iter__(self):
        vcf = VCF(self.handle)
        var = next(vcf)
        
        self.assertEqual(str(var), '1\t100\t.\tA\tG\t100\tPASS\tAC=100\n')
        
        # check for StopIteration at end of file
        with self.assertRaises(StopIteration):
            next(vcf)
    
