

import unittest
from vcfremapper.revcomp import revcomp, reverse_var, reverse_snv, reverse_indel, \
    reverse_cnv, is_snv, is_indel, is_cnv

class TestReverse(unittest.TestCase):
    ''' test swapping variants to reverse strand
    '''
    
    class Var:
        pass
    
    def test_revcomp(self):
        self.assertEqual(revcomp('ACTT'), 'AAGT')
        
        # can handle other allele values
        self.assertEqual(revcomp('AN*'), '*NT')
        
        # can handle lower-case
        self.assertEqual(revcomp('actt'), 'aagt')
        
        # non-DNA sequences pass through unmodified (but reversed)
        self.assertEqual(revcomp('MZ'), 'ZM')
    
    def test_is_snv(self):
        self.assertTrue(is_snv('A', 'G'))
        self.assertTrue(is_snv('AT', 'TT'))
        self.assertFalse(is_snv('A', 'TG'))
    
    def test_is_indel(self):
        self.assertTrue(is_indel('A', 'AG'))
        self.assertTrue(is_indel('AG', 'A'))
        self.assertFalse(is_indel('G', 'A'))
    
    def test_is_cnv(self):
        self.assertTrue(is_cnv('A', '<DEL>', {'SVLEN': 1000}))
        self.assertTrue(is_cnv('A', '<DEL>', {}))
        
        # make sure non-CNVs don't return true
        self.assertFalse(is_cnv('A', 'G', {}))
    
