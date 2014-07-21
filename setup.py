#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "gitdata",
    version = "0.0.1",
    description = "Storage the data files in ssh servers",
    url = "https://github.com/juanpabloaj/gitdata",
    license='MIT',
    author = "JuanPablo AJ",
    author_email = "jpabloaj@gmail.com",
    test_suite = "tests",
    entry_points={
        'console_scripts': [
            'git-data=bin:main',
        ],
    },
    classifiers = [
        'Programming Language :: Python :: 2.7',
    ]
)
