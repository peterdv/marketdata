#!/bin/bash
#
# Install pipenv and jupyterlab
pip install pipenv
pipenv shell
echo "Install jupyterlab in the virtual env by running"
echo "  `pipenv install jupyterlab`"
echo "See https://realpython.com/pipenv-guide/"
echo "Install packages like sphinx using `pipenv install sphinx`"
echo "exit by typing 'exit'"
echo "start 'jupyter' typing `jupyter lab`"

