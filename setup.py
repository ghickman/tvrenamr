from setuptools import setup

setup(
    name = 'tvrenamr',
    version = '2.1.3',
    description = 'Rename tv show files using online databases',
    author = 'George Hickman',
    author_email = 'george@ghickman.co.uk',
    url = 'http://github.com/ghickman/tvrenamr',
    license = 'MIT',
    packages = ['tvrenamr', 'tvrenamr/lib'],
    scripts = ['bin/tvr'],
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
    install_requires = 'pyyaml'
)