# -*- coding: utf-8; mode: makefile-gmake; -*-

realclean:
	$(MAKE) -C doc realclean
	find . -name "*~"  -print -exec rm -f {} \;
	find . -name ".*~" -print -exec rm -f {} \;

pep8:
	py.test --pep8 -m pep8 marketdata

# py.test --pep8 -m pep8 tests
# py.test --pep8 -m pep8 --clearcache
# pep8 --show-source --show-pep8

test:
	python -m pytest -v -rA

pep8-tests:
	python -m pytest --pep8 -m pep8 tests

flake8:
	python -m pytest --cache-clear --flake8 -m flake8 marketdata

flake8-tests:
	python -m pytest --cache-clear --flake8 -m flake8 tests


cov:
	python -m pytest --cov=./marketdata --cov-report=html

cov-report: 
	coverage combine .coverage
	coverage report

