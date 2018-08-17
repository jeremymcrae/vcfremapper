
import sys
import os
import io
from setuptools import setup

setup (name="vcfremapper",
    description='Package to maps VCFs between genome builds',
    long_description=io.open('README.md', encoding='utf-8').read(),
    version="1.0.0",
    author="Jeremy McRae",
    author_email="jmcrae@illumina.com",
    license="MIT",
    url='https://github.com/jeremymcrae/vcfremapper',
    packages=["vcfremapper"],
    install_requires=['pyliftover >= 0.3.0',
    ],
    entry_points={'console_scripts': ['vcfremapper = vcfremapper.__main__:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
    ])
