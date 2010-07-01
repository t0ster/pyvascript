from setuptools import setup
import os

DESCRIPTION = 'Pythonic JavaScript syntax'

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

setup(name='pyvascript',
      packages=['pyvascript'],
      author='Waldemar Kornewald',
      url='http://www.allbuttonspressed.com/projects/pyvascript',
      include_package_data=True,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      install_requires=[],
)
