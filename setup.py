#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-archan',
    version='0.0.4',
    packages=['darchan'],
    include_package_data=True,
    license='MPL 2.0',

    author='Timothée Mazzucotelli',
    author_email='timothee.mazzucotelli@gmail.com',
    url='https://github.com/Pawamoy/django-archan',
    # download_url = 'https://github.com/Pawamoy/django-archan/tarball/0.0.1',

    install_requires=['dependenpy', 'archan', 'future'],

    keywords="architecture analysis dependency matrix dsm ontology",
    description="A Django app that displays dependency matrices "
                "and project architecture information",
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        'Development Status :: 4 - Beta',
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ]
)
