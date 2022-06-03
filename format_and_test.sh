#!/bin/bash

#small shell utitlity to format all files and 
#run all tests.

#requires pytest, isort and black to be installed

# format
isort --project pymrio --profile black .
black .

# test
coverage erase
isort --profile black --check-only .
coverage run -m pytest --black -vv .
coverage report 

# for more information on the coverage run
# coverage html 
# and open
# ./htmlcov/index.html

