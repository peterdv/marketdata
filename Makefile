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

pep8-tests:
	PYTHONPATH=/home/peterdv/proj/marketdata/marketdata/iso10383mic pytest --pep8 -m pep8 tests

flake8:
	pytest --cache-clear --flake8 -m flake8 marketdata

flake8-tests:
	PYTHONPATH=marketdata/iso10383mic pytest --cache-clear --flake8 -m flake8 tests


cov:
	PYTHONPATH=marketdata/iso10383mic pytest --cov=./marketdata --cov-report=html

cov-report: 
	coverage combine .coverage
	coverage report

