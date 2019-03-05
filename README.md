#### vcfremapper
utility to convert coordinates of variants in VCF files between different genome
builds.

### Install
Install via pip:
```sh
pip install vcfremapper
```

### Usage
``` sh
vcfremapper PATH_TO_VCF CONVERTED --reference genome.fa

# or pass output to bgzip
vcfremapper PATH_TO_VCF --reference genome.fa | bgzip > CONVERTED

# or pipe in gzipped data
cat PATH_TO_VCF | vcfremapper --reference genome.fa | bgzip > CONVERTED
```

Options:
 - `--reference` - path to reference genome, for the build being converted to.
 - `--build-in` - build to convert from, defaults to hg19
 - `--build-out` - build to convert to, defaults to hg38
 - `--tempdir` - folder to save uncompressed temp file in before sorting
