
from collections import OrderedDict

class Sample(object):
    ''' hold sample data for a variant (e.g. genotype call, allele depths)
    '''
    # set up a class variable that will be shared by all Sample instances, ie,
    # all individuals for a given variant. That way they have a common set of
    # keys for the variant.
    fields = OrderedDict()
    @classmethod
    def set_format(cls_obj, fields):
        cls_obj.fields = OrderedDict()
        for key in fields.split(':'):
            if key == '':
                continue
            cls_obj.fields[key] = None
    
    def __init__(self, sample):
        self.data = {}
        if sample == '.':
            sample = '.:' * len(self.fields)
            sample = sample[:-1]
        
        sample = sample.split(':')
        if len(sample) != len(self.fields):
            raise ValueError('sample data should match expected fields')
        
        for key, value in zip(self.fields, sample):
            self[key] = value
    
    def __str__(self):
        return ':'.join(map(str, (self[x] for x in self.fields)))
    
    def keys(self):
        return list(self.fields)
    
    def __getitem__(self, key):
        if key not in self.fields:
            raise KeyError
        
        # if a key isn't present in one sample (because the key was only used
        # for a subset of samples), then use missing value for other samples
        if key not in self.data:
            return '.'
        
        return self.data[key]
    
    def __setitem__(self, key, value):
        if key == '':  # key must not be blank
            return
        
        # new keys need be tracked for all samples
        if key not in self.fields:
            self.fields[key] = None
        
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.fields
    
    def __delitem__(self, key):
        self.data[key] = '.'
    
    def __hash__(self):
        return hash(tuple(self[x] for x in self.fields))
    
    def __eq__(self, other):
        return self.fields == other.fields and hash(self) == hash(other)

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
        
        if self.idx >= len(self):
            self.idx = -1
            raise StopIteration
        
        return self.samples[self.idx]
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        return self.samples[idx]
