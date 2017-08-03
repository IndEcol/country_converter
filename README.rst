country converter
=================

The country converter (coco) is a Python package to convert country names between different classifications and between different naming versions. Internally it uses regular expressions to match country names.

.. image:: https://badge.fury.io/py/country_converter.svg
    :target: https://badge.fury.io/py/country_converter
.. image:: http://joss.theoj.org/papers/af694f2e5994b8aacbad119c4005e113/status.svg
    :target: http://joss.theoj.org/papers/af694f2e5994b8aacbad119c4005e113
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.838248.svg
   :target: https://doi.org/10.5281/zenodo.838248
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
.. image:: https://travis-ci.org/konstantinstadler/country_converter.svg?branch=master
    :target: https://travis-ci.org/konstantinstadler/country_converter

|


.. contents:: Table of Contents

Motivation
-----------

To date, there is no single standard of how to name or specify individual countries in a (meta) data description.
While some data sources follow ISO 3166, this standard defines a two and a three letter code in addition to a numerical classification.
To further complicate the matter, instead of using one of the existing standards, many databases use unstandardised country names to classify countries.

The country converter (coco) automates the conversion from different standards and version of country names.
Internally, coco is based on a table specifying the different ISO and UN standards per country together with the official name and a regular expression which aim to match all English versions of a specific country name.
In addition, coco includes classification based on UN-, EU-, OECD-membership, UN regions specifications, continents and various MRIO databases (see `Classification schemes`_ below).

Installation
------------

Country_converter is registered at PyPI. From the command line:

::

    pip install country_converter --upgrade

Alternatively, the source code is available on GitHub_.

.. _GitHub: https://github.com/konstantinstadler/country_converter

The package depends on Pandas_; for testing py.test_ is required.
For further information on running the tests see `CONTRIBUTING.rst`_.

.. _Pandas: http://pandas.pydata.org/

.. _py.test: http://pytest.org/

Usage
-----

Basic usage
^^^^^^^^^^^

Use within Python
"""""""""""""""""

Convert various country names to some standard names:

.. code:: python

    import country_converter as coco
    some_names = ['United Rep. of Tanzania', 'DE', 'Cape Verde', '788', 'Burma', 'COG',
                  'Iran (Islamic Republic of)', 'Korea, Republic of',
                  "Dem. People's Rep. of Korea"]
    standard_names = coco.convert(names=some_names, to='name_short')
    print(standard_names)

Which results in ['Tanzania', 'Germany', 'Cabo Verde', 'Tunisia', 'Myanmar', 'Congo Republic', 'Iran', 'South Korea', 'North Korea'].
The input format is determined automatically, based on ISO two letter, ISO three letter, ISO numeric or regular expression matching.
In case of any ambiguity, the source format can be specified with the parameter 'src'.

In case of multiple conversion, better performance can be achieved by
instantiating a single CountryConverter object for all conversions:

.. code:: python

    import country_converter as coco
    cc = coco.CountryConverter()

    some_names = ['United Rep. of Tanzania', 'Cape Verde', 'Burma',
                  'Iran (Islamic Republic of)', 'Korea, Republic of',
                  "Dem. People's Rep. of Korea"]

    standard_names = cc.convert(names = some_names, to = 'name_short')
    UNmembership = cc.convert(names = some_names, to = 'UNmember')
    print(standard_names)
    print(UNmembership)


Convert between classification schemes:

.. code:: python

    iso3_codes = ['USA', 'VUT', 'TKL', 'AUT', 'XXX' ]
    iso2_codes = coco.convert(names=iso3_codes, to='ISO2')
    print(iso2_codes)

Which results in ['US', 'VU', 'TK', 'AT', 'not found']

The not found indication can be specified (e.g. not_found = 'not there'),
if None is passed for 'not_found', the original entry gets passed through:

.. code:: python

    iso2_codes = coco.convert(names=iso3_codes, to='ISO2', not_found=None)
    print(iso2_codes)

results in ['US', 'VU', 'TK', 'AT', 'XXX']


Internally the data is stored in a Pandas DataFrame, which can be accessed directly.
For example, this can be used to filter countries for membership organisations (per year).
Note: for this, an instance of CountryConverter is required.

.. code:: python

    import country_converter as coco
    cc = coco.CountryConverter()

    some_countries = ['Australia', 'Belgium', 'Brazil', 'Bulgaria', 'Cyprus', 'Czech Republic',
                      'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                      'India', 'Indonesia', 'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania',
                      'Luxembourg', 'Malta', 'Romania', 'Russia', 'Turkey', 'United Kingdom',
                      'United States']

    oecd_since_1995 = cc.data[(cc.data.OECD >= 1995) & cc.data.name_short.isin(some_countries)].name_short
    eu_until_1980 = cc.data[(cc.data.EU <= 1980) & cc.data.name_short.isin(some_countries)].name_short
    print(oecd_since_1995)
    print(eu_until_1980)

Some properties provide direct access to affiliations:

.. code:: python

    cc.EU28
    cc.OECD

    cc.EU27as('ISO3')

and the classification schemes available:

.. code:: python

    cc.valid_class


The regular expressions can also be used to match any list of countries to any other. For example:

.. code:: python

    match_these = ['norway', 'united_states', 'china', 'taiwan']
    master_list = ['USA', 'The Swedish Kingdom', 'Norway is a Kingdom too',
                   'Peoples Republic of China', 'Republic of China' ]

    matching_dict = coco.match(match_these, master_list)


See the IPython Notebook (country_converter_examples.ipynb_) for more information.

.. _country_converter_examples.ipynb: http://nbviewer.ipython.org/github/konstantinstadler/country_converter/blob/master/doc/country_converter_examples.ipynb

Command line usage
""""""""""""""""""""""

