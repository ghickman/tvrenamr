SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make release -- build and release to PyPI"
	@echo "    make setup   -- set up for local dev"
	@echo "    make test    -- run the tests"

release:
	rm -rf dist/*
	python setup.py register bdist_wheel sdist
	twine upload dist/*

setup:
	pip install -e .
	pip install -r requirements.txt

test:
	tox
