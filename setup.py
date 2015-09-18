#!/usr/bin/env python

from distutils.core import setup

setup(name='ansiterm_flashcard',
      version='4.0.0',
      description='flash card presenter',
      author='gulan',
      author_email='glen.wilder@gmail.com',
      # data_files=[('share/flashy','hsk2009.sql')],
      # packages=['flashy'],
      py_modules=['chinese','deck_api','screen','dialog'],
      scripts=['ansiterm_flashcard.py']
     )
