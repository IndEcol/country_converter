country converter
=================

The country converter (coco) is a Python package to convert country names between different classifications and between different naming versions. Internally it uses regular expressions to match country names.

.. image:: https://travis-ci.org/konstantinstadler/country_converter.svg?branch=master
    :target: https://travis-ci.org/konstantinstadler/country_converter

Installation
------------

Country_converter is registered at PyPI. From the command line:

::

    pip install country_converter

Alternatively, the source code is available on github_.

.. _github: https://github.com/konstantinstadler/country_converter

The package depends on pandas_; for testing py.test_ is required.

.. _pandas: http://pandas.pydata.org/

.. _py.test: http://pytest.org/ 

Usage
-----

Basic usage
^^^^^^^^^^^

Use within python
"""""""""""""""""

Convert various country names to some standard names:

::

    import country_converter as coco
    some_names = ['United Rep. of Tanzania', 'Cape Verde', 'Burma', 'Iran (Islamic Republic of)', 'Korea, Republic of', "Dem. People's Rep. of Korea"]
    standard_names = coco.convert(names=some_names, to='name_short')
    print(standard_names)

Which results in ['Tanzania', 'Cabo Verde', 'Myanmar', 'Iran', 'South Korea', 'North Korea'].

In case of multiple conversion, better performance can be achieved by
instantiating a single CountryConverter object for all conversions:

::

    import country_converter as coco
    cc = coco.CountryConverter()

    some_names = ['United Rep. of Tanzania', 'Cape Verde', 'Burma', 'Iran (Islamic Republic of)', 'Korea, Republic of', "Dem. People's Rep. of Korea"]

    standard_names = cc.convert(names = some_names, src = 'regex', to = 'name_short') 
    UNmembership = cc.convert(names = some_names, src = 'regex', to = 'UNmember') 
    print(standard_names)
    print(UNmembership)


Convert between classification schemes:

::

    iso3_codes = ['USA', 'VUT', 'TKL', 'AUT' ]
    iso2_codes = coco.convert(names = iso3_codes, src = 'ISO3', to = 'ISO2')
    print(iso2_codes)

Which results in ['US', 'VU', 'TK', 'AT']

Internally the data is stored in a pandas dataframe, which can be accessed directly. 
For example, this can be used to filter countries for membership organisations (per year). 
Note: for this, an instance of CountryConverter is required.

::

    import country_converter as coco
    cc = coco.CountryConverter()

    some_countries = ['Australia', 'Belgium', 'Brazil', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'India', 'Indonesia', 'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Romania', 'Russia',  'Turkey', 'United Kingdom', 'United States']

    oecd_since_1995 = cc.data[(cc.data.OECD >= 1995) & cc.data.name_short.isin(some_countries)].name_short
    eu_until_1980 = cc.data[(cc.data.EU <= 1980) & cc.data.name_short.isin(some_countries)].name_short
    print(oecd_since_1995)
    print(eu_until_1980)

Some properties provide direct access to affiliations:

::

    cc.EU28
    cc.OECD

    cc.EU27in('ISO3')

and the classification schemes available:

::

    cc.valid_class


The regular expressions can also be used to match any list of countries to any other. For example: 

::

    match_these = ['norway', 'united_states', 'china', 'taiwan']
    master_list = ['USA', 'The Swedish Kingdom', 'Norway is a Kingdom too', 'Peoples Republic of China', 'Republic of China' ]

    matching_dict = coco.match(match_these, master_list)


See the IPython Notebook (country_converter_examples.ipynb_) for more information.

.. _country_converter_examples.ipynb: http://nbviewer.ipython.org/github/konstantinstadler/country_converter/blob/master/doc/country_converter_examples.ipynb

Command line usage    
""""""""""""""""""""""

The country converter package also provides a command line interface
called coco.

Minimal example:

:: 
    
    coco Cyprus Denmark Estonia 'United Kingdom' 

