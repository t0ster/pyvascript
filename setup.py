from setuptools import setup, find_packages

DESCRIPTION = 'Pythonic JavaScript syntax'

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

setup(name='pyvascript',
      packages=find_packages(exclude=('tests', 'tests.*')),
      package_data={'pyvascript': ['*.ometa']},
      author='Waldemar Kornewald',
      url='http://www.allbuttonspressed.com/projects/pyvascript',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      install_requires=[],
)
