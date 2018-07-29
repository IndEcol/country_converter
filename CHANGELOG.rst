Change Log
===========

0.6.5 - 20180309
-----------------

Coco now includes as switch for including obsolete countries (off by default),
see https://github.com/konstantinstadler/country_converter#classification-schemes

Further improved test coverage


0.6.4 - 20180308
-----------------

Improved test coverage
Changed ISO3 for Kosovo from KSV to XKV


0.6.3 - 20180105
-----------------

Switched ROW in WIOD to RoW


0.6.2 - 20180105
-----------------

Switched WIOD country names to upper case to fit the WIOD database case


0.6.1 - 20180102
-----------------

Minor spelling fixes

0.6.0 - 20180102
-----------------

Aggregation concordance building functionality with

  - method get_correspondance_dict in CountryConverter
  - function agg_conc which build concordance matrices in various formats
  - notebook tutorial

Include Eora(26) country codes

CountryConverter accepts a parameter only_UNmember to restrict the concordances to UN member countries.

Fix and close Issue #28 (Wrong ISO3 code for Palestine) and #25 (Non-standard codes).

0.5.4 - 20170922
----------------

Corrected Palestine ISO3 code to PSE

0.5.3 - 20170811
----------------

Minor bugfixes with UN codes and regions.

Fixing issue 22 and 23

0.5.2 - 20170807
----------------

Changed Futuna and Sahara to Uppercase


0.5.1 - 20170803
----------------

Minor update, added the citation for the JOSS article.


0.5.0 - 20170802
----------------

This is the version after the review for publication in The Journal of Open Source Software. 

Changed
^^^^^^^

    * Renamed XXin methods to XXas. For example coco.EU27in('ISO3') becomese coco.EU27as('ISO3')
    * Some updates in README.rst (related software, badges, motivation)
    * Added CONTRIBUTING.rst


0.4.0 - 20170622
----------------

This version is available at Zenodo at 10.5281/zenodo.838036 .

Changed
^^^^^^^

    * Added CHANGELOG
    * Updated docstrings
    * Account for cases where countries or regions are specified with 'exclude ...'
    * Possibility to add custom countryfile for own mappings
    * Not found value can be specified also in the CLI version
    * Automatically detect input format (ISO2, ISO3, ISOnumeric)
    * Change ISO3 for Romania from ROM to ROU (bugfix)
    * Change ISO3 for Congo from COD to COG (bugfix)
    * Updated readme and IPython notebook tutorial


pre 0.4.0 - before 20170501
----------------------------

Initial versions, including CLI and matlab examples.


