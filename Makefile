# -*- coding: utf-8; mode: makefile-gmake; -*-

realclean:
	find . -name "*~"  -print -exec rm -f {} \;
	find . -name ".*~" -print -exec rm -f {} \;
	rm -fr doc/_build
	rm -fr doc/apidoc

pep8:
	py.test --pep8 -m pep8 marketdata
	# py.test --pep8 -m pep8 tests
	# py.test --pep8 -m pep8 --clearcache
	# pep8 --show-source --show-pep8

pep8-tests:
	py.test --pep8 -m pep8 tests

flake8:
	py.test --flake8 -m flake8 marketdata


cov:
	PYTHONPATH=marketdata/ISO3166MIC pytest --cov

cov-report: 
	coverage combine .coverage
	coverage report

