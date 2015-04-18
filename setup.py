#!/usr/bin/env python
'''
IcePick
------------------
IcePick is a All in one Package library for easy Scraping.


Requirements
------------
* Python 3.4 or later(not support 2.x)


Dependencies Libraries
------------
* aiohttp
* beautifulsoup4
* pymongo >= 3.0
* nose

Links
`````
* `Github <https://github.com/teitei-tk/ice-pick>`_
'''

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    import sys
    print("Please install setuptools.")
    sys.exit(1)


classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='icePick',
    version='0.0.1',
    description='icePick is a All in one Package library for easy Scraping',
    long_description=__doc__,
    author='teitei-tk',
    author_email='teitei.tk@gmail.com',
    url='https://github.com/teitei-tk/ice-pick',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=classifiers,
    install_requires=open('requirements.txt').read().splitlines(),
    keywords=['scraping'],
    download_url='https://github.com/teitei-tk/ice-pick/archive/master.tar.gz'
)
