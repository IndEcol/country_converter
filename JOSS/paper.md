---
title: The country converter coco - a Python package for converting country names between different classification schemes. 

tags:
  - country classifications
  - regular expressions
  - geography
authors:
 - name: Konstantin Stadler
   orcid: 0000-0002-1548-201X
   affiliation: 1
affiliations:
 - name: Industrial Ecology Programme, NTNU Trondheim, Norway. 
   index: 1
date: 12 July 2017
bibliography: paper.bib
---

# Summary


To date, several competing standards exist for country abbreviations. This
hinders the automatic parsing of data, in particular for the construction of globally
spanning models and databases as for example Multi Regional Input Output Models
(@tukker_global_2013). 

Of the existing standards, ISO 3166-1 (see @_iso_2017) defines a two and a
three letter code in addition to a numerical classification. The UN uses its
own numerical classification scheme, mostly based on the ISO 3166-1 numerical
code. To further complicate the matter, several other databases use their own country
names to classify countries.

To ease the conversion between various forms of country names and different
classification schemes, I developed the country converter (coco) in python 3.
Coco converts a given country name or ISO/UN code to a specified output format.

The basis of coco is a table of regular expression which match all English
versions of country names encountered by the author. The included tests match
these regular expression against all found names, checking for unique matching
between regular expression and country names and vice versa.

The table of regular expression and linked country names and classification can
be extended by passing additional tables to account for databases using
erroneous country codes or names.

In addition to the one to one matching, coco includes regional country
classifications based on continent, UN region, OECD membership (per year), UN
membership (per year), EU membership (per year) as well as classification of
the Rest of the World countries (@stadler_rest_2014) in the Multi Regional
Input Output Databases EXIOBASE (@wood_global_2014) and WIOD
(@timmer_world_2012).

Coco can be used in Python and also provides a command line interface. Examples
of how to use coco in Matlab(c) are provided in the readme. An accompanying
ipython notebook provides some instruction for advanced usage. 


# References
