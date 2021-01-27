country converter
=================

The country converter (coco) is a Python package to convert and match country names between different classifications and between different naming versions. Internally it uses regular expressions to match country names. Coco can also be used to build aggregation concordance matrices between different classification schemes.

.. image:: https://badge.fury.io/py/country-converter.svg
    :target: https://badge.fury.io/py/country_converter
.. image:: https://anaconda.org/conda-forge/country_converter/badges/version.svg   
    :target: https://anaconda.org/conda-forge/country_converter
.. image:: http://joss.theoj.org/papers/af694f2e5994b8aacbad119c4005e113/status.svg
    :target: http://joss.theoj.org/papers/af694f2e5994b8aacbad119c4005e113
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.838035.svg
   :target: https://doi.org/10.5281/zenodo.838035
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
.. image:: https://travis-ci.org/konstantinstadler/country_converter.svg?branch=master
    :target: https://travis-ci.org/konstantinstadler/country_converter
.. image:: https://coveralls.io/repos/github/konstantinstadler/country_converter/badge.svg?branch=master
    :target: https://coveralls.io/github/konstantinstadler/country_converter?branch=master
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


.. contents:: Table of Contents

Motivation
-----------

To date, there is no single standard of how to name or specify individual countries in a (meta) data description.
While some data sources follow ISO 3166, this standard defines a two and a three letter code in addition to a numerical classification.
To further complicate the matter, instead of using one of the existing standards, many databases use unstandardised country names to classify countries.

The country converter (coco) automates the conversion from different standards and version of country names.
Internally, coco is based on a table specifying the different ISO and UN standards per country together with the official name and a regular expression which aim to match all English versions of a specific country name.
In addition, coco includes classification based on UN-, EU-, OECD-membership, UN regions specifications, continents and various MRIO and IAM databases (see `Classification schemes`_ below).

Installation
------------

Country_converter is registered at PyPI. From the command line:

::

    pip install country_converter --upgrade

The country converter is also available from the `conda forge 
<https://conda-forge.org/>`_ and can be installed using conda with (if you don't 
have the conda_forge channel added to your conda config add "-c conda-forge", 
see `the install instructions here <https://github.com/conda-forge/country_converter-feedstock>`_):

::
    
   conda install country_converter

.. _Anaconda: https://anaconda.org/konstantinstadler/country_converter

Alternatively, the source code is available on GitHub_.

.. _GitHub: https://github.com/konstantinstadler/country_converter

The package depends on Pandas_; for testing pytest_ is required.
For further information on running the tests see `CONTRIBUTING.rst`_.

.. _Pandas: http://pandas.pydata.org/
.. _pytest: http://pytest.org/

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

All classifications can be directly accessed by: 

.. code:: python

    cc.EU28
    cc.OECD

    cc.EU27as('ISO3')

and the classification schemes available:

.. code:: python

    cc.valid_class

There is also a methdod for only getting country classifications (thus omitting 
any grouping of countries):

.. code:: python

    cc.valid_country_classifications

If you rather need a dictionary describing the classification/membership use:

.. code:: python

    import country_converter as coco
    cc = coco.CountryConverter()
    cc.get_correspondence_dict('EXIO3', 'ISO3')

to also include countries not assigned within a specific classification use:

.. code:: python

    cc.get_correspondence_dict('EU27', 'ISO2', replace_nan='NonEU')



The regular expressions can also be used to match any list of countries to any other. For example:

.. code:: python

    match_these = ['norway', 'united_states', 'china', 'taiwan']
    master_list = ['USA', 'The Swedish Kingdom', 'Norway is a Kingdom too',
                   'Peoples Republic of China', 'Republic of China' ]

    matching_dict = coco.match(match_these, master_list)
    

Country converter by default provides a warning to the python `logging` logger if no match is found.
The following example demonstrates how to configure the `coco` logging behaviour.

.. code:: python

   import logging
   import country_converter as coco
   logging.basicConfig(level=logging.INFO)
   coco.convert("asdf")
   # WARNING:country_converter.country_converter:asdf not found in regex
   # Out: 'not found'

   coco_logger = coco.logging.getLogger()
   coco_logger.setLevel(logging.CRITICAL)
   coco.convert("asdf")
   # Out: 'not found'


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

