#!/usr/bin/env python3
""" country_converter - Classification converter for coutries

"""

import argparse
import logging
import os
import re
import pandas as pd


def match(list_a, list_b, not_found='not_found', enforce_sublist=False):
    """ Matches the country names given in two lists into a dictionary.

    This function matches names given in list_a to the one provided in list_b
    using regular expressions defined in country_data.txt

    Parameters
    ----------
    list_a : list
        Names of countries to identify
    list_b : list
        Master list of names for coutnries

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value
        (default: 'not found')

    enforce_sublist : boolean, optional
        If True, all entries in both list are list.
        If False(default), only multiple matches are list, rest are strings

    Returns
    -------
    dict:
        A dictionary with a key for every entry in list_a. The value
        correspond to the matching entry in list_b if found. If there is
        a 1:1 correspondence, the value is a str (if enforce_sublist is False),
        otherwise multiple entries as list.

    """
    if isinstance(list_a, str):
        list_a = [list_a]
    if isinstance(list_b, str):
        list_b = [list_b]
    if isinstance(list_a, tuple):
        list_a = list(list_a)
    if isinstance(list_b, tuple):
        list_b = list(list_b)

    coco = CountryConverter()

    name_dict_a = dict()
    match_dict_a = dict()

    for name_a in list_a:

        name_dict_a[name_a] = []
        match_dict_a[name_a] = []

        for regex in coco.regexes:
            if regex.search(name_a):
                match_dict_a[name_a].append(regex)

        if len(match_dict_a[name_a]) == 0:
            logging.warning('Could not identify {} in list_a'.format(name_a))
            _not_found_entry = name_a if not not_found else not_found
            name_dict_a[name_a].append(_not_found_entry)
            if not enforce_sublist:
                name_dict_a[name_a] = name_dict_a[name_a][0]
            continue

        if len(match_dict_a[name_a]) > 1:
            logging.warning(
                'Multiple matches for name {} in list_a'.format(name_a))

        for match_case in match_dict_a[name_a]:
            b_matches = 0
            for name_b in list_b:
                if match_case.search(name_b):
                    b_matches += 1
                    name_dict_a[name_a].append(name_b)

        if b_matches == 0:
            logging.warning(
                'Could not find any '
                'correspondence for {} in list_b'.format(name_a))
            _not_found_entry = name_a if not not_found else not_found
            name_dict_a[name_a].append(_not_found_entry)

        if b_matches > 1:
            logging.warning('Multiple matches for '
                            'name {} in list_b'.format(name_a))

        if not enforce_sublist and (len(name_dict_a[name_a]) == 1):
            name_dict_a[name_a] = name_dict_a[name_a][0]

    return name_dict_a


def convert(*args, **kargs):
    """ Wraper around CountryConverter.convert()

    Uses the same paramter. This function has the same performance as
    CountryConverter.convert for one call; for multiple calls its better to
    instantiate a common CountryConverter (this avoid loading the source data
    file multiple times).

    Note
    ----
    A lot of the functioality can also be done directly in pandas dataframes.
    For example:
    cc = CountryConverter()
    names = ['USA', 'SWZ', 'PRI']
    cc.data[cc.data['ISO3'].isin(names)][['ISO2', 'continent']]

    Parameters
    ----------
    names : str or list like
        Countries in 'src' classification to convert to 'to' classification

    src : str, optional
        Source classification

    to : str or list, optional
        Output classification (valid str or list of string of the
        country_data.txt), defalut: name_short

    enforce_list : boolean, optional
        If True, enforces the output to be list (if only one name was passed)
        or to be a list of lists (if multiple names were passed).  If False
        (default), the output will be a string (if only one name was passed) or
        a list of str and/or lists (str if a one to one matching, list
        otherwise).

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value
        (default: 'not found')

    Returns
    -------
    list or str, depending on enforce_list

    """

    coco = CountryConverter()
    return coco.convert(*args, **kargs)


