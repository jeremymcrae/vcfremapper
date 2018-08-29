
import unittest

from vcfremapper.info import Info

class TestInfo(unittest.TestCase):
    ''' test Info class
    '''
    
    def test_info_init(self):
        ''' check initialising Info objects
        '''
        
        info = Info('AC=100')
        self.assertIn('AC', info)
        self.assertEqual(sorted(info.keys()), ['AC'])
        self.assertEqual(info['AC'], '100')
        
        # check we don't have any entries for the default
        info = Info()
        self.assertEqual(len(info.keys()), 0)
    
    def test_info__str__(self):
        ''' check conversion to string
        '''
        self.assertEqual(str(Info('AC=100')), 'AC=100')
        self.assertEqual(str(Info('AC=100;AN=200')), 'AC=100;AN=200')
        
        # info output is sorted
        self.assertEqual(str(Info('AN=100;AC=200')), 'AC=200;AN=100')
        
        # duplicate fields are trimmed
        self.assertEqual(str(Info('AC=100;AC=200')), 'AC=200')
        
        # empty string gives empty string
        self.assertEqual(str(Info('')), '')
        
        # default initialiser gives empty string
        self.assertEqual(str(Info()), '')
    
    def test_parse_info(self):
        ''' check parsing more complex info fields
        '''
        # check multiple entries
        info = Info('AC=100;AN=200')
        self.assertEqual(sorted(info.keys()), ['AC', 'AN'])
        self.assertEqual(info['AC'], '100')
        self.assertEqual(info['AN'], '200')
        
        # check flag fields
        info = Info('AC=100;AN')
        self.assertEqual(sorted(info.keys()), ['AC', 'AN'])
        self.assertEqual(info['AC'], '100')
        self.assertEqual(info['AN'], True)
        
        # check empty info
        info = Info('')
        self.assertEqual(len(info.keys()), 0)
        
        # check field with extra '='
        info = Info('B=this=fine')
        self.assertEqual(info['B'], 'this=fine')
    
    def test_info__setitem__(self):
        ''' check setting Info fields
        '''
        
        info = Info()
        info['AC'] = 100
        self.assertEqual(info['AC'], 100)
        self.assertEqual(str(info), 'AC=100')
    
    def test_info__del__(self):
        ''' check info field deletion
        '''
        
        info = Info('AC=100;AN=200')
        self.assertEqual(sorted(info.keys()), ['AC', 'AN'])
        
        del info['AC']
        self.assertEqual(sorted(info.keys()), ['AN'])
        
        # check we raise an error if deleting a missing key
        with self.assertRaises(KeyError):
            del info['AC']
    
    def test_info__eq__(self):
        ''' check info equality
        '''
        a = Info('AC=100')
        b = Info('AC=101')
        self.assertNotEqual(a, b)
        
        # now change value so they are identical
        b['AC'] = '100'
        self.assertEqual(a, b)
    