and to specify an additional data file which will overwrite existing country matching

::

    coco Congo --additional_data path/to/datafile.csv

See https://github.com/konstantinstadler/country_converter/tree/master/tests/custom_data_example.txt for an example of an additional datafile.

The flags --UNmember_only (-u) and --include_obsolete (-i) restrict the search 
to UN member states only or extend it to also include currently obsolete
countries. For example, the `Netherlands Antilles`_ were dissolved in 2010.

.. _Netherlands Antilles: https://en.wikipedia.org/wiki/Netherlands_Antilles


Thus: 

:: 

   coco "Netherlands Antilles"

results in "not found". The search, however, can be extended to recently 
dissolved countries by:


:: 

   coco "Netherlands Antilles" -i

which results in 'ANT'.

In addition to the countries, the coco command line tool also accepts 
various country classifications (EXIO1, EXIO2, EXIO3, WIOD, Eora, MESSAGE, 
OECD, EU27, EU28, UN, obsolete, Cecilia2050, BRIC, APEC, BASIC, CIS, G7, G20).
One of these can be passed by

::
   
   coco G20

which lists all countries in that classification.

For the classifications covering almost all countries (MRIO and IAM 
classifications)

::

   coco EXIO3

lists the unique classification names. When passing a --to parameter, a 
simplified correspondence of the chosen classification is printed:

::

   coco EXIO3 --to ISO3

For further information call the help by

::

    coco -h


Use in Matlab
"""""""""""""

Newer (tested in 2016a) versions of Matlab allow to directly call Python
functions and libraries.  This requires a Python version >= 3.4 installed in the
system path (e.g. through Anaconda).

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


Alternatively, as a long oneliner:

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



Building concordances for country aggregation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coco provides a function for building concordance vectors, matrices and dictionaries between
different classifications. This can be used in python as well as in matlab.  
For further information see (country_converter_aggregation_helper.ipynb_)

.. _country_converter_aggregation_helper.ipynb: http://nbviewer.ipython.org/github/konstantinstadler/country_converter/blob/master/doc/country_converter_aggregation_helper.ipynb


.. _Classifications:

Classification schemes
----------------------

Currently the following classification schemes are available (see also Data sources below for further information):

#) ISO2 (ISO 3166-1 alpha-2)
#) ISO3 (ISO 3166-1 alpha-3)
#) ISO - numeric (ISO 3166-1 numeric)
#) UN numeric code (M.49 - follows to a large extend ISO-numeric)
#) A standard or short name
#) The "official" name
#) Continent
#) UN region
#) EXIOBASE_ 1 classification
#) EXIOBASE_ 2 classification
#) EXIOBASE_ 3 classification
#) WIOD_ classification
#) Eora_
#) OECD_ membership (per year)
#) MESSAGE_ 11-region classification
#) IMAGE_
#) REMIND_
#) UN_ membership (per year)
#) EU_ membership (including EU12, EU15, EU25, EU27, EU27_2007, EU28)
#) EEA_ membership
#) Schengen_ region
#) Cecilia_ 2050 classification
#) APEC_
#) BRIC_
#) BASIC_
#) CIS_ (as by 2019, excl. Turkmenistan)
#) G7_
#) G20_ (listing all EU member states as individual members)
#) FAOcode_ (numeric)

Coco contains official recognised codes as well as non-standard codes for disputed or dissolved countries. 
To restrict the set to only the official recognized UN members or include obsolete countries, pass

.. code:: python

    import country_converter as coco
    cc = coco.CountryConverter()
    cc_UN = coco.CountryConverter(only_UNmember=True)
    cc_all = coco.CountryConverter(include_obsolete=True)

    cc.convert(['PSE', 'XKX', 'EAZ', 'FRA'], to='name_short')
    cc_UN.convert(['PSE', 'XKX', 'EAZ', 'FRA'], to='name_short')
    cc_all.convert(['PSE', 'XKX', 'EAZ', 'FRA'], to='name_short')

