#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='rutimeparser',
    version='1.1.0',
    author='orsinium',
    author_email='master_fess@mail.ru',
    description='Recognize date and time in russian text.',
    long_description=open('README.rst', encoding='utf8').read(),
    keywords='timeparser parse date time datetime russian text',
    packages=['rutimeparser'],
    requires=['python (>= 3.4)'],
    url='https://github.com/orsinium/rutimeparser',
    download_url='https://github.com/orsinium/rutimeparser/tarball/master',
    license='GNU Lesser General Public License v3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    ],
)
