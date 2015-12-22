import multiprocessing  # noqa # stop tests breaking tox
from setuptools import find_packages, setup

import tvrenamr


def long_desc():
    with open('README.rst') as f:
        readme = f.read()

    with open('CHANGELOG.rst') as f:
        changelog = f.read()

    return readme + '\n\n' + changelog


requires = [
    'click',
    'defusedxml',
    'pyyaml',
    'requests',
]

setup(
    name=tvrenamr.__title__,
    version=tvrenamr.__version__,
    description='Rename tv show files using online databases',
    long_description=long_desc(),
    author=tvrenamr.__author__,
    author_email='george@ghickman.co.uk',
    url='http://tvrenamr.info',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={'console_scripts': ['tvr=tvrenamr.cli.core:rename']},
    install_requires=requires,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
)
