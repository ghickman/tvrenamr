SHELL := /bin/bash

pyc:
	find . -name "*.pyc" -delete

release:
	python setup.py register sdist upload

test:
	python setup.py test