Converts the given names to ISO3 codes based on regular expression matching.
The list of names must be separated by spaces, country names consisting of multiple words must be put in quotes ('').

The input classification can be specified with '--src' or '-s', the target classification with '--to' or '-t'.

The default output is a space separated list, this can be changed by passing a separator by '--output_sep' or '-o'.

Thus, to convert from ISO3 to UN number codes and receive the output as comma separated list use:

::

    coco AUT DEU VAT AUS -s ISO3 -t UNcode -o ', '
    

For further information call the help by

::

    coco -h


Use in matlab
""""""""""""""""""""""

Newer (tested in 2016a) versions from Matlab allow to directly call python
functions and libaries.  This requires a python version >= 3.4 installed in the
sytem path (e.g. through Anaconda).

To test, try this in matlab:

::
    
    py.print(py.sys.version)
    
If this works, you can also use coco after installing it through pip 
(at the windows commandline - see the installing instruction above):

::
    
    pip install country_converter
    
And in matlab:

::

    coco = py.country_converter.CountryConverter()
    countries = {'The Swedish Kingdom', 'Norway is a Kingdom too', 'Peoples Republic of China', 'Republic of China'};
    ISO2_pythontype = coco.convert(countries, pyargs('to', 'ISO2'));
    ISO2_cellarray = cellfun(@char,cell(ISO2_pythontype),'UniformOutput',false);
    

Alternativley, as a long oneliner:
   
::

    short_names = cellfun(@char, cell(py.country_converter.convert({56, 276}, pyargs('src', 'UNcode', 'to', 'name_short'))), 'UniformOutput',false);

All properties of coco as explained above are also available in matlab:    

::
    
    coco = py.country_converter.CountryConverter();
    coco.EU27
    EU27ISO3 = coco.EU27in('ISO3');

These functions return a pandas DataFrame. 
The underlying values can be access with .values (e.g. 

::

    EU27ISO3.values

I leave it to professional matlab users to figure out how to further process them.
    

Refining and Extending
^^^^^^^^^^^^^^^^^^^^^^

The underlying raw data is a tab-separated file (country_data.txt) which is read into a pandas dataframe (available as attribute .data in the main class).
Any column added to this dataframe can be used for all conversions. The datafile is utf-8 encoded.

The included regular expressions were tested against names commonly found in various databases. In case the expression need to be updated rerun all tests (using the _py.test package). 

These tests check 

#) Do the short names uniquely match the regular expression?
#) Do the official name uniquely match the regular expression?
#) Do the alternative names tested so far still uniquely match the standard names?

To specify a new test set just add a tab-separated file with headers "name_short" and "name_test" and provide name (corresponding to the short name in the main classification file) and the alternative name which should be tested (one pair per row in the file). If the file name starts with "test\_regex\_" it will be automatically recognised by the test functions.


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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most of the underlying data can be found in Wikipedia.
https://en.wikipedia.org/wiki/ISO_3166-1 is a good starting point.
UN regions/codes are given on the United Nation Statistical Division (unstats_) web-page.
EXIOBASE_ and WIOD_ classification were extracted from the respective databases.
The membership of OECD_, UN_ and EU_ can be found at the membership organisations webpages. 

.. _unstats: http://unstats.un.org/unsd/methods/m49/m49regin.htm
.. _OECD: http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm
.. _UN: http://www.un.org/en/members/
.. _EU: http://europa.eu/about-eu/countries/index_en.htm
.. _EXIOBASE: http://exiobase.eu/ 
.. _WIOD: http://www.wiod.org/new_site/home.htm 

Acknowledgements
----------------

This package was inspired by (and the regular expression are mostly based on) the R-package countrycode_ by Julian_ Hinz and its port to Python (pycountrycode_) by Vincent_ Arel-Bundock.

.. _Julian: http://julianhinz.com/
.. _countrycode: https://github.com/julianhinz/countrycode
.. _Vincent: http://arelbundock.com/
.. _pycountrycode: http://github.com/vincentarelbundock/pycountrycode



