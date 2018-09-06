
class Header(object):
    ''' object to hold VCF header data
    '''

    def __init__(self):
        self.lines = []
        self.info = {}
        self.format = {}
        self.idx = -1

    def append(self, line):
        self.parse(line)
        self.lines.append(line)

    def parse(self, line):
        if not line.startswith('#'):
            raise ValueError('not a VCF header line')

        if line.startswith('##INFO'):
            attribute = self.info
        elif line.startswith('##FORMAT'):
            attribute = self.format
        else:
            return

        attribute.update(parse_metadata(line))

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        if self.idx >= len(self):
            self.idx = -1
            raise StopIteration

        return self.lines[self.idx]

    def __len__(self):
        return len(self.lines)

    next = __next__

def parse_metadata(line):
    ''' parse a metadata line from VCF header

    ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
    '''
    line = line.strip('\n').split('=', 1)[1].strip('<>')

    data = []
    active = True
    item = ''
    for char in line:
        if char == '"':
            active = not active

        if active and char == ',':
            data.append(item.split('=', 1))
            item = ''
        else:
            item += char

    data.append(item.split('=', 1))
    data = dict(data)
    ID = data.pop('ID')

    return {ID: data}
