#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis_async, os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='redis_async',
    version=redis_async.__VERSION__,
    description="Simple redis async wrapper for python3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Redis',
        'Programming Language :: Python :: 3',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='redis_async redis async wrapper for python3',
    author="Stefan Liu",
    author_email="stefanliu@outlook.com",
    url="http://github.com/devfans/redis-async",
    license="MIT",
    packages=["redis_async"],
    include_package_data=True,
    zip_safe=True,
    install_requires=['redis'],
)