The country converter package also provides a command line interface
called coco.

Minimal example:

::

    coco Cyprus DE Denmark Estonia 4 'United Kingdom' AUT

Converts the given names to ISO3 codes based on matching the input to ISO2, ISO3, ISOnumeric or regular expression matching.
The list of names must be separated by spaces, country names consisting of multiple words must be put in quotes ('').

The input classification can be specified with '--src' or '-s' (or will be determined automatically), the target classification with '--to' or '-t'.

The default output is a space separated list, this can be changed by passing a separator by '--output_sep' or '-o' (e.g -o '|').

Thus, to convert from ISO3 to UN number codes and receive the output as comma separated list use:

::

    coco AUT DEU VAT AUS -s ISO3 -t UNcode -o ', '

The command line tool also allows to specify the output for none found entries, including passing them through to the output by passing None:

::

    coco CAN Peru US Mexico Venezuela UK Arendelle --not_found=None

and to specifiy an additional data file which will overwrite existing country matchings

::

    coco Congo --additional_data path/to/datafile.csv

See https://github.com/konstantinstadler/country_converter/tree/master/tests/custom_data_example.txt for an example of an additional datafile.

For further information call the help by

::

    coco -h


Use in Matlab
"""""""""""""

Newer (tested in 2016a) versions of Matlab allow to directly call Python
functions and libaries.  This requires a Python version >= 3.4 installed in the
sytem path (e.g. through Anaconda).

To test, try this in Matlab:

.. code:: matlab

    py.print(py.sys.version)

If this works, you can also use coco after installing it through pip
(at the windows commandline - see the installing instruction above):

.. code:: matlab

    pip install country_converter --upgrade

And in matlab:

.. code:: matlab

    coco = py.country_converter.CountryConverter()
    countries = {'The Swedish Kingdom', 'Norway is a Kingdom too', 'Peoples Republic of China', 'Republic of China'};
    ISO2_pythontype = coco.convert(countries, pyargs('to', 'ISO2'));
    ISO2_cellarray = cellfun(@char,cell(ISO2_pythontype),'UniformOutput',false);


Alternativley, as a long oneliner:

.. code:: matlab

    short_names = cellfun(@char, cell(py.country_converter.convert({56, 276}, pyargs('src', 'UNcode', 'to', 'name_short'))), 'UniformOutput',false);


All properties of coco as explained above are also available in Matlab:

