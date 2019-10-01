

import unittest
import tempfile
import os
import shutil

from pyfaidx import Fasta, Faidx

from vcfremapper.revcomp import reverse, complement, revcomp, reverse_var, \
    reverse_snv, reverse_indel, reverse_cnv, is_snv, is_indel, is_cnv

class TestReverse(unittest.TestCase):
    ''' test swapping variants to reverse strand
    '''
    
    class Var:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        
        # create a fasta file
        cls.fa = os.path.join(cls.dir, 'genome.fa')
        with open(cls.fa, mode='wt') as handle:
            handle.write('>chrN\n')
            handle.write('NNTGATGCTAGCTAGTATCTG\n')
        
        # index the fasta file
        fai = Faidx(cls.fa)
        fai.close()
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir)
    
    def test_reverse(self):
        ''' check that reverse works correctly
        '''
        self.assertEqual(reverse('acgt'), 'tgca')
    
    def test_complement(self):
        ''' check that complement works correctly
        '''
        self.assertEqual(complement('acct'), 'tgga')
    
    def test_revcomp(self):
        ''' check that revcomp works correctly
        '''
        self.assertEqual(revcomp('ACTT'), 'AAGT')
        
        # can handle other allele values
        self.assertEqual(revcomp('AN*'), '*NT')
        
        # can handle lower-case
        self.assertEqual(revcomp('actt'), 'aagt')
        
        # non-DNA sequences pass through unmodified (but reversed)
        self.assertEqual(revcomp('MZ'), 'ZM')
    
    def test_reverse_var(self):
        ''' check that reverse_var works correctly
        '''
        genome = Fasta(self.fa)
        var = self.Var(chrom='chrN', pos=11, ref='G', alts=['A', 'C'])
        rev = reverse_var(var, genome)
        self.assertEqual(rev.ref, 'C')
        
        # the position stays the same
        self.assertEqual(var.pos, 11)
        
        # multi-allelic variants with indels return None
        var = self.Var(pos=10, ref='G', alts=['A', 'CC'], info={})
        self.assertIsNone(reverse_var(var, genome))
        genome.close()
    
    def test_reverse_missing_alt(self):
        ''' check that reverse  works correctly
        '''
        genome = Fasta(self.fa)
        var = self.Var(chrom='N', pos=10, ref='C', alts=['.'])
        rev = reverse_var(var, genome)
        self.assertEqual(rev.ref, 'G')
        self.assertEqual(rev.alts, ['.'])
        self.assertEqual(rev.pos, 10)
    
    def test_reverse_missing_ref(self):
        ''' check that reverse  works correctly
        '''
        genome = Fasta(self.fa)
        var = self.Var(chrom='N', pos=1, ref='N', alts=['.'])
        rev = reverse_var(var, genome)
        self.assertEqual(rev.ref, 'N')
        self.assertEqual(rev.alts, ['.'])
        self.assertEqual(rev.pos, 1)

    def test_reverse_snv(self):
        ''' check that reverse_snv works correctly
        '''
        var = self.Var(pos=10, ref='C', alts=['A', 'G'])
        rev = reverse_snv(var)
        self.assertEqual(rev.alts, ['T', 'C'])
        
        # now try a SNV with longer allele codes
        var = self.Var(pos=10, ref='CTA', alts=['ATA', 'GTA'])
        rev = reverse_snv(var)
        self.assertEqual(rev.alts, ['TAT', 'TAC'])
        self.assertEqual(rev.ref, 'TAG')
        self.assertEqual(rev.pos, 8)
    
    def test_reverse_insertion(self):
        ''' check that reverse_indel works correctly for insertions
        '''
        genome = Fasta(self.fa)
        var = self.Var(pos=11, chrom='N', ref='G', alts=['GAA'])
        rev = reverse_indel(var, genome)
        self.assertEqual(rev.pos, 10)
        self.assertEqual(rev.ref, 'G')
        self.assertEqual(rev.alts, ['GTT'])
        genome.close()
    
    def test_reverse_deletion(self):
        ''' check that reverse_indel works correctly for deletions
        '''
        genome = Fasta(self.fa)
        var = self.Var(pos=10, chrom='N', ref='CTA', alts=['C'])
        rev = reverse_indel(var, genome)
        self.assertEqual(rev.pos, 7)
        self.assertEqual(rev.ref, 'CTA')
        self.assertEqual(rev.alts, ['C'])
        genome.close()
    
    def test_reverse_cnv(self):
        ''' check that reverse_cnv works correctly
        '''
        genome = Fasta(self.fa)
        var = self.Var(pos=25, chrom='chrN', ref='A', info={'SVLEN': 15})
        var = reverse_cnv(var, genome)
        
        self.assertEqual(var.pos, 10)
        self.assertEqual(var.ref, 'G')
        genome.close()
    
    def test_is_snv(self):
        ''' check that is_snv works correctly
        '''
        self.assertTrue(is_snv('A', 'G'))
        self.assertTrue(is_snv('AT', 'TT'))
        self.assertFalse(is_snv('A', 'TG'))
    
    def test_is_indel(self):
        ''' check that is_indel works correctly
        '''
        self.assertTrue(is_indel('A', 'AG'))
        self.assertTrue(is_indel('AG', 'A'))
        self.assertFalse(is_indel('G', 'A'))
    
    def test_is_cnv(self):
        ''' check that is_cnv works correctly
        '''
        self.assertTrue(is_cnv('A', '<DEL>', {'SVLEN': 1000}))
        self.assertTrue(is_cnv('A', '<DEL>', {}))
        
        # make sure non-CNVs don't return true
        self.assertFalse(is_cnv('A', 'G', {}))
    
