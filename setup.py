import os
import sys
from setuptools import setup

install_requires = [
    'future',
]

test_requires = [
    'nose2',
    'numpy',
    'coverage',
    'coveralls'
]

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 5):
    raise RuntimeError("Python version 2.7 or >=3.5 required.")

version_py = os.path.join(os.path.dirname(
    __file__), 'tasklogger', 'version.py')
version = open(version_py).read().strip().split(
    '=')[-1].replace('"', '').strip()

readme = open('README.rst').read()

setup(name='tasklogger',
      version=version,
      description='tasklogger',
      author='Scott Gigante, Krishnaswamy Lab, Yale University',
      author_email='scott.gigante@yale.edu',
      packages=['tasklogger', ],
      include_package_data=True,
      license='GNU General Public License Version 2',
      install_requires=install_requires,
      extras_require={'test': test_requires},
      test_suite='nose2.collector.collector',
      long_description=readme,
      url='https://github.com/scottgigante/tasklogger',
      download_url="https://github.com/scottgigante/tasklogger/archive/v{}.tar.gz".format(
          version),
      keywords=['graphs',
                'big-data',
                'signal processing',
                'manifold-learning',
                ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Framework :: Jupyter',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Mathematics',
      ]
      )
