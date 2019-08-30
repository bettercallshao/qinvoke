# qinvoke
[![CircleCI](https://circleci.com/gh/hydiant/qinvoke.svg?style=shield)](https://circleci.com/gh/hydiant/qinvoke)
[![PyPi](https://badge.fury.io/py/qinvoke.svg)](https://badge.fury.io/py/qinvoke)

qinvoke - q stands for nothing particular.

# summary
A web gui for running invoke commands.

# install
    pip install qinvoke

# usage
    use qinvoke in place of invoke or import Program from qinvoke instead of invoke.

# develop
to release make a tag like v0.1.0 that matches package version.

    python3 setup.py sdist
    python3 -m twine upload dist/*
