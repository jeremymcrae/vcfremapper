
import unittest

from vcfremapper.samples import Sample, Samples

class TestSample(unittest.TestCase):
    ''' test Sample class
    '''
    
    def setUp(self):
        # reset Sample fields, to keep tests clean
        Sample.set_format('')
    
    def test_sample__init__(self):
        ''' check initialising a Sample
        '''
        Sample.set_format('GT:DP')
        samp = Sample('1/1:100')
        
        self.assertEqual(samp.keys(), ['GT', 'DP'])
        self.assertEqual(samp['GT'], '1/1')
        self.assertEqual(samp['DP'], '100')
        
        # check when all fields are blank
        samp = Sample('.')
        self.assertEqual(samp['GT'], '.')
        self.assertEqual(samp['DP'], '.')
        
        # check for an error if the sample and expected fields are different
        with self.assertRaises(ValueError):
            Sample('1/1')
        
        # check that Sample can have different keys
        Sample.set_format('GT')
        samp = Sample('1/1')
        self.assertEqual(samp.keys(), ['GT'])
    
    def test_sample__str__(self):
        ''' check conversion of Sample to str
        '''
        
        Sample.set_format('GT:DP')
        
        samp = Sample('1/1:100')
        self.assertEqual(str(samp), '1/1:100')
        
        samp = Sample('.')
        self.assertEqual(str(samp), '.:.')
    
    def test_sample__setitem__(self):
        ''' check setting Sample fields
        '''
        
        Sample.set_format('GT:DP')
        
        samp = Sample('1/1:100')
        samp['DP'] = 200
        self.assertEqual(samp['DP'], 200)
        self.assertEqual(str(samp), '1/1:200')
    
    def test_sample__del__(self):
        ''' check sample field deletion
        '''
        
        Sample.set_format('GT:DP')
        
        samp = Sample('1/1:100')
        self.assertEqual(samp.keys(), ['GT', 'DP'])
        
        # deleting an entry just gives a NA value
        del samp['DP']
        self.assertEqual(samp.keys(), ['GT', 'DP'])
        self.assertEqual(samp['DP'], '.')
    
    def test_sample__eq__(self):
        Sample.set_format('GT:DP')
        a = Sample('1/1:100')
        b = Sample('1/1:100')
        c = Sample('1/1:101')
        
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

class TestSamples(unittest.TestCase):
    ''' test Samples class
    '''
    def test_samples__init__(self):
        ''' check initialising Samples
        '''
        
        samples = Samples('GT:DP', ['1/1:100', '0/1:.', '.'])
        self.assertEqual(samples.idx, -1)
        self.assertEqual(samples.samples, [Sample('1/1:100'), Sample('0/1:.'),
            Sample('.')])
    
    def test_samples__str__(self):
        ''' check conversion of Samples to str
        '''
        samples = Samples('GT:DP', ['1/1:100', '0/1:.', '.'])
        self.assertEqual(str(samples), 'GT:DP\t1/1:100\t0/1:.\t.:.')
    
    def test_samples__iter__(self):
        ''' check iterating through Samples
        '''
        samples = Samples('GT:DP', ['1/1:100', '0/1:.', '.'])
        matched = [Sample('1/1:100'), Sample('0/1:.'), Sample('.')]
        
        self.assertEqual(len(samples), len(matched))
        for x, y in zip(samples, matched):
            self.assertEqual(x, y)
    
