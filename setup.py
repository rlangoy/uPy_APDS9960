"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='uPy_APDS9960',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='micropython proximity driver for APSD9960 / GY-9960LLC  board',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/rlangoy/uPy_APDS9960',

    # Author details
    author='Rune Langøy',
 
    # Choose your license
    license='GNUv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='PDS9960 / GY-9960LLC proximity light sensor hardware micropython',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['uPy_APDS9960'],
)
