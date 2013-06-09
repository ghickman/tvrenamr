import multiprocessing  # stop tests breaking tox
from setuptools import setup

import tvrenamr


requires = ('pyyaml', 'requests')
packages = ('tvrenamr',)

setup_requires = ('minimock', 'mock', 'nose', 'pyyaml')

setup(
    name = tvrenamr.__title__,
    version = tvrenamr.__version__,
    description = 'Rename tv show files using online databases',
    long_description = open('README.rst').read() + '\n\n' +
                       open('CHANGELOG.rst').read(),
    author = tvrenamr.__author__,
    author_email = 'george@ghickman.co.uk',
    url = 'http://tvrenamr.info',
    license = open('LICENSE').read(),
    packages = packages,
    entry_points = {'console_scripts': ['tvr = tvrenamr.frontend:run']},
    classifiers = (
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia',
        'Topic :: Utilities',
    ),
    install_requires = requires,
    setup_requires=setup_requires,
    test_suite='nose.collector',
)

