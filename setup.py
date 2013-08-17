#!/usr/bin/python

# Python imports
import os

try:
    from setuptools import setup, Extension
    has_setuptools = True
except ImportError:
    from distutils.core import setup, Extension
    has_setuptools = False

version_string = '0.0.1'


setup_kwargs = {}

setup(name="glass.py",
    description="",
    keywords='',
    version="0.0.1",
    url='https://github.com/SamyPesse/glass.py.git',
    license='Apache',
    author="Samy Pesse",
    author_email='samypesse@gmail.com',
    long_description="""""",
    packages=[
        "glass"
    ],
    **setup_kwargs
)
