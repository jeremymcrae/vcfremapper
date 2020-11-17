
import unittest
import tempfile

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from vcfremapper.sort_vcf import sort_vcf

class TestSortVcf(unittest.TestCase):
    ''' test sort_vcf function
    '''

    def test_sort_vcf(self):
        ''' check sort_vcf function
        '''
        lines = ['1\t100\t.\tA\tG\t100\tPASS\tAC=100\n',
            '2\t150\t.\tA\tG\t100\tPASS\tAC=100\n',
            '2\t150\t.\tA\tC\t100\tPASS\tAC=100\n',
            '1\t200\t.\tA\tG\t100\tPASS\tAC=100\n',
            '1\t180\t.\tA\tG\t100\tPASS\tAC=100\n']

        input = tempfile.NamedTemporaryFile(mode='w+t')
        output = tempfile.NamedTemporaryFile(mode='w+t')

        input.writelines(lines)
        input.flush()

        header = '##fileformat=VCFv4.1\n' \
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
        # define the byte offsets for the lines by their coordinates
        coords = {
            '1': {
                (100, 'A', ('G',)): 0, 
                (200, 'A', ('G',)): 84, 
                (180, 'A', ('G',)): 112,
                }, 
            '2': {
                (150, 'A', ('G',)): 28,
                (150, 'A', ('C',)): 56,
                },
            }

        # sort the VCF
        sort_vcf(coords, input, output, header)

        output.seek(0)
        self.assertEqual(output.read(), header + ''.join(sorted(lines)))
