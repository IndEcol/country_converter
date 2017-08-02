Contributing to coco
====================

First off, thanks for taking the time to contribute!

There are two main ways you can help to improve the country converter coco.

1) Update the country table, for example by providing new regular expressions to account for more country variants or by adding new country classifications.

2) Add new functionality to the code.

Independent of your contribution, please use pull requests to inform me about any improvements you did and make sure all tests pass (see below).


Updating the country table
--------------------------

The underlying raw data of coco is a tab-separated file (country_converter/country_data.tsv) which is read into a Pandas_ DataFrame (available as attribute .data in the main class).
Any column added to this DataFrame can be used for all conversions. The datafile is utf-8 encoded.

Regular expressions
^^^^^^^^^^^^^^^^^^^

The easiest way to contribute to coco is by improving the regular expressions used for matching a specific country name.
If you come across a country name which currently is not matched by the regular expressions included in country_converter/country_data.tsv add or modify the regular expression for this country in the column "regex".
For a good introduction in the used regular expression syntax see https://docs.python.org/3.5/library/re.html .
In particular, make use of the or symbol "|" to include multiple regular expressions for one country.
See the entry for "Czech Republic" for a relatively simple example, "Republic of the Congo" for a more advanced case.
IMPORTANT: new regular expressions must not break the already present matchings.
Run the tests before issuing a pull request and consider including a test case for the new match (see below).

New country classification
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you think a certain country classification is missing from coco, you can simply add them as new columns in country_converter/country_data.tsv.
For fixed country classifications (as for example the "continent") just add a new column with the corresponding name.
For a classification which changes over time (as for example "OECD") make an new column and provide the year at with the country obtained its membership.
Optional: you can add a new property for accessing a specific membership.
See the available properties for EU28, OECD, etc in the class CountryConverter in country_converter/country_converter.py for how to do that and continue reading at
"Changing the code base".
New classifications must also be added to the README.rst at the section "Classification schemes"

Changing the code base
----------------------

If you plan any changes to the source code of this repo, please first discuss the change you wish to make via a filing an issue (labelled Enhancement or Bug) before making a change.
All code contribution must be provided as pull requests connected to a filed issue.
Use numpy style docstrings_ and follow pep8_ style guide.
The latter is a requirement to pass the tests before merging a pull request.
Since coco is already used in research projects, please aim for keeping compatibility with previous versions.

.. _docstrings: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _pep8: https://www.python.org/dev/peps/pep-0008/

Running and extending the tests
-------------------------------

Before filing a pull request, make sure your changes pass all tests.
Coco uses the py.test_ package with the pytest-pep8_ extension for testing.
To run the tests install these two packages (and the Pandas_ dependency) and run

::

    py.test -v -pep8

in the root of your local copy of coco.

The included tests verify the regular expressions against names commonly found in various databases.

These tests check

#) Do the short names uniquely match the regular expression?
#) Do the official name uniquely match the regular expression?
#) Do the alternative names tested so far still uniquely match the standard names?

To specify a new test set just add a tab-separated file with headers "name_short" and "name_test" and provide name (corresponding to the short name in the main classification file) and the alternative name which should be tested (one pair per row in the file).
If the file name starts with "test\_regex\_" it will be automatically recognised by the test functions.

.. _py.test: http://pytest.org/
.. _pytest-pep8: https://pypi.python.org/pypi/pytest-pep8
.. _Pandas: https://pandas.pydata.org/




