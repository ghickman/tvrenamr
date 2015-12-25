SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make release -- build and release to PyPI"
	@echo "    make setup   -- set up for local dev"
	@echo "    make test    -- run the tests"

release:
	python setup.py register sdist bdist_wheel upload

setup:
	pip install -e .
	pip install -r requirements.txt

test:
	tox
