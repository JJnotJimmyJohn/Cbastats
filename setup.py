# from distutils.core import setup
import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md"),encoding='utf-8') as fid:
    README = fid.read()

setup(
  name = 'cbastats',
  packages = ['cbastats'],
  version = 'v0.0.4',
  license='MIT',
  long_description=README,
  long_description_content_type="text/markdown",
  description = 'Python package to access CBA stats',
  author = 'Jian Jin',
  author_email = 'jjtt0926@gmail.com',
  url = 'https://github.com/JJ0131/Cbastats',
  download_url = 'https://github.com/JJ0131/Cbastats/archive/v0.0.4.tar.gz',
  keywords = ['CBA', 'Baseketball'],
  install_requires=[
          'pandas','tabulate'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7'
  ],
)