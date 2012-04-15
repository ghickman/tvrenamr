SHELL := /bin/bash

pyc:
	find . -name "*.pyc" -delete

release:
	python setup.py register sdist upload

simpleci:
	nosetests --with-spec

test:
	nosetests --with-spec --spec-color