class CountryConverter():
    """ Main class for converting countries

    Attributes
    ----------

    data : pandas DataFrame
        Raw data read from country_data.txt

    """

    def __init__(self):
        country_data_file = os.path.join(
            os.path.split(os.path.abspath(__file__))[0],
            'country_data.txt'
        )

        self.data = pd.read_table(country_data_file, sep='\t',
                                  encoding='utf-8')
        self.regexes = [re.compile(entry, re.IGNORECASE)
                        for entry in self.data.regex]

        must_be_unique = ['name_short', 'name_official', 'regex']
        for name_entry in must_be_unique:
            if self.data[name_entry].duplicated().any():
                logging.error(
                    'Duplicated values in column {}'.format(name_entry))

    def convert(self, names, src=None, to=None, enforce_list=False,
                not_found='not found'):
        """ Convert names from a list to another list.

        Note
        ----
        A lot of the functioality can also be done directly in pandas
        dataframes.
        For example:
        coco = CountryConverter()
        names = ['USA', 'SWZ', 'PRI']
        coco.data[coco.data['ISO3'].isin(names)][['ISO2', 'continent']]

        Parameters
        ----------
        names : str or list like
            Countries in 'src' classification to convert
            to 'to' classification

        src : str, optional
            Source classification. Assumed to be regular
            expression if None (default)

        to : str or list, optional
            Output classification (valid str or list of
            string of the country_data.txt), defalut: ISO3

        enforce_list : boolean, optional
            If True, enforces the output to be list (if only one name was
            passed) or to be a list of lists (if multiple names were passed).
            If False (default), the output will be a string (if only one name
            was passed) or a list of str and/or lists (str if a one to one
            matching, list otherwise).

        not_found : str, optional
            Fill in value for not found entries. If None, keep the input value
            (default: 'not found')

        Returns
        -------
        list or str, depending on enforce_list

        """
        if isinstance(names, str):
            names = [names]
        # The list to tuple conversion is necessary for a convenient matlab
        # interface
        if isinstance(names, tuple):
            names = list(names)
        outlist = names.copy()

        if src is None:
            src = 'regex'
        if to is None:
            to = 'ISO3'

        if isinstance(to, str):
            to = [to]

        if src.lower() == 'regex':
            for ind_names, spec_name in enumerate(names):
                result_list = []
                for ind_regex, ccregex in enumerate(self.regexes):
                    if ccregex.search(spec_name):
                        result_list.append(
                            self.data.ix[ind_regex, to].values[0])
                if len(result_list) > 1:
                    logging.warning(
                        'More then one regular expression '
                        'match for {}'.format(spec_name))
                    outlist[ind_names] = result_list
                elif len(result_list) < 1:
                    logging.warning(
                        '{} does not match any '
                        'regular expression'.format(spec_name))
                    _fillin = not_found or spec_name
                    outlist[ind_names] = [_fillin] if enforce_list else _fillin
                else:
                    outlist[ind_names] = (result_list if
                                          enforce_list else result_list[0])

        else:
            for ind, spec_name in enumerate(names):
                try:
                    spec_name = int(spec_name)
                except ValueError:
                    pass
                found = self.data[self.data[src].isin([spec_name])][to]
                if len(found) == 0:
                    logging.warning(
                        '{} not found in {}'.format(spec_name, src))
                    _fillin = not_found or spec_name
                    listentry = [_fillin] if enforce_list else _fillin
                else:
                    listentry = list(found.values[0])
                    if len(listentry) == 1 and enforce_list is False:
                        listentry = listentry[0]
                outlist[ind] = listentry

        outlist = ['{:.0f}'.format(spec_name) if isinstance(spec_name, float)
                   else str(spec_name) for spec_name in outlist]

        if (len(outlist) == 1) and not enforce_list:
            return outlist[0]
        else:
            return outlist

    def EU28in(self, to='name_short'):
        """
        Return EU28 countries in the specified classification

        Parameters
        ----------
        to : str or list
            Valid column header (first row of country_data.txt).

        Returns
        -------
        pandas dataframe

        """
        if type(to) is str:
            to = [to]
        return self.data[self.data.EU < 2015][to]

    def EU27in(self, to='name_short'):
        """
        Return EU27 countries in the specified classification

        Parameters
        ----------
        to : str or list
            Valid column header (first row of country_data.txt).

        Returns
        -------
        pandas dataframe

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.EU < 2013][to]

    def OECDin(self, to='name_short'):
        """
        Return OECD memberstates in the specified classification

        Parameters
        ----------
        to : str or list
            Valid column header (first row of country_data.txt).

        Returns
        -------
        pandas dataframe

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.OECD > 0][to]

    def UNin(self, to='name_short'):
        """
        Return UN memberstates in the specified classification

        Parameters
        ----------
        to : str or list
            Valid column header (first row of country_data.txt).

        Returns
        -------
        pandas dataframe

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.UNmember > 0][to]

    @property
    def EU28(self):
        """ EU28 memberstates (standard name_short) -
            use EU28in() for any other classification
        """
        return self.EU28in(to='name_short')

    @property
    def EU27(self):
        """ EU27 memberstates (standard name_short) -
            use EU27in() for any other classification
        """
        return self.EU27in(to='name_short')

    @property
    def OECD(self):
        """ OECD memberstates (standard name_short) -
            use OECDin() for any other classification
        """
        return self.OECDin(to='name_short')

    @property
    def UN(self):
        """ UN memberstates (standard name_short) -
        use UNin() for any other classification
        """
        return self.UNin(to='name_short')

    @property
    def valid_class(self):
        """ Valid strings for the converter """
        return list(self.data.columns)


def _parse_arg(valid_classifications):
    """ Command line parser for coco

    Parameters
    ----------

    valid_classifications: list
        Available classifications, used for checking input parameters.

    Returns
    -------

    args : ArgumentParser namespace
    """

    parser = argparse.ArgumentParser(
        description=('The country converter (coco): a Python package for '
                     'converting country names between '
                     'different classifications schemes. '
                     'Version: {}'.format('0.2')
                     ), prog='coco', usage=('%(prog)s --names --src --to]'))

    parser.add_argument(
        'names',
        help=('List of countries to convert '
              '(comma or space separated, country names consisting of '
              'multiple words must be put in quoation marks). '
              'Possible classifications: ' +
              ', '.join(valid_classifications) +
              '; NB: long, official and short are provided as shortcuts '
              'for the names classifications'
              ), nargs='*')

    parser.add_argument(
        '-s', '--src', '--source', '-f', '--from',
        help='Classification of the names given, (default: "regex")')
    parser.add_argument(
        '-t', '--to',
        help='Required classification of the passed names (default: "ISO3"')
    parser.add_argument('-o', '--output_sep',
                        help=('Seperator for output names '
                              '(default: space), e.g. "," '))

    args = parser.parse_args()
    args.src = args.src or 'regex'
    args.to = args.to or 'ISO3'
    args.output_sep = args.output_sep or ' '
    args.names = [nn.replace(',', ' ') for nn in args.names]

    if 'short' in args.src.lower():
        args.src = 'name_short'
    if 'official' in args.src.lower():
        args.src = 'name_official'
    if 'long' in args.src.lower():
        args.src = 'name_official'
    if args.src.lower() == 'name' or args.src.lower() == 'names':
        args.src = 'name_short'
    if 'short' in args.to.lower():
        args.to = 'name_short'
    if 'official' in args.to.lower():
        args.to = 'name_official'
    if 'long' in args.to.lower():
        args.to = 'name_official'
    if args.to.lower() == 'name' or args.to.lower() == 'names':
        args.to = 'name_short'

    if args.src not in valid_classifications:
        raise TypeError('Source classifiction {} not available'.
                        format(args.src))
    if args.to not in valid_classifications:
        raise TypeError('Target classifiction {} not available'.
                        format(args.to))

    return args


def main():
    """ Main entry point - used for command line call
    """
    coco = CountryConverter()
    args = _parse_arg(coco.valid_class)
    converted_names = coco.convert(
        names=args.names,
        src=args.src,
        to=args.to)
    if isinstance(converted_names, str) or isinstance(converted_names, int):
        converted_names = [converted_names]

    print(args.output_sep.join(converted_names))


if __name__ == "__main__":
    try:
        main()

    except Exception as excep:
        logging.exception(excep)
        raise
