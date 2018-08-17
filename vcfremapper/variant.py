
class Variant(object):
    ''' Variant object, to hold data from VCF line
    '''
    def __init__(self, line):
        self.chrom, pos, self.var_id, self.ref, alts, \
            self.rest = line.strip('\n').split('\t', 5)
        self.pos = int(pos)
        self.alts = alts
    
    def __str__(self):
        alts = ','.join(self.alts)
        return '{}\t{}\t{}\t{}\t{}\t{}\n'.format(self.chrom, self.pos,
            self.var_id, self.ref, alts, self.rest)
    
    @property
    def alts(self):
        return self._alts
    
    @alts.setter
    def alts(self, value):
        ''' set alts attribute from either list or comma-separated string
        '''
        if type(value) == list:
            self._alts = value
        else:
            self._alts = value.split(',')
