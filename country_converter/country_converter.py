#!/usr/bin/env python3
""" country_converter - Classification converter for countries

"""

import argparse
import logging
import os
import re
from collections import OrderedDict
import pandas as pd
from country_converter.version import __version__

COUNTRY_DATA_FILE = os.path.join(
    os.path.split(os.path.abspath(__file__))[0], 'country_data.tsv')


def agg_conc(original_countries,
             aggregates,
             missing_countries='test',
             merge_multiple_string='_&_',
             log_missing_countries=None,
             log_merge_multiple_strings=None,
             coco=None,
             as_dataframe='sparse',
             original_countries_class=None):
    """ Builds an aggregation concordance dict, vec or matrix

    Parameters
    ----------

    original_countries: list or str
        List of countries to aggregated, also accepts and valid column name of
        CountryConverter.data

    aggregates: list of dict or str
        List of aggregation information. This can either be dict mapping the
        names of 'original_countries' to aggregates, or a valid column name of
        CountryConverter.data Aggregation happens in order given in this
        parameter.  Thus, country assigned to an aggregate are not re-assigned
        by the following aggregation information.

    missing_countries: str, boolean, None
        Entry to fill in for countries in 'original_countries' which do not
        appear in 'aggregates'.  str: Use the given name for all missing
        countries True: Use the name in original_countries for missing
        countries False: Skip these countries None: Use None for these
        countries

    merge_multiple_string: str or None, optional
        If multiple correspondance entries are given in one of the aggregates
        join them with the given string (default: '_&_'.  To skip these enries,
        pass None.

    log_missing_countries: function, optional
        This function is called with country is country is in
        'original_countries' but missing in all 'aggregates'.
        For example, pass
        lambda x: logging.error('Country {} missing'.format(x))
        to log errors for such countries.  Default: do nothing

    log_merge_multiple_strings: function, optional
        Function to call for logging multiple strings, see
        log_missing_countries Default: do nothing

    coco: instance of CountryConverter, optional
        CountryConverter instance used for the conversion.  Pass a custom one
        if additional data is needed in addition to the custom country
        converter file.  If None (default), the bare CountryConverter is used

    as_dataframe: boolean or st, optional
        If False, output as OrderedDict.  If True or str, output as pandas
        dataframe.  If str and 'full', output as a full matrix, otherwise only
        two collumns with the original and aggregated names are returned.

    original_countries_class: str, optional
        Valid column name of CountryConverter.data.  This parameter is needed
        if a list of countries is passed to 'orginal_countries' and strings
        corresponding to data in CountryConverter.data are used subsequently.
        Can be omitted otherwise.

    Returns
    -------

    OrderedDict or DataFrame (defined by 'as_dataframe')

    """

    if coco is None:
        coco = CountryConverter()

    if type(original_countries) is str:
        original_countries_class = original_countries
        original_countries = coco.data[original_countries].values
    else:
        original_countries_class = (original_countries_class or
                                    coco._get_input_format_from_name(
                                        original_countries[0]))

    if type(aggregates) is not list:
        aggregates = [aggregates]

    correspond = OrderedDict.fromkeys(original_countries)

    for agg in aggregates:
        if type(agg) is str:
            agg = coco.get_correspondance_dict(original_countries_class,
                                               agg)
        for country in original_countries:
            if correspond.get(country) is None:
                try:
                    entry = agg[country]
                except KeyError:
                    entry = None

                if type(entry) is list:
                    if 1 < len(entry):
                        if merge_multiple_string:
                            entry = merge_multiple_string.join([
                                str(e) for e in entry])
                        else:
                            entry = None
                        if log_merge_multiple_strings:
                            log_merge_multiple_strings(country)
                    else:
                        entry = entry[0]

                correspond[country] = entry

    for country in original_countries:
        if correspond.get(country) is None:
            if missing_countries is True:
                correspond[country] = country
            elif missing_countries is False:
                del correspond[country]
            else:
                correspond[country] = missing_countries
            if log_missing_countries:
                log_missing_countries(country)

    if as_dataframe:
        correspond = pd.DataFrame.from_dict(
            correspond, orient='index').reset_index()
        correspond.columns = ['original', 'aggregated']
        if ((type(as_dataframe) is str) and
                (as_dataframe[0].lower() == 'f')):
            _co_list = correspond.original
            correspond['val'] = 1
            correspond = correspond.set_index(
                ['original', 'aggregated']).unstack().fillna(0)['val']
            correspond = correspond.loc[_co_list]

    return correspond


