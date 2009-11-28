#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


HOME_URL = 'https://internal.55minutes.com/svn/fiftyfive/python/trunk/lib/'

short_description = '55 Minutes Python libraries.'
if os.path.exists("README.rst"):
    long_description = codecs.open("README.rst", "r", "utf-8").read()
else:
    long_description = short_description


# Setup the project directory
setup(
    name='55M-Python',
    version='0.5',
    author='55 Minutes',
    author_email='info@55minutes.com',
    maintainer='55 Minutes',
    maintainer_email='info@55minutes.com',
    url=HOME_URL,
    description=short_description,
    long_description=long_description,
    download_url=HOME_URL,
    platforms=["any"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilties",
    ],
    license="All Rights Reserved (c) 2010 55 Minutes",
    package_dir={'':'src'},

    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['fiftyfive'],
    zip_safe=False,
)