.. code:: matlab

    coco = py.country_converter.CountryConverter();
    coco.EU27
    EU27ISO3 = coco.EU27as('ISO3');

These functions return a Pandas DataFrame.
The underlying values can be access with .values (e.g.

.. code:: matlab

    EU27ISO3.values

I leave it to professional Matlab users to figure out how to further process them.

See also IPython Notebook (country_converter_examples.ipynb_) for more
information - all functions available in Python (for example passing additional
data files, specifying the output in case of missing data) work also in Matlab
by passing arguments through the pyargs function.

.. _Classifications:

Classification schemes
----------------------

Currently the following classification schemes are available:

#) ISO2 (ISO 3166-1 alpha-2)
#) ISO3 (ISO 3166-1 alpha-3)
#) ISO - numeric (ISO 3166-1 numeric)
#) UN numeric code (which follows to a large extend ISO - numeric)
#) A standard or short name
#) The "official" name
#) Continent
#) UN region
#) EXIOBASE 1 classification
#) EXIOBASE 2 classification
#) EXIOBASE 2 classification
#) WIOD classification
#) OECD membership (per year)
#) UN membership (per year)
#) EU membership (per year)


Data sources and further reading
--------------------------------

Most of the underlying data can be found in Wikipedia.
https://en.wikipedia.org/wiki/ISO_3166-1 is a good starting point.
UN regions/codes are given on the United Nation Statistical Division (unstats_) webpage.
EXIOBASE_ and WIOD_ classification were extracted from the respective databases.
The membership of OECD_, UN_ and EU_ can be found at the membership organisations' webpages.

.. _unstats: http://unstats.un.org/unsd/methods/m49/m49regin.htm
.. _OECD: http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm
.. _UN: http://www.un.org/en/members/
.. _EU: http://europa.eu/about-eu/countries/index_en.htm
.. _EXIOBASE: http://exiobase.eu/
.. _WIOD: http://www.wiod.org/home



Communication, issues, bugs and enhancements
--------------------------------------------

Please use the issue tracker for documenting bugs, proposing enhancements and all other communication related to coco.

You can follow me on twitter_ or mastodon_ to get the latest news about all my open-source and research projects (and occasionally some random retweets).

.. _twitter: https://twitter.com/kst_stadler
.. _mastodon: https://mastodon.rocks/@kstadler

Contributing
---------------

Want to contribute? Great!
Please check `CONTRIBUTING.rst`_ if you want to help to improve coco.


Related software
-----------------

The package pycountry_ provides access to the official ISO databases for historic countries, country subdivisions, languages and currencies.
In case you need to convert non-English country names, countrynames_ includes an extensive database of country names in different languages and functions to convert them to the different ISO 3166 standards.
Python-iso3166_ focuses on conversion between the two-letter, three-letter and three-digit codes defined in the ISO 3166 standard.

If you are using R, you should have a look at countrycode_.

.. _pycountry: https://pypi.python.org/pypi/pycountry
.. _Python-iso3166: https://github.com/deactivated/python-iso3166
.. _countrynames: https://github.com/occrp/countrynames

Citing the country converter   
-------------------------------

Version 0.5 of the country converter was published in the `Journal of Open Source Software`_.
To cite the country converter in publication please use:

Stadler, K. (2017). The country converter coco - a Python package for converting country names between different classification schemes. The Journal of Open Source Software. doi: http://dx.doi.org/10.21105/joss.00332

For the full bibtex key see CITATION_

.. _CITATION: CITATION


Acknowledgements
----------------

This package was inspired by (and the regular expression are mostly based on) the R-package countrycode_ by `Vincent Arel-Bundock`_ and his (defunct) port to Python (pycountrycode).
Many thanks to `Robert Gieseke`_ for the review of the source code and paper for the publication in the `Journal of Open Source Software`_.

.. _Vincent Arel-Bundock: http://arelbundock.com/
.. _countrycode: https://github.com/vincentarelbundock/countrycode
.. _Robert Gieseke: https://github.com/rgieseke
.. _Journal of Open Source Software: http://joss.theoj.org/

.. _CONTRIBUTING.rst: CONTRIBUTING.rst
