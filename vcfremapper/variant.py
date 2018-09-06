
from vcfremapper.info import Info
from vcfremapper.samples import Samples

class Variant(object):
    ''' Variant object, to hold data from VCF line
    '''
    header = None
    @classmethod
    def set_header(cls, header):
        cls.header = header
    
    def __init__(self, line):
        line = line.strip('\n').split('\t')
        self.chrom, pos, self.var_id, self.ref, alts, self.qual, self.filter, \
            self.info = line[:8]
        
        self.pos = int(pos)
        self.alts = alts
        self.info = Info(self.info)
        self.samples = None if len(line) == 8 else Samples(line[8], line[9:])
    
    def __str__(self):
        alts = ','.join(self.alts)
        data = [self.chrom, self.pos, self.var_id, self.ref, alts, self.qual,
            self.filter, self.info]
        
        if self.samples is not None:
            data.append(self.samples)
        
        return '\t'.join(map(str, data)) + '\n'
    
    @property
    def alts(self):
        return self._alts
    
    @alts.setter
    def alts(self, value):
        ''' set alts attribute from either list or comma-separated string
        '''
        if isinstance(value, list):
            self._alts = value
        else:
            self._alts = value.split(',')
