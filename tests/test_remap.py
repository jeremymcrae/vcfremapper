
import unittest

# from pyfaidx import Fasta
from pyliftover import LiftOver

from vcfremapper.remap import get_new_coords, remap
from vcfremapper.variant import Variant

class TestRemap(unittest.TestCase):
    ''' test remapping functions
    '''
    
    @classmethod
    def setUpClass(cls):
        cls.lift = LiftOver('hg19', 'hg38')

    def test_get_new_coords(self):
        ''' check getting new coordinates for a variant
        '''

        data = get_new_coords(self.lift, 'chr1', 1000000)
        self.assertEqual(data, ('chr1', 1064619, '+'))

        # check a pos which swaps strand
        data = get_new_coords(self.lift, 'chr1', 317720)
        self.assertEqual(data, ('chr1', 501616, '-'))
        
        # positions no longer in the new genome build raise errors
        with self.assertRaises(ValueError):
            get_new_coords(self.lift, 'chr1', 1)

        # unprefixed chromosomes can't be converted
        with self.assertRaises(TypeError):
            get_new_coords(self.lift, '1', 1000000)

    def test_remap(self):
        ''' check remapping a variant
        '''

        genome = None
        var = Variant('1\t1000000\t.\tA\tG\t100\tPASS\tAC=100\n')
        var = remap(self.lift, var, genome)
        self.assertEqual(var.chrom, '1')
        self.assertEqual(var.pos, 1064620)

    def test_remap_not_in_build(self):
        ''' check a variant where the position is not in the new build
        '''
        genome = None
        var = Variant('1\t1\t.\tA\tG\t100\tPASS\tAC=100\n')
        self.assertIsNone(remap(self.lift, var, genome))

    def test_remap_unknown_chrom(self):
        ''' check a variant where the variant maps to a non-standard chromosome
        '''
        genome = None
        var = Variant('1\t13027995\t.\tA\tG\t100\tPASS\tAC=100\n')
        self.assertIsNone(remap(self.lift, var, genome))
