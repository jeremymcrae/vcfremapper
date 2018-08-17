#### vcfremapper
utility to convert coordinates of variants in VCF files between different genome
builds.

### Install
``` sh
python setup.py install
```

### Usage
``` sh
vcfremapper PATH_TO_VCF CONVERTED

# or pass output to bgzip
vcfremapper PATH_TO_VCF | bgzip > CONVERTED

# or pipe in gzipped data
cat PATH_TO_VCF | vcfremapper | bgzip > CONVERTED
```
