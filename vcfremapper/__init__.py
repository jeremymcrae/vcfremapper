from pkg_resources import get_distribution

__version__ = get_distribution('vcfremapper').version

CHROMS = list(map(str, range(1, 23))) + ['X', 'Y', 'MT']
CHROMS += [ 'chr{}'.format(x) for x in CHROMS ]
