
import unittest

from vcfremapper.variant import Variant
from vcfremapper.info import Info
from vcfremapper.samples import Samples

class TestVariant(unittest.TestCase):
    ''' test Variant class
    '''
    
    def test_variant_init(self):
        ''' check initialising a Variant
        '''
        
        line = '1\t100\t.\tA\tG\t.\t.\tAC=100\n'
        var = Variant(line)
        
        self.assertEqual(var.chrom, '1')
        self.assertEqual(var.pos, 100)
        self.assertEqual(var.ref, 'A')
        self.assertEqual(var.ref, 'A')
        self.assertEqual(var.alts, ['G'])
        self.assertIsInstance(var.info, Info)
        self.assertEqual(var.info, Info('AC=100'))
        self.assertIsNone(var.samples)
        
        self.assertEqual(str(var), line)
    
    def test_variant_multiallelic(self):
        ''' check initialising a multiallelic Variant
        '''
        
        line = '1\t100\t.\tA\tG,C\t.\t.\tAC=100\n'
        var = Variant(line)
        self.assertEqual(var.alts, ['G', 'C'])
    
    def test_variant_with_samples(self):
        ''' check that we can construct a Variant with sample data
        '''
        
        line = '1\t100\t.\tA\tG\t.\t.\tAD=100\tGT:PL\t1/1:80,9,2\n'
        var = Variant(line)
        
        self.assertIsInstance(var.samples, Samples)
        self.assertEqual(str(var), line)
        
        # check it works for variants with multiple samples
        line = '1\t100\t.\tA\tG\t.\t.\tAC=9\tGT:PL\t1/1:80,9,2\t0/1:9,1,1\n'
        var = Variant(line)
        self.assertEqual(str(var), line)
    
    def test_variant_alts(self):
        ''' check we can set a variant alt alleles
        '''
        
        line = '1\t100\t.\tA\tG\t.\t.\tAC=100\n'
        var = Variant(line)
        
        var.alts = 'G,C'
        self.assertEqual(var.alts, ['G', 'C'])
        
        var.alts = ['G', 'T']
        self.assertEqual(var.alts, ['G', 'T'])
        
        var.alts = 'G'
        self.assertEqual(var.alts, ['G'])