def match(list_a, list_b, not_found='not_found', enforce_sublist=False,
          country_data=COUNTRY_DATA_FILE, additional_data=None):
    """ Matches the country names given in two lists into a dictionary.

    This function matches names given in list_a to the one provided in list_b
    using regular expressions defined in country_data.

    Parameters
    ----------
    list_a : list
        Names of countries to identify
    list_b : list
        Master list of names for countries

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value
        (default: 'not found')

    enforce_sublist : boolean, optional
        If True, all entries in both list are list.
        If False(default), only multiple matches are list, rest are strings

    country_data : Pandas DataFrame or path to data file (optional)
        This is by default set to COUNTRY_DATA_FILE - the standard (tested)
        country list for coco.

    additional_data: (list of) Pandas DataFrames or data files (optional)
         Additional data to include for a specific analysis.
         This must be given in the same format as specified in the
         country_data file. (utf-8 encoded tab separated data, same
         column headers in all files)

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

    coco = CountryConverter(country_data, additional_data)

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
    """ Wrapper around CountryConverter.convert()

    Uses the same parameters. This function has the same performance as
    CountryConverter.convert for one call; for multiple calls it is better to
    instantiate a common CountryConverter (this avoid loading the source data
    file multiple times).

    Note
    ----
    A lot of the functionality can also be done directly in Pandas DataFrames.
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

    to : str, optional
        Output classification (valid str for an index of the
        country data file), default: name_short

    enforce_list : boolean, optional
        If True, enforces the output to be list (if only one name was passed)
        or to be a list of lists (if multiple names were passed).  If False
        (default), the output will be a string (if only one name was passed) or
        a list of str and/or lists (str if a one to one matching, list
        otherwise).

    not_found : str, optional
        Fill in value for not found entries. If None, keep the input value
        (default: 'not found')

    country_data : Pandas DataFrame or path to data file (optional)
        This is by default set to COUNTRY_DATA_FILE - the standard (tested)
        country list for coco.

    additional_data: (list of) Pandas DataFrames or data files (optional)
         Additional data to include for a specific analysis.
         This must be given in the same format as specified in the
         country_data_file. (utf-8 encoded tab separated data, same
         column headers as in the general country data file)

    Returns
    -------
    list or str, depending on enforce_list

    """
    init = {'country_data': COUNTRY_DATA_FILE,
            'additional_data': None,
            'only_UNmember': False,
            'include_obsolete': False}
    init.update({kk: kargs.get(kk) for kk in init.keys() if kk in kargs})
    coco = CountryConverter(**init)
    kargs = {kk: ii for kk, ii in kargs.items() if kk not in init.keys()}
    return coco.convert(*args, **kargs)


class CountryConverter():
    """ Main class for converting countries

    Attributes
    ----------

    data : Pandas DataFrame
        Raw data read from the country data file

    """

    @staticmethod
    def _separate_exclude_cases(name, exclude_prefix):
        """ Splits the excluded

        Parameters
        ----------
        name : str
            Name of the country/region to convert.

        exclude_prefix : list of valid regex strings
            List of indicators which negate the subsequent country/region.
            These prefixes and everything following will not be converted.
            E.g. 'Asia excluding China' becomes 'Asia' and
            'China excluding Hong Kong' becomes 'China' prior to conversion


        Returns
        -------

        dict with
            'clean_name' : str
                as name without anything following exclude_prefix
            'excluded_countries' : list
                list of excluded countries

        """

        excluder = re.compile('|'.join(exclude_prefix))
        split_entries = excluder.split(name)
        return {'clean_name': split_entries[0],
                'excluded_countries': split_entries[1:]}

    def __init__(self, country_data=COUNTRY_DATA_FILE,
                 additional_data=None, only_UNmember=False,
                 include_obsolete=False):
        """
        Parameters
        ----------

        country_data : Pandas DataFrame or path to data file
            This is by default set to COUNTRY_DATA_FILE - the standard
            (tested) country list for coco.

        additional_data: (list of) Pandas DataFrames or data files
            Additioanl data to include for a specific analysis.
            This must be given in the same format as specified in the
            country_data file. (utf-8 encoded tab separated data, same
            column headers in all files)

        only_UNmember: boolean, optional
            If True, only load countries currently being UN members from
            the standard data file. If False (default) load the full list
            of countries. In this case, also countries currently not existing
            (USSR) or with overlapping territories are included.

        include_obsolete: boolean, optional
            If True, includes countries that have become obsolete. If
            False (default) only includes currently valid countries.

        """

        must_be_unique = ['name_short', 'name_official', 'regex']
        must_be_string = must_be_unique + (['ISO2', 'ISO3',
                                            'continent', 'UNregion',
                                            'EXIO1', 'EXIO2', 'EXIO3',
                                            'WIOD'])

        def test_for_unique_names(df, data_name='passed dataframe',
                                  report_fun=logging.error):
            for name_entry in must_be_unique:
                if df[name_entry].duplicated().any():
                    report_fun('Duplicated values in column {} of {}'.format(
                        name_entry, data_name))

        def data_loader(data):
            if isinstance(data, pd.DataFrame):
                ret = data
                test_for_unique_names(data)
            else:
                ret = pd.read_table(data, sep='\t', encoding='utf-8',
                                    converters={str_col: str
                                                for str_col in must_be_string})
                test_for_unique_names(ret, data)
            return ret

        basic_df = data_loader(country_data)
        if only_UNmember:
            basic_df.dropna(subset=['UNmember'], inplace=True)

        if not include_obsolete:
            basic_df = basic_df[basic_df.obsolete.isnull()]

        if additional_data is None:
            additional_data = []
        if not isinstance(additional_data, list):
            additional_data = [additional_data]

        add_data = [data_loader(df) for df in additional_data]
        self.data = pd.concat([basic_df] + add_data, ignore_index=True,
                              axis=0)

        test_for_unique_names(
            self.data,
            data_name='merged data - keep last one',
            report_fun=logging.warning)

        for name_entry in must_be_unique:
            self.data.drop_duplicates(subset=[name_entry],
                                      keep='last', inplace=True)

        self.data.reset_index(drop=True, inplace=True)
        self.regexes = [re.compile(entry, re.IGNORECASE)
                        for entry in self.data.regex]

    def convert(self, names, src=None, to='ISO3', enforce_list=False,
                not_found='not found',
                exclude_prefix=['excl\\w.*', 'without', 'w/o']):
        """ Convert names from a list to another list.

        Note
        ----
        A lot of the functionality can also be done directly in Pandas
        DataFrames.
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
            Source classification. If None (default), each passed name is
            checked if it is a number (assuming UNnumeric) or 2 (ISO2) or
            3 (ISO3) characters long; for longer names 'regex' is assumed.

        to : str, optional
            Output classification (valid index of the country_data file),
            default: ISO3

        enforce_list : boolean, optional
            If True, enforces the output to be list (if only one name was
            passed) or to be a list of lists (if multiple names were passed).
            If False (default), the output will be a string (if only one name
            was passed) or a list of str and/or lists (str if a one to one
            matching, list otherwise).

        not_found : str, optional
            Fill in value for none found entries. If None, keep the input value
            (default: 'not found')

        exclude_prefix : list of valid regex strings
            List of indicators which negate the subsequent country/region.
            These prefixes and everything following will not be converted.
            E.g. 'Asia excluding China' becomes 'Asia' and
            'China excluding Hong Kong' becomes 'China' prior to conversion
            Default: ['excl\\w.*', 'without', 'w/o'])

        Returns
        -------
        list or str, depending on enforce_list

        """
        # The list to tuple conversion is necessary for Matlab interface
        names = list(names) if (
                isinstance(names, tuple) or
                isinstance(names, set)) else names

        names = names if isinstance(names, list) else [names]

        names = [str(n) for n in names]

        outlist = names.copy()

        to = [self._validate_input_para(to, self.data.columns)]

        exclude_split = {name: self._separate_exclude_cases(name,
                                                            exclude_prefix)
                         for name in names}

        for ind_names, current_name in enumerate(names):
            spec_name = exclude_split[current_name]['clean_name']

            if src is None:
                src_format = self._get_input_format_from_name(spec_name)
            else:
                src_format = self._validate_input_para(src, self.data.columns)

            if src_format.lower() == 'regex':
                result_list = []
                for ind_regex, ccregex in enumerate(self.regexes):
                    if ccregex.search(spec_name):
                        result_list.append(
                            self.data.ix[ind_regex, to].values[0])
                    if len(result_list) > 1:
                        logging.warning('More then one regular expression '
                                        'match for {}'.format(spec_name))

            else:
                _match_col = self.data[src_format].astype(
                    str).str.replace('\\..*', '')

                result_list = [etr[0] for etr in
                               self.data[_match_col.str.contains(
                                    '^' + spec_name + '$', flags=re.IGNORECASE,
                                    na=False)][to].values]

            if len(result_list) == 0:
                logging.warning(
                    '{} not found in {}'.format(spec_name, src_format))
                _fillin = not_found or spec_name
                outlist[ind_names] = [_fillin] if enforce_list else _fillin
            else:
                outlist[ind_names] = []
                for etr in result_list:
                    try:
                        conv_etr = int(etr)
                    except ValueError:
                        conv_etr = etr
                    outlist[ind_names].append(conv_etr)

                if len(outlist[ind_names]) == 1 and enforce_list is False:
                    outlist[ind_names] = outlist[ind_names][0]

        if (len(outlist) == 1) and not enforce_list:
            return outlist[0]
        else:
            return outlist

    def EU28as(self, to='name_short'):
        """
        Return EU28 countries in the specified classification

        Parameters
        ----------
        to : str, optional
            Output classification (valid str for an index of
            country_data file), default: name_short

        Returns
        -------
        Pandas DataFrame

        """
        if type(to) is str:
            to = [to]
        return self.data[self.data.EU < 2015][to]

    def EU27as(self, to='name_short'):
        """
        Return EU27 countries in the specified classification

        Parameters
        ----------
        to : str, optional
            Output classification (valid str for an index of
            country_data file), default: name_short

        Returns
        -------
        Pandas DataFrame

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.EU < 2013][to]

    def OECDas(self, to='name_short'):
        """
        Return OECD member states in the specified classification

        Parameters
        ----------
        to : str, optional
            Output classification (valid str for an index of
            country_data file), default: name_short

        Returns
        -------
        Pandas DataFrame

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.OECD > 0][to]

    def UNas(self, to='name_short'):
        """
        Return UN member states in the specified classification

        Parameters
        ----------
        to : str, optional
            Output classification (valid str for an index of
            country_data file), default: name_short

        Returns
        -------
        Pandas DataFrame

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.UNmember > 0][to]

    def obsoleteas(self, to='name_short'):
        """
        Return obsolete countries in the specified classification

        Parameters
        ----------
        to : str, optional
            Output classification (valid str for an index of
            country_data file), default: name_short

        Returns
        -------
        Pandas DataFrame

        """
        if isinstance(to, str):
            to = [to]
        return self.data[self.data.obsolete > 0][to]

    @property
    def EU28(self):
        """ EU28 member states (standard name_short) -
            use EU28as() for any other classification
        """
        return self.EU28as(to='name_short')

    @property
    def EU27(self):
        """ EU27 member states (standard name_short) -
            use EU27as() for any other classification
        """
        return self.EU27as(to='name_short')

    @property
    def OECD(self):
        """ OECD member states (standard name_short) -
            use OECDas() for any other classification
        """
        return self.OECDas(to='name_short')

    @property
    def UN(self):
        """ UN member states (standard name_short) -
        use UNas() for any other classification
        """
        return self.UNas(to='name_short')

    @property
    def valid_class(self):
        """ Valid strings for the converter """
        return list(self.data.columns)

    def get_correspondance_dict(self, classA, classB,
                                restrict=None,
                                replace_numeric=True):
        """ Returns a correspondance between classification A and B as dict

        Parameters
        ----------

        classA: str
            Valid classification (column name of data)

        classB: str
            Valid classification (column name of data).

        restrict: boolean vector of size cc.data, optional
            where cc is the name of the CountryConverter instance.  Used to
            restrict the data sheet if necessary.  E.g. to convert to countries
            which were OECD members before 1970 use
            cc.get_correspondance_dict('ISO3', 'OECD', restrict=cc.data.OECD <
            1970)

        replace_numeric: boolean, optional
            If True (default) replace numeric values with the column header.
            This can be used if get a correspondance to, for example, 'OECD'
            instead of to the OECD membership years. Set to False if the actual
            numbers are required (as for UNcode).

        Returns
        -------
        dict with
            keys: based on classA
            items: list of correspoding entries in classB or None

        """
        result = {nn: None for nn in self.data[classA].values}

        if restrict is None:
            df = self.data.copy()
        else:
            df = self.data[restrict].copy()

        if replace_numeric and df[classB].dtype.kind in 'bifc':
            df.loc[~df[classB].isnull(), classB] = classB
            df.loc[df[classB].isnull(), classB] = None

        result.update(df.groupby(classA)
                        .aggregate(lambda x: list(x.unique()))
                        .to_dict()[classB])

        return result

    def _validate_input_para(self, para, column_names):
        """ Convert the input classificaton para to the correct df column name

        Parameters
        ----------

        para : string
        column_names : list of strings

        Returns
        -------

        validated_para : string
            Converted to the case used in the country file
        """
        lower_case_valid_class = [et.lower() for et in self.valid_class]

        alt_valid_names = {
            'name_short': ['short', 'short_name', 'name', 'names'],
            'name_official': ['official', 'long_name', 'long'],
            'UNcode': ['un', 'unnumeric'],
            'ISOnumeric': ['isocode'],
            }

        for item in alt_valid_names.items():
            if para.lower() in item[1]:
                para = item[0]

        try:
            validated_para = self.valid_class[
                lower_case_valid_class.index(para.lower())]
        except ValueError:
            raise KeyError(
                '{} is not a valid country classification'.format(para))

        return validated_para

    def _get_input_format_from_name(self, name):
        """ Determines the input format based on the given country name

        Parameters
        ----------

        name : string

        Returns
        -------

        string : valid input format
        """
        try:
            int(name)
            src_format = 'ISOnumeric'
        except ValueError:
            if len(name) == 2:
                src_format = 'ISO2'
            elif len(name) == 3:
                src_format = 'ISO3'
            else:
                src_format = 'regex'
        return src_format


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
                     'Version: {}'.format(__version__)
                     ), prog='coco', usage=('%(prog)s --names --src --to]'))

    parser.add_argument('names',
                        help=('List of countries to convert '
                              '(space separated, country names consisting of '
                              'multiple words must be put in quotation marks).'
                              'Possible classifications: ' +
                              ', '.join(valid_classifications) +
                              '; NB: long, official and short are provided '
                              'as shortcuts for the names classifications'
                              ), nargs='*')
    parser.add_argument('-s', '--src', '--source', '-f', '--from',
                        help=('Classification of the names given, '
                              '(default: inferred from names)'))
    parser.add_argument('-t', '--to',
                        help=('Required classification of the passed names'
                              '(default: "ISO3"'))
    parser.add_argument('-o', '--output_sep',
                        help=('Seperator for output names '
                              '(default: space), e.g. "," '))
    parser.add_argument('-n', '--not_found',
                        default='not found',
                        help=('Fill in value for none found entries. '
                              'If "None" (string), keep the input value '
                              '(default: not found)'))
    parser.add_argument('-a', '--additional_data',
                        help=('Data file with additional country data'
                              '(Same format as the original data file - '
                              'utf-8 encoded tab separated data, same '
                              'column headers as in the general country '
                              'data file; default: not found)'))

    args = parser.parse_args()
    args.src = args.src or None
    args.to = args.to or 'ISO3'
    args.not_found = args.not_found if args.not_found != 'None' else None
    args.output_sep = args.output_sep or ' '

    return args


def main():
    """ Main entry point - used for command line call
    """
    args = _parse_arg(CountryConverter().valid_class)
    coco = CountryConverter(additional_data=args.additional_data)
    converted_names = coco.convert(
        names=args.names,
        src=args.src,
        to=args.to,
        enforce_list=False,
        not_found=args.not_found)

    print(args.output_sep.join(
        [str(etr) for etr in converted_names] if
        isinstance(converted_names, list) else [str(converted_names)]))


if __name__ == "__main__":
    try:
        # main()
        coco = CountryConverter()
        coco.data
    except Exception as excep:
        logging.exception(excep)
        raise