cc results in ['Palestine', 'Kosovo', 'not found', 'France'], whereas cc_UN converts to
['not found', 'not found', 'not found', 'France'] and cc_all converts to
['Palestine', 'Kosovo', 'Zanzibar', 'France']
Note that the underlying dataframe is available at the attribute .data (e.g. cc_all.data).

Data sources and further reading
--------------------------------

Most of the underlying data can be found in Wikipedia, the page describing 
`ISO 3166-1 <https://en.wikipedia.org/wiki/ISO_3166-1>`_ is a good starting point.
UN regions/codes are given on the United Nation Statistical Division (unstats_) webpage.
The differences between the ISO numeric and UN (M.49) codes 
are `also explained at wikipedia <https://en.wikipedia.org/wiki/UN_M.49>`_.
EXIOBASE_, WIOD_ and Eora_ classification were extracted from the respective databases.
For Eora_, the names are based on the 'Country names' csv file provided on the webpage, but
updated for different names used in the Eora26 database. The MESSAGE 
classification follows the 11-region aggregation given in the MESSAGE_ model 
regions description. The IMAGE_ classification is based on the "`region 
classification map`_", for REMIND_ we received a country mapping from the model 
developers. 
The membership of OECD_ and UN_ can be found at the membership organisations' webpages, 
information about obsolete country codes on the Statoids_ webpage.
The situation for the EU_ got complicated due to the Brexit process. For the 
naming, coco follows the `Eurostat glossary`_, thus EU27 refers to the EU 
without UK, whereas EU27_2007 refers to the EU without Croatia (the status 
after the 2007 enlargement). The shortcut EU always links to the most recent 
classification. The EEA_ agreements are still valid for the UK (status September 2020, Brexit transition period - as `described here  <https://en.wikipedia.org/wiki/European_Economic_Area>`_), thus UK is currently included in the EEA.

.. _unstats: http://unstats.un.org/unsd/methods/m49/m49regin.htm
.. _OECD: http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm
.. _UN: http://www.un.org/en/members/
.. _EU: https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:EU_enlargements
.. _Schengen: https://en.wikipedia.org/wiki/Schengen_Area
.. _`Eurostat glossary`: https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:EU_enlargements
.. _EEA: https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:European_Economic_Area_(EEA)
.. _EXIOBASE: http://exiobase.eu/
.. _WIOD: http://www.wiod.org/home
.. _Eora: http://www.worldmrio.com/
.. _MESSAGE: http://www.iiasa.ac.at/web/home/research/researchPrograms/Energy/MESSAGE-model-regions.en.html
.. _Statoids: http://www.statoids.com/w3166his.html
.. _Cecilia: https://cecilia2050.eu/system/files/De%20Koning%20et%20al.%20%282014%29_Scenarios%20for%202050_0.pdf
.. _APEC: https://en.wikipedia.org/wiki/Asia-Pacific_Economic_Cooperation
.. _BRIC: https://en.wikipedia.org/wiki/BRIC 
.. _BASIC: https://en.wikipedia.org/wiki/BASIC_countries
.. _CIS: https://en.wikipedia.org/wiki/Commonwealth_of_Independent_States
.. _G7: https://en.wikipedia.org/wiki/Group_of_Seven
.. _G20: https://en.wikipedia.org/wiki/G20
.. _IMAGE: https://models.pbl.nl/image/index.php/Welcome_to_IMAGE_3.0_Documentation
.. _REMIND: https://www.pik-potsdam.de/en/institute/departments/transformation-pathways/models/remind
.. _`region classification map`: https://models.pbl.nl/image/index.php/Region_classification_map
.. _FAOcode: http://www.fao.org/faostat/en/#definitions


Communication, issues, bugs and enhancements
--------------------------------------------

Please use the issue tracker for documenting bugs, proposing enhancements and all other communication related to coco.

You can follow me on twitter_ to get the latest news about all my open-source and research projects (and occasionally some random retweets).

.. _twitter: https://twitter.com/kst_stadler

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

Stadler, K. (2017). The country converter coco - a Python package for converting country names between different classification schemes. The Journal of Open Source Software. doi: `10.21105/joss.00332 <http://dx.doi.org/10.21105/joss.00332>`_

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
