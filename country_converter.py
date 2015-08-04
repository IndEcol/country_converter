""" country_converter - Converting countries from one code/classification to another

KST 20150803
"""

import os
import sys
import re
import pandas as pd
import logging

SEP = '\t'
COUNTRY_DATA_FILE = os.path.join(
        os.path.split(os.path.abspath(__file__))[0],
        'country_data.txt'
        )


def match(list_A, list_B, not_found = 'not_found', enforce_sublist = False):
    """ Matches the country names given in two lists into a dictionary.

    This function matches names given in list_A to the one provided in list_B using 
    regular expressions defined in country_data.txt

    Parameters
    ----------
    list_A : list
        Names of countries to identify
    list_B : list
        Master list of names for coutnries
        

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value (default: 'not found')


    enforce_sublist : boolean, optional
        If True, all entries in both list are list. 
        If False(default), only multiple matches are list, rest are strings

    Returns
    -------
    dict:
        A dictionary with a key for every entry in list_A. The value
        correspond to the matching entry in list_B if found. If there is 
        a 1:1 correspondence, the value is a str (if enforce_sublist is False),
        otherwise multiple entries as list.

    """
    if type(list_A) is str: list_A = [list_A]
    if type(list_B) is str: list_B = [list_B]

    cc = CountryConverter()

    name_dict_A = dict()
    match_dict_A = dict()

    for name_A in list_A:

        name_dict_A[name_A] = []
        match_dict_A[name_A] = []

        for regex in cc.regexes:
            if(regex.search(name_A)):
                match_dict_A[name_A].append(regex)

        if len(match_dict_A[name_A]) == 0:
            logging.warn('Could not identify {} in list_A'.format(name_A))
            _not_found_entry = name_A if not not_found else not_found
            name_dict_A[name_A].append(_not_found_entry)
            if not enforce_sublist: name_dict_A[name_A] = name_dict_A[name_A][0]
            continue

        if len(match_dict_A[name_A]) > 1:
            logging.warn('Multiple matches for name {} in list_A'.format(name_A))

        for match in match_dict_A[name_A]:
            B_matches = 0
            for name_B in list_B:
                if(match.search(name_B)):
                    B_matches+=1
                    name_dict_A[name_A].append(name_B)

        if B_matches == 0:
            logging.warn('Could not find any correspondence for {} in list_B'.format(name_A))
            _not_found_entry = name_A if not not_found else not_found
            name_dict_A[name_A].append(_not_found_entry)

        if B_matches > 1:
            logging.warn('Multiple matches for name {} in list_B'.format(name_A))

        if not enforce_sublist and (len(name_dict_A[name_A]) == 1):
            name_dict_A[name_A] = name_dict_A[name_A][0]

    return name_dict_A


def convert(**parameters):
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
        Output classification (valid str or list of string of the country_data.txt), defalut: name_standard

    enforce_list : boolean, optional
        If True, enforces the output to be list (if only one name was passed) or to 
        be a list of lists (if multiple names were passed).
        If False (default), the output will be a string (if only one name was passed) or
        a list of str and/or lists (str if a one to one matching, list otherwise).

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value (default: 'not found')

    Returns
    -------
    list or str, depending on enforce_list


    """

    cc = CountryConverter()
    return cc.convert(**parameters)


class CountryConverter():
    """ Main class for converting countries

    Attributes
    ----------

    data : pandas DataFrame
        Raw data read from country_data.txt

    """
    def __init__(self):
       self.data = pd.read_table(COUNTRY_DATA_FILE, sep = SEP, encoding = 'utf-8')
       self.regexes = [re.compile(entry, re.IGNORECASE) for entry in self.data.regex]

    def convert(self, names, src = None, to = 'name_standard', enforce_list = False, not_found = 'not found'):
        """ Convert names from a list to another list.

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
            Output classification (valid str or list of string of the country_data.txt), defalut: name_standard

        enforce_list : boolean, optional
            If True, enforces the output to be list (if only one name was passed) or to 
            be a list of lists (if multiple names were passed).
            If False (default), the output will be a string (if only one name was passed) or
            a list of str and/or lists (str if a one to one matching, list otherwise).

        not_found : str, optional
            Fill in value for not found entries. If None, keep the input value (default: 'not found')

        Returns
        -------
        list or str, depending on enforce_list

        """
        if type(names) is str: names = [names]
        outlist = names.copy()
        if type(to) is str: to = [to]

        if src.lower() == 'regex':
            for ind_names, nn in enumerate(names):
                result_list = []
                for ind_regex, ccregex in enumerate(self.regexes):
                    if(ccregex.search(nn)):
                        _found = list(self.data.ix[ind_regex,to].values)
                        if len(_found) == 1 and enforce_list is False: _found = _found[0]
                        result_list.append(_found)
                if len(result_list) > 1:
                    logging.warning('More then one regular expression match for {}'.format(nn))
                    outlist[ind_names] = result_list
                elif len(result_list) < 1:
                    logging.warning('{} does not match any regular expression'.format(nn))
                    _fillin = not_found or nn
                    outlist[ind_names] = [_fillin] if enforce_list else _fillin
                else:
                    outlist[ind_names] = result_list if enforce_list else result_list[0]
            return outlist

        else:
            for ind, nn in enumerate(names):
                found = self.data[self.data[src].isin([nn])][to]
                if len(found) == 0:
                    logging.warn('{} not found in {}'.format(nn, src))
                    _fillin = not_found or nn
                    listentry = [_fillin] if enforce_list else _fillin
                else:
                    listentry = list(found.values[0])
                    if len(listentry) == 1 and enforce_list is False:
                        listentry = listentry[0]
                outlist[ind] = listentry
            return outlist

    def EU28in(self, to = 'name_standard'):
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

    def EU27in(self, to = 'name_standard'):
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
        if type(to) is str:
            to = [to]
        return self.data[self.data.EU < 2013][to]

    def OECDin(self, to = 'name_standard'):
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
        if type(to) is str:
            to = [to]
        return self.data[self.data.OECD > 0][to]

    def UNin(self, to = 'name_standard'):
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
        if type(to) is str:
            to = [to]
        return self.data[self.data.UNmember > 0][to]


    @property
    def EU28(self):
        """ EU28 memberstates (standard name) - use EU28in() for any other classification """
        return self.EU28in(to = 'name_standard')

    @property
    def EU27(self):
        """ EU27 memberstates (standard name) - use EU27in() for any other classification """
        return self.EU27in(to = 'name_standard')

    @property
    def OECD(self):
        """ OECD memberstates (standard name) - use OECDin() for any other classification """
        return self.OECDin(to = 'name_standard')

    @property
    def UN(self):
        """ UN memberstates (standard name) - use UNin() for any other classification """
        return self.UNin(to = 'name_standard')

    @property
    def valid_class(self):
        """ Valid strings for the converter """
        return list(self.data.columns)

