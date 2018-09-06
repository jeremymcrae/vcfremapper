
from vcfremapper.variant import Variant
from vcfremapper.header import Header

class VCF(object):
    ''' VCF object, to hold VCF file handle
    
    Can extract header lines, and iterate through VCF variant lines
    '''
    def __init__(self, handle):
        self.handle = handle
        
        if self.handle.seekable():
            self.handle.seek(0)
        
        self.first = None
        self.header = self.handle
    
    @property
    def header(self):
        return self._header
    
    @header.setter
    def header(self, handle):
        self._header = Header()
        for line in handle:
            try:
                self._header.append(line)
            except ValueError:
                break
        
        self.first = line
        
        # make sure all the header data is available within variants
        Variant.set_header(self._header)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.first is not None:
            line, self.first = self.first, None  # get value and blank self.first
            return Variant(line)
        
        return Variant(next(self.handle))
    
    next = __next__
