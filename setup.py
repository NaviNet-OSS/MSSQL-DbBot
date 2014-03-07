#!/usr/bin/env python

from setuptools import setup
from os.path import abspath, dirname, join
import re

NAME = 'MSSQL-dbbot'
CLASSIFIERS = """
Development Status :: 4 - Beta 
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'dbbot', '__init__.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'\n", f.read()).group(1)
with open(join(CURDIR, 'README.md')) as f:
    README = f.read()

setup(
    name             = NAME,
    version          = VERSION,
    author           = 'aaronhutton',
    author_email     = 'ahutton@navinet.net',
    url              = 'https://github.com/NaviNet/MSSQL-DbBot',
    download_url     = 'https://github.com/NaviNet/MSSQL-DbBot/tarball/'VERSION,
    license          = 'Apache License 2.0',
    description      = 'A tool for serializing Robot Framework test run '
                       'results into an sqlite3 database.',
    long_description = README,
    keywords         = 'robotframework testing testautomation atdd database',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    packages         = ['dbbot'],
    install_requires = ['robotframework']
)

