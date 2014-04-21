#! /usr/bin/env python
from setuptools import setup
import os

PROJECT_ROOT, _ = os.path.split(__file__)
REVISION = '0.0.21'
PROJECT_NAME = 'toytable'
PROJECT_AUTHORS = "Salim Fadhley"
PROJECT_EMAILS = 'salimfadhley@gmail.com'
PROJECT_URL = "https://bitbucket.org/salimfadhley/toytable"
SHORT_DESCRIPTION = 'Simple in-memory tables in Python.'

DESCRIPTION = """Toytable is a toy table package. It is suitable for lightweight data analysis tasks. It provides a class
which is suitable for representing one-dimensional tables (e.g. time-sequences).

Toytable is built with an emphasis on simplicity, both in interface and internal design
rather than performance or scalability. Toytable is intended to have as few dependancies
as possible, and is therefore suitable for casual development tasks."""


setup(
    name=PROJECT_NAME.lower(),
    version=REVISION,
    author=PROJECT_AUTHORS,
    author_email=PROJECT_EMAILS,
    packages=['toytable', 'toytable_tests'],
    zip_safe=True,
    include_package_data=False,
    install_requires=['blist', 'six'],
    test_suite='nose.collector',
    tests_require=['mock', 'nose', 'coverage'],
    url=PROJECT_URL,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    use_2to3=True,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ],
)
