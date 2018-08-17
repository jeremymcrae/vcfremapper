
class Sample(object):
    format = None
    @classmethod
    def set_format(cls_obj, format):
        cls_obj.format = format.split(':')
    
    def __init__(self, sample):
        if sample == '.':
            self.data = dict(zip(self.format, [ '.' for x in self.format ]))
        else:
            self.data = dict(zip(self.format, sample.split(':')))
    
    def __str__(self):
        return ':'.join( self[x] for x in self.format )
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.data
    
    def __delitem__(self, key):
        del self.data[key]

class Samples(object):
    def __init__(self, format, samples):
        Sample.set_format(format)
        self.samples = [ Sample(x) for x in samples ]
        self.idx = -1
        
    def __str__(self):
        return [':'.join(Sample.format)] + self.samples
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.idx += 1
        
        if self.idx >= len(self.samples):
            self.idx = -1
            raise StopIteration
        
        return self.samples[self.idx]
