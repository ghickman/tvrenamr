SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make release -- build and release to PyPI"
	@echo "    make test    -- run the tests"

release:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

test:
	python setup.py test
