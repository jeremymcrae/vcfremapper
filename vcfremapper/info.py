
class Info(object):
    ''' class for INFO field of VCF variants
    '''
    def __init__(self, values=''):
        self.info = {}
        
        for item in values.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
            else:
                key, value = item, True
            self[key] = value
    
    def __str__(self):
        ''' reprocess the info dictionary back into a string, correctly sorted
        '''
        
        info = []
        for key, value in sorted(self.info.items()):
            entry = key
            if value != True:
                entry = '{}={}'.format(key, value)
            info.append(entry)
            
        return ';'.join(info)
    
    def keys(self):
        return self.info.keys()
    
    def __getitem__(self, key):
        return self.info[key]
    
    def __setitem__(self, key, value):
        if key == '':  # key must not be blank
            return
        self.info[key] = value
    
    def __contains__(self, key):
        return key in self.info
    
    def __delitem__(self, key):
        del self.info[key]
    
    def __eq__(self, other):
        if set(self.keys()) != set(other.keys()):
            return False
        
        return all(self[key] == other[key] for key in self.info)
            
