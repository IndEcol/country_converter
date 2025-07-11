# Contributing to coco

First off, thanks for taking the time to contribute!

There are two main ways you can help to improve the country converter
coco.

1.  Update the country table, for example by providing new regular
    expressions to account for more country variants or by adding new
    country classifications.
2.  Add new functionality to the code.

Independent of your contribution, please use pull requests to inform me
about any improvements you did and make sure all tests pass (see below).

## Updating the country table

The underlying raw data of coco is a tab-separated file
(country_converter/country_data.tsv) which is read into a
[Pandas](https://pandas.pydata.org/) DataFrame (available as attribute
.data in the main class). Any column added to this DataFrame can be used
for all conversions. The datafile is utf-8 encoded.

### Regular expressions

The easiest way to contribute to coco is by improving the regular
expressions used for matching a specific country name. If you come
across a country name which currently is not matched by the regular
expressions included in country_converter/country_data.tsv add or modify
the regular expression for this country in the column "regex". For a
good introduction in the used regular expression syntax see
<https://docs.python.org/3.8/library/re.html> . In particular, make use
of the or symbol "\|" to include multiple regular expressions for one
country. See the entry for "Czech Republic" for a relatively simple
example, "Republic of the Congo" for a more advanced case. IMPORTANT:
new regular expressions must not break the already present matchings.
Run the tests before issuing a pull request and consider including a
test case for the new match (see below).

### New country classification

If you think a certain country classification is missing from coco, you
can simply add them as new columns in
country_converter/country_data.tsv. For fixed country classifications
(as for example the "continent") just add a new column with the
corresponding name. For a classification which changes over time (as for
example "OECD") make an new column and provide the year at which the
country obtained its membership. New properties are added automatically
to the CountryConverter class for all columns in this file. New
classifications must also be added to the README.rst at the section
"Classification schemes"

If you need to parse some data to extract the classification codes, see
the example script for parsing the Global Burden of Diseases here:
<https://gist.github.com/IndEcol/dc3583a4674a39def0d4611c095eb788>

## Changing the code base

If you plan any changes to the source code of this repo, please first
discuss the change you wish to make by filing an issue (labelled
Enhancement or Bug) before making a change. All code contributions must
be provided as pull requests connected to a filed issue. Use numpy style
[docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
and follow the [pep8](https://www.python.org/dev/peps/pep-0008/) style guide.
Passing the linter and test suite is required before merging a pull request.
Since coco is already used in research projects, please aim to keep compatibility
with previous versions.

All formatting, linting, and testing is managed via [poethepoet](https://github.com/nat-n/poethepoet)
tasks defined in `pyproject.toml`. The following commands can be used:

```bash
poe format      # Format all files
poe check       # Lint the codebase
poe test        # Run fast tests
poe fulltest    # Run the full test suite with coverage
```

If you are using [uv](https://github.com/astral-sh/uv) for environment management, you can set up your development environment with:

```bash
uv sync --all-extras
uv pip install -e . 
```
The `--all-extras` switch ensures that all optional dependencies listed in `pyproject.toml` are installed, including those needed for development and testing.

## Running and extending the tests

Before filing a pull request, make sure your changes pass all tests.
Coco uses the [pytest](http://pytest.org/) package with several plugins
(see `pyproject.toml`). After installing the development dependencies run

```bash
poe test        
```

The included tests verify the regular expressions against names commonly
found in various databases.

These tests check

1.  Do the short names uniquely match the regular expression?
2.  Do the official name uniquely match the regular expression?
3.  Do the alternative names tested so far still uniquely match the
    standard names?

To specify a new test set just add a tab-separated file with headers
"name_short" and "name_test" and provide name (corresponding to the
short name in the main classification file) and the alternative name
which should be tested (one pair per row in the file). If the file name
starts with "test_regex\_" it will be automatically recognised by the
test functions.
