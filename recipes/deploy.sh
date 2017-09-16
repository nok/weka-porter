#!/usr/bin/env bash

# pip install wheel twine

source activate weka-porter
python setup.py sdist bdist_wheel

# TEST
twine register dist/sklearn-porter-0.1.0.tar.gz -r pypitest
twine register dist/sklearn_porter-0.1.0-py2-none-any.whl -r pypitest
twine upload dist/* -r pypitest
# https://testpypi.python.org/pypi?:action=display&name=weka-porter&version=0.1.0

# PROD
# twine register dist/sklearn-porter-0.1.0.tar.gz -r pypi
# twine register dist/sklearn_porter-0.1.0-py2-none-any.whl -r pypi
# twine upload dist/* -r pypi
# https://pypi.python.org/pypi?:action=display&name=weka-porter&version=0.1.0