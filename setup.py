#!/usr/bin/env python

from distutils.core import setup

setup(name='jiyi-tty',
      version='4.1.0',
      description='flash card presenter',
      author='gulan',
      author_email='glen.wilder@gmail.com',
      data_files=[('hsk2009.sql',)],
      py_modules=['chinese', 'screen', 'dialog'],
      scripts=['main.py'])
