
class Sample(object):
    fields = []
    @classmethod
    def set_format(cls_obj, fields):
        cls_obj.fields = fields.split(':')
    
    def __init__(self, sample):
        if sample == '.':
            self.data = dict(zip(self.fields, [ '.' for x in self.fields ]))
        else:
            self.data = dict(zip(self.fields, sample.split(':')))
    
    def __str__(self):
        return ':'.join( self[x] for x in self.fields )
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.data
    
    def __delitem__(self, key):
        del self.data[key]

class Samples(object):
    def __init__(self, fields, samples):
        Sample.set_format(fields)
        self.samples = [ Sample(x) for x in samples ]
        self.idx = -1
        
    def __str__(self):
        data = [':'.join(Sample.fields)] + list(map(str, self.samples))
        return '\t'.join(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.idx += 1
        
        if self.idx >= len(self.samples):
            self.idx = -1
            raise StopIteration
        
        return self.samples[self.idx]
