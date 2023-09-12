# Changelog

## 1.0.1dev

### Development

- removed htmlcov

### Classifications

- Correct spelling "Faeroe Islands" to "Faroe Islands" #145 (by @jpatokal)


## 1.0.0

### Classifications

- fix Myanmar UN region (#125) [by Alan Orth]
- add missing MESSAGE R11 regions [by Advait]
- added Croatia to the Euro list [by PeterMaxwell]


### Development

- droped 3.6 support, added tests for 3.10 and 3.11
- fixed github workflow
- change repository from github.com/konstantinstadler to github.com/IndEcol
- Add build-system requirements and isort configuration to pyproject.toml [by Mike Taves]


## 0.8.0


### Classifications

- added Costa Rica as new OECD member (2021), fix #118 
- added GWCodes, https://www.tandfonline.com/doi/abs/10.1080/03050629908434958
- added ccTLD (country top-level domains) via @plotski  
- updated EEA (remove UK, Switzerland)
- rename Turkey to Türkiye

### Bug fixes

- fix UN M.49 names 


### Development

- added pandas-convert (via @jim-rivera) for faster conversion of pandas series


## 0.7.7 - 20220805


### Bug fixes

- ISO2 did return the regex for GB|UK - fix #113


## 0.7.6 - 20220802

### Breaking

- additional data must specify ISO2 (necessary for regex matching in ISO2)


### Classifications

- added DACcode (pull request by @jm-rivera)

### Bug fixes

- N Korea matches North Korea - fix #95

### Development

- All rst files (readme, changelog, etc. format changed to markdown
- ISO2 column accepts regex - fix #92


## 0.7.5 - 20220802

### Classifications

-   Changed name from Republic of Turkey to Republic of Türkiye (see
    <https://en.wikipedia.org/wiki/Turkey> ).
-   Changed Macedonia to North Macedonia (following the Prespa
    agreement: <https://en.wikipedia.org/wiki/Prespa_agreement>).

### Bug Fixes

-   Escape characters in country names to allow for names with special
    symbols (brackets) in regex (#101)
-   Updated regex of India to exclude Bassas Da India (#111)

### Development

-   Minimum required version of Black is 22.3.0

## 0.7.4 - 20211118

### Classifications

-   added IEA classification (by @Kajwan\]

### Development

-   changed development environment to python 3.9
-   change github actions testing to development -\> production for
    multiple os
-   added link to example script on how to parse data for adding a new
    classification:
    <https://gist.github.com/konstantinstadler/dc3583a4674a39def0d4611c095eb788>

## 0.7.3 - 20210409

### Classifications

-   added GBDcode (numerical Global Burden of Disease codes)

### Bug Fixes

-   Update for regex for several regions which erroneous matched
    countries (solves #86)
-   CLI help fix (solves #81)
-   Added HKSAR for Hong Kong, N.Korea for North Korea and some Macaou
    tests (solves #84)
-   Fixed for pandas Series inputs (solves #54)
-   Fixed aggregation concordance (solves #82)
-   Indiana does not match India

### Development

-   functionality for testing regions which should not match
-   handle pandas future regex warning
-   moved from travis to github actions for CI testing
-   restructured tests and added test for consistent CHANGELOG - module
    version

## 0.7.2 - 20210127

### Classifications

-   added FAOcode (numerical FAO code)

### API

-   added CountryConverter().valid_country_classifications which gives
    all country classifications (without any aggregation like continents
    or models)

### Bug Fixes

-   French Guyana resettled to America (was Africa before) (fixes #76)
-   D.P.R of Korea resolves to North Korea (fixes #79)

## 0.7.1 - 20201014

### Classifications

-   added 2020 OECD membership for Colombia

### Misc

-   changed the description for installing from conda forge
-   updated contributing.rst
-   explained logging settings in the readme

## 0.7.0 - 20200925

### Breaking

-   removed support for python 3.5
-   minimum pandas version = 1.0
-   The classifications for the EU are now based on names (EU27, EU15,
    ...) - the years have been removed (Brexit had made this necessary).
-   The output of the class level attributes and methods for the
    classifications (e.g. coco.OECD or coco.EXIO3as()) has changed
-   The standard output of the command line changed from ISO3 to short
    names, pass --to=ISO3 for the previous behaviour

### Classifications

-   Added EU12, EU15, EU25, EU27_2007, EU28 and EU27 classification.
    This follows the names as explained here
    <https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:EU_enlargements>
-   The classification EU is linked to EU27 (thus status after Brexit)
-   The classification UN is a shortcut for UNmember
-   Added IAM IMAGE and REMIND classifications
-   Added EEA, for now including UK as it is still in place
-   Added Schengen region classification
-   Updated Lithuania OECD membership
-   fixed Ireland, UK, US regex problems - UK, GB and US are now
    included in the regex search term
-   changed official name of Macao to Macau

### Internals

-   Adding class level attributes for the shortcuts to the
    classifications is now automated
-   multiple bug and spelling fixes
-   using black and isort for the code style
-   logger used in the country_converter is named (based on module
    \_\_name\_\_)
-   re-established test coverage

## 0.6.7 - 20191011

-   fixed various country spellings

-   Calling the command line (coco) without arguments prints help
    message

-   Deprecated pandas methods (ix, read_table) replaced

-   CLI interface allows to  
    -   include obsolete countries (--include_obsolete, -i)
    -   restrict to only UN membersstates (--UNmember_only, -u)
    -   return classifications (e.g. coco OECD or coco EXIO1)

-   Extended classification helper

## 0.6.6 - 20180729

-   Added Cecilia2050 classification (merging pull request #36 (with
    some futher modifications)
-   Changing Swaziland to Eswatini, following the official name change
    in April 2018
    (<https://unterm.un.org/UNTERM/Display/Record/UNHQ/NA/01b637e1-1497-4825-b73d-e0114a7f4d22>
    …). Closes issue #35
-   Removed space from McDonald in "Heard and Mc Donald Islands" and
    updated offical name to "Territory of Heard Island and McDonald
    Islands". Closes issus #34.

## 0.6.5 - 20180309

Coco now includes as switch for including obsolete countries (off by
default), see
<https://github.com/konstantinstadler/country_converter#classification-schemes>

Further improved test coverage

## 0.6.4 - 20180308

Improved test coverage Changed ISO3 for Kosovo from KSV to XKV

## 0.6.3 - 20180105

Switched ROW in WIOD to RoW

## 0.6.2 - 20180105

Switched WIOD country names to upper case to fit the WIOD database case

## 0.6.1 - 20180102

Minor spelling fixes

## 0.6.0 - 20180102

Aggregation concordance building functionality with

> -   method get_correspondance_dict in CountryConverter
> -   function agg_conc which build concordance matrices in various
>     formats
> -   notebook tutorial

Include Eora(26) country codes

CountryConverter accepts a parameter only_UNmember to restrict the
concordances to UN member countries.

Fix and close Issue #28 (Wrong ISO3 code for Palestine) and #25
(Non-standard codes).

## 0.5.4 - 20170922

Corrected Palestine ISO3 code to PSE

## 0.5.3 - 20170811

Minor bugfixes with UN codes and regions.

Fixing issue 22 and 23

## 0.5.2 - 20170807

Changed Futuna and Sahara to Uppercase

## 0.5.1 - 20170803

Minor update, added the citation for the JOSS article.

## 0.5.0 - 20170802

This is the version after the review for publication in The Journal of
Open Source Software.

### Changed

> -   Renamed XXin methods to XXas. For example coco.EU27in('ISO3')
>     becomese coco.EU27as('ISO3')
> -   Some updates in README.rst (related software, badges, motivation)
> -   Added CONTRIBUTING.rst

## 0.4.0 - 20170622

This version is available at Zenodo at 10.5281/zenodo.838036 .

### Changed

> -   Added CHANGELOG
> -   Updated docstrings
> -   Account for cases where countries or regions are specified with
>     'exclude ...'
> -   Possibility to add custom countryfile for own mappings
> -   Not found value can be specified also in the CLI version
> -   Automatically detect input format (ISO2, ISO3, ISOnumeric)
> -   Change ISO3 for Romania from ROM to ROU (bugfix)
> -   Change ISO3 for Congo from COD to COG (bugfix)
> -   Updated readme and IPython notebook tutorial

## pre 0.4.0 - before 20170501

Initial versions, including CLI and matlab examples.
