

import unittest
from vcfremapper.utils import prefix_chrom

class TestUtils(unittest.TestCase):
    ''' test utils functions
    '''
    
    class Var:
        pass
    
    def test_prefix_chrom(self):
        var = self.Var()
        var.chrom = '1'
        
        prefixed, chrom = prefix_chrom(var)
        
        self.assertFalse(prefixed)
        self.assertEqual(chrom, 'chr1')
    
    def test_prefix_chrom_existing(self):
        var = self.Var()
        var.chrom = 'chr1'
        
        prefixed, chrom = prefix_chrom(var)
        
        self.assertTrue(prefixed)
        self.assertEqual(chrom, 'chr1')
