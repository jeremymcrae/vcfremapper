''' setup file for vcfremapper
'''

import io
from setuptools import setup

setup(name="vcfremapper",
    description='Package to map VCFs between genome builds',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    version="1.0.5",
    author="Jeremy McRae",
    author_email="jmcrae@illumina.com",
    license="MIT",
    url='https://github.com/jeremymcrae/vcfremapper',
    packages=["vcfremapper"],
    install_requires=[
        'liftover >= 1.0.0',
        'pyfaidx >= 0.5.4'
    ],
    entry_points={'console_scripts': ['vcfremapper = vcfremapper.__main__:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite='tests')
