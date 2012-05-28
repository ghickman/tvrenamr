SHELL := /bin/bash

pyc:
	find . -name "*.pyc" -delete

release:
	python setup.py register sdist upload

simpleci:
	nosetests

test:
	nosetests --with-spec --spec-color

