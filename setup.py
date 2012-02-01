from setuptools import setup, find_packages

from tvrenamr import get_version

setup(
    name = 'tvrenamr',
    version = get_version(),
    description = 'Rename tv show files using online databases',
    author = 'George Hickman',
    author_email = 'george@ghickman.co.uk',
    url = 'http://github.com/ghickman/tvrenamr',
    license = 'MIT',
    packages = find_packages(exclude=['tests']),
    entry_points = {'console_scripts': ['tvr = tvrenamr.tvrenamr:run',],},
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Topic :: Multimedia',
        'Topic :: Utilities',
        'Natural Language :: English'],
    install_requires = ('lxml', 'pyyaml', 'requests',)
)

