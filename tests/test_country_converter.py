import os
import sys
import pytest
import pandas as pd
import logging
from pandas.util.testing import assert_frame_equal
import collections
from collections import OrderedDict

TESTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TESTPATH, '..'))

import country_converter as coco  # noqa
from country_converter.country_converter import _parse_arg  # noqa

regex_test_files = [nn for nn in os.listdir(TESTPATH)
                    if (nn[:10] == 'test_regex') and
                    (os.path.splitext(nn)[1] == '.txt')]
custom_data = os.path.join(TESTPATH, 'custom_data_example.txt')


@pytest.fixture(scope='module', params=regex_test_files)
def get_regex_test_data(request):
    retval = collections.namedtuple('regex_test_data',
                                    ['data_name', 'data'])
    return retval(
        request.param,
        pd.read_csv(os.path.join(TESTPATH, request.param),
                    sep='\t', encoding='utf-8'))


def test_name_short():
    """ Tests if there is a unique matching of name_short to regular expressions
    """
    converter = coco.CountryConverter()
    not_found_id = 'XXX'
    for row in converter.data.iterrows():
        name_test = row[1].name_short
        name_result = converter.convert(
            name_test,
            src='regex',
            to='name_short',
            not_found=not_found_id,
            enforce_list=False)
        assert len(name_result) > 2, (
            'Name {} matched several regular expressions: {}'.format(
                name_test, ' ,'.join(name_result)))
        assert name_result != not_found_id, (
            'Name {} did not match any regular expression'.format(name_test))
        assert name_result == name_test, (
            'Name {} did match the wrong regular expression: {}'.format(
                name_test, name_result))


def test_name_official():
    """ Tests if there is a unique matching of name_official to regular expressions
    """
    converter = coco.CountryConverter()
    not_found_id = 'XXX'
    for row in converter.data.iterrows():
        name_test = row[1].name_official
        name_result = converter.convert(
            name_test,
            src='regex',
            to='name_official',
            not_found=not_found_id,
            enforce_list=False)
        assert len(name_result) > 2, (
            'Name {} matched several regular expressions: {}'.format(
                name_test, ' ,'.join(name_result)))
        assert name_result != not_found_id, (
            'Name {} did not match any regular expression'.format(name_test))
        assert name_result == name_test, (
            'Name {} did match the wrong regular expression: {}'.format(
                name_test, name_result))


def test_alternative_names(get_regex_test_data):
    converter = coco.CountryConverter(include_obsolete=True)
    not_found_id = 'XXX'
    for row in get_regex_test_data.data.iterrows():
        name_test = row[1].name_test
        name_short = row[1].name_short
        name_result = converter.convert(
            name_test,
            src='regex',
            to='name_short',
            not_found=not_found_id,
            enforce_list=False)
        assert len(name_result) > 2, (
            'File {0} - row {1}: Name {2} matched several '
            'regular expressions: {3}'.format(
                get_regex_test_data.data_name,
                row[0],
                name_test,
                ' ,'.join(name_result)))
        if name_short != not_found_id:
            assert name_result != not_found_id, (
                'File {0} - row {1}: Name {2} did not match any '
                'regular expression'.format(
                    get_regex_test_data.data_name,
                    row[0],
                    name_test))
        assert name_result == name_short, (
            'File {0} - row {1}: Name {2} did match the '
            'wrong regular expression: {3}'.format(
                get_regex_test_data.data_name,
                row[0],
                name_test,
                name_result))


def test_additional_country_file():
    converter_basic = coco.CountryConverter()
    converter_extended = coco.CountryConverter(
        additional_data=custom_data)

    assert converter_basic.convert('Congo') == 'COG'
    assert converter_extended.convert('Congo') == 'COD'
    assert converter_extended.convert('wirtland',
                                      to='name_short') == 'Wirtland'


def test_additional_country_data():
    add_data = pd.DataFrame.from_dict({
        'name_short': ['xxx country'],
        'name_official': ['longer xxx country name'],
        'regex': ['xxx country'],
        'ISO3': ['XXX']}
    )
    converter_extended = coco.CountryConverter(
        additional_data=add_data)
    assert 'xxx country' == converter_extended.convert('XXX', src='ISO3',
                                                       to='name_short')
    assert pd.np.nan is converter_extended.convert('XXX', src='ISO3',
                                                   to='continent')


def test_UNmember():
    cc = coco.CountryConverter(only_UNmember=True)
    assert len(cc.data) == 193


def test_obsolete():
    cc = coco.CountryConverter()
    assert len(cc.data) == 250
    cc = coco.CountryConverter(include_obsolete=False)
    assert len(cc.data) == 250
    cc = coco.CountryConverter(include_obsolete=True)
    assert len(cc.data) == 256


def test_special_cases():
    """ Some test for special cases which occurred during development.

    These are test for specific issues turned up.
    """
    converter = coco.CountryConverter().convert

    # issue 22 - namibia iso2 na interpreted as not a number
    assert converter('NA', to='ISO3') == 'NAM'
    assert converter('NAM', to='ISO2') == 'NA'


def test_get_correspondance_dict_standard():
    """ Standard test case for get_correspondance_dict method
    """
    classA = 'EXIO1'
    classB = 'continent'
    cc = coco.CountryConverter()
    corr = cc.get_correspondance_dict(classA=classA,
                                      classB=classB)
    assert type(corr) == dict
    assert len(corr) == 44
    assert corr['DE'] == ['Europe']
    assert corr['ZA'] == ['Africa']
    assert corr['WW'] == ['Asia', 'Europe',
                          'Africa', 'Oceania',
                          'America', 'Antarctica']


def test_get_correspondance_dict_numeric_replace():
    """ Numeric replacement test of get_correspondance_dict method
    """
    classA = 'EXIO1'
    classB = 'OECD'
    cc = coco.CountryConverter()
    corr_str = cc.get_correspondance_dict(classA=classA,
                                          classB=classB,
                                          replace_numeric=True)
    assert type(corr_str) == dict
    assert len(corr_str) == 44
    assert corr_str['JP'] == ['OECD']
    assert corr_str['ZA'] == [None]
    assert None in corr_str['WW']
    assert 'OECD' in corr_str['WW']
    assert len(corr_str['WW']) == 2

    corr_num = cc.get_correspondance_dict(classA=classA,
                                          classB=classB,
                                          replace_numeric=False)
    assert type(corr_num) == dict
    assert len(corr_num) == 44
    assert corr_num['JP'] == [1964]
    assert pd.np.isnan(corr_num['ZA'])
    assert 2010 in corr_num['WW']
    assert 1961 in corr_num['WW']
    assert len(corr_num['WW']) == 4


def test_build_agg_conc_custom():
    """ Minimal test of the aggregation concordance building functionality
    """

    original_countries = ['c1', 'c2', 'c3', 'c4']
    aggregates = [{'c1': 'r1', 'c2': 'r1', 'c3': 'r2'}]

    agg_dict_wmiss = coco.agg_conc(original_countries,
                                   aggregates,
                                   merge_multiple_string=None,
                                   missing_countries=True,
                                   log_missing_countries=(
                                       lambda x: logging.error(
                                           'Country {} missing'.format(x))),
                                   log_merge_multiple_strings=None,
                                   as_dataframe=False
                                   )

    assert agg_dict_wmiss == OrderedDict([('c1', 'r1'),
                                          ('c2', 'r1'),
                                          ('c3', 'r2'),
                                          ('c4', 'c4')])

    agg_dict_replace = coco.agg_conc(original_countries,
                                     aggregates,
                                     merge_multiple_string=None,
                                     missing_countries='RoW',
                                     log_missing_countries=None,
                                     log_merge_multiple_strings=None,
                                     as_dataframe=False
                                     )

    assert agg_dict_replace == OrderedDict([('c1', 'r1'),
                                            ('c2', 'r1'),
                                            ('c3', 'r2'),
                                            ('c4', 'RoW')])

    agg_vec_womiss = coco.agg_conc(original_countries,
                                   aggregates,
                                   merge_multiple_string=None,
                                   missing_countries=False,
                                   log_missing_countries=None,
                                   log_merge_multiple_strings=None,
                                   as_dataframe='sparse'
                                   )

    expected_vec = pd.DataFrame(data=[['c1', 'r1'],
                                      ['c2', 'r1'],
                                      ['c3', 'r2'],
                                      ],
                                columns=['original', 'aggregated']
                                )

    assert_frame_equal(agg_vec_womiss, expected_vec)

    agg_matrix_womiss = coco.agg_conc(original_countries,
                                      aggregates,
                                      merge_multiple_string=None,
                                      missing_countries=False,
                                      log_missing_countries=None,
                                      log_merge_multiple_strings=None,
                                      as_dataframe='full'
                                      )

    expected_matrix = pd.DataFrame(data=[[1.0, 0.0],
                                         [1.0, 0.0],
                                         [0.0, 1.0],
                                         ],
                                   columns=['r1', 'r2'],
                                   index=['c1', 'c2', 'c3'],
                                   )
    expected_matrix.index.names = ['original']
    expected_matrix.columns.names = ['aggregated']

    assert_frame_equal(agg_matrix_womiss, expected_matrix)

    original_countries = ['c1', 'c2', 'c3', 'c4']
    aggregates = [{'c1': ['r1', 'r2'], 'c2': 'r1', 'c3': 'r2'}]
    agg_matrix_double_region = coco.agg_conc(original_countries,
                                             aggregates,
                                             merge_multiple_string='_&_',
                                             missing_countries=False,
                                             log_missing_countries=None,
                                             log_merge_multiple_strings=(
                                                 lambda x: logging.warning(
                                                     'Country {} belongs to '
                                                     'multiple '
                                                     'regions'.format(x))),
                                             as_dataframe='full'
                                             )
    expected_matrix = pd.DataFrame(data=[[0.0, 1.0, 0.0],
                                         [1.0, 0.0, 0.0],
                                         [0.0, 0.0, 1.0],
                                         ],
                                   columns=['r1', 'r1_&_r2', 'r2'],
                                   index=['c1', 'c2', 'c3'],
                                   )
    expected_matrix.index.names = ['original']
    expected_matrix.columns.names = ['aggregated']

    assert_frame_equal(agg_matrix_double_region, expected_matrix)


def test_build_agg_conc_exio():
    """ Some agg_conc test with a subset of exio countries
    """

    original_countries = ['TW', 'XX', 'AT', 'US', 'WA']
    aggregates = [
        'EU', 'OECD', 'continent'
    ]

    agg_dict_replace = coco.agg_conc(original_countries,
                                     aggregates,
                                     merge_multiple_string=False,
                                     missing_countries='RoW',
                                     log_missing_countries=None,
                                     log_merge_multiple_strings=None,
                                     as_dataframe=False
                                     )

    assert agg_dict_replace == OrderedDict([('TW', 'Asia'),
                                            ('XX', 'RoW'),
                                            ('AT', 'EU'),
                                            ('US', 'OECD'),
                                            ('WA', 'RoW')])

    agg_dict_skip = coco.agg_conc(original_countries,
                                  aggregates,
                                  merge_multiple_string=False,
                                  missing_countries=False,
                                  log_missing_countries=None,
                                  log_merge_multiple_strings=None,
                                  as_dataframe=False
                                  )

    assert agg_dict_skip == OrderedDict([('TW', 'Asia'),
                                         ('AT', 'EU'),
                                         ('US', 'OECD')])

    agg_matrix_skip = coco.agg_conc(original_countries,
                                    aggregates,
                                    merge_multiple_string=False,
                                    missing_countries=False,
                                    log_missing_countries=None,
                                    log_merge_multiple_strings=None,
                                    as_dataframe='full'
                                    )

    assert agg_matrix_skip.index.tolist() == ['TW', 'AT', 'US']

    aggregates_oecd_first = [
        'OECD', 'EU', {'WA': 'RoW', 'WF': 'RoW'}
    ]

    agg_dict_oecd_eu = coco.agg_conc(original_countries,
                                     aggregates_oecd_first,
                                     merge_multiple_string=False,
                                     missing_countries=True,
                                     log_missing_countries=None,
                                     log_merge_multiple_strings=None,
                                     as_dataframe=False
                                     )

    assert agg_dict_oecd_eu == OrderedDict([('TW', 'TW'),
                                            ('XX', 'XX'),
                                            ('AT', 'OECD'),
                                            ('US', 'OECD'),
                                            ('WA', 'RoW')])

    aggregates = 'EU'
    agg_dict_full_exio = coco.agg_conc('EXIO2',
                                       aggregates,
                                       merge_multiple_string=False,
                                       missing_countries='RoW',
                                       log_missing_countries=None,
                                       log_merge_multiple_strings=None,
                                       as_dataframe=False
                                       )

    assert len(agg_dict_full_exio) == 48
    assert agg_dict_full_exio['US'] == 'RoW'
    assert agg_dict_full_exio['AT'] == 'EU'


def test_match():
    match_these = ['norway', 'united_states', 'china', 'taiwan']
    master_list = ['USA', 'The Swedish Kingdom', 'Norway is a Kingdom too',
                   'Peoples Republic of China', 'Republic of China']
    matching_dict = coco.match(match_these, master_list)
    assert matching_dict['china'] == 'Peoples Republic of China'
    assert matching_dict['taiwan'] == 'Republic of China'
    assert matching_dict['norway'] == 'Norway is a Kingdom too'
    match_string_from = 'united states'
    match_string_to_correct = 'USA'
    matching_dict = coco.match(match_string_from, match_string_to_correct)
    assert matching_dict['united states'] == 'USA'
    match_from = ('united states',)
    match_false = ('abc',)
    matching_dict = coco.match(match_from, match_false)
    assert matching_dict['united states'] == 'not_found'
    matching_dict = coco.match(match_false, match_false)
    assert matching_dict['abc'] == 'not_found'


def test_regex_warnings(caplog):
    # for rec in caplog.records:
    coco.convert('abc', src='regex')
    assert "not found in regex" in caplog.text


def test_cli_output(capsys):
    inp_list = ['a', 'b']
    exp_string = 'a-b'
    inp_df1col = pd.DataFrame(data=inp_list,
                              columns=['names'],
                              index=['co1', 'co2'])
    inp_df2col = inp_df1col.T
    coco.cli_output(inp_list, sep='-')
    out, err = capsys.readouterr()
    assert exp_string in out

    coco.cli_output(inp_df1col, sep='-')
    out, err = capsys.readouterr()
    assert exp_string in out

    coco.cli_output(inp_df2col, sep='-')
    out, err = capsys.readouterr()
    assert exp_string in out


def test_wrapper_convert():
    assert 'US' == coco.convert('usa', src='regex', to='ISO2')
    assert 'AT' == coco.convert('40', to='ISO2')


def test_convert_wrong_classification():
    with pytest.raises(KeyError) as _:
        coco.convert('usa', src='abc')


def test_EU_output():
    cc = coco.CountryConverter()
    EU28 = cc.EU28as('ISO2')
    assert len(EU28 == 28)
    assert cc.convert('Croatia', to='ISO2') in EU28.ISO2.values
    EU27 = cc.EU27as('ISO2')
    assert len(EU27 == 27)
    assert cc.convert('Croatia', to='ISO2') not in EU27.ISO2.values


def test_EXIO_output():
    cc = coco.CountryConverter()
    exio1 = cc.EXIO1
    exio2 = cc.EXIO2
    exio3 = cc.EXIO3
    assert len(exio1) == 44
    assert len(exio2) == 48
    assert len(exio3) == 49
    assert 'WW' in exio1.values
    assert 'WA' in exio2.values
    assert 'WA' in exio3.values
    exio1iso3 = cc.EXIO1as(to='ISO3').set_index('original')
    exio2iso3 = cc.EXIO2as(to='ISO3').set_index('original')
    exio3iso3 = cc.EXIO3as(to='ISO3').set_index('original')

    assert exio1iso3.loc['AFG', 'aggregated'] == 'WW'
    assert exio2iso3.loc['AFG', 'aggregated'] == 'WA'
    assert exio3iso3.loc['AFG', 'aggregated'] == 'WA'
    assert exio1iso3.loc['DEU', 'aggregated'] == 'DE'
    assert exio2iso3.loc['DEU', 'aggregated'] == 'DE'
    assert exio3iso3.loc['DEU', 'aggregated'] == 'DE'


def test_WIOD_output():
    cc = coco.CountryConverter()
    ws = cc.WIOD
    wi = cc.WIODas(to='ISO2').set_index('original')
    assert len(ws) == 41
    assert 'RoW' in ws.values
    assert 'NLD' in ws.values
    assert wi.loc['AF', 'aggregated'] == 'RoW'
    assert wi.loc['AT', 'aggregated'] == 'AUT'


def test_Eora_output():
    cc = coco.CountryConverter()
    es = cc.Eora
    ei = cc.Eoraas(to='ISO2').set_index('original')
    assert len(es) == 238
    assert 'AUT' in es.values
    assert 'AFG' in es.values
    assert ei.loc['AF', 'aggregated'] == 'AFG'
    assert ei.loc['AT', 'aggregated'] == 'AUT'


def test_MESSAGE_output():
    cc = coco.CountryConverter()
    ms = cc.MESSAGE
    mi = cc.MESSAGEas(to='ISO3').set_index('original')
    assert len(ms) == 12
    assert 'PAO' in ms.values
    assert 'SAS' in ms.values
    assert mi.loc['AUT', 'aggregated'] == 'WEU'


def test_BRIC_output():
    cc = coco.CountryConverter()
    bs = cc.BRIC
    bi = cc.BRICas(to='ISO2')
    bn = cc.BRICas(to=None)
    assert len(bs) == 4 == len(bi) == len(bn)
    assert 'Brazil' in bs.values
    assert 'Brazil' in bn.values
    assert 'CN' in bi.values


def test_APEC_output():
    cc = coco.CountryConverter()
    aa = cc.APEC
    ai = cc.APECas(to='ISO2')
    an = cc.APECas(to=None)
    assert len(aa) == 21 == len(ai) == len(an)
    assert 'Taiwan' in aa.values
    assert 'Russia' in an.values
    assert 'RU' in ai.values


def test_BASIC_output():
    cc = coco.CountryConverter()
    ba = cc.BASIC
    bi = cc.BASICas(to='ISO2')
    bn = cc.BASICas(to=None)
    assert len(ba) == 4 == len(bi) == len(bn)
    assert 'Brazil' in ba.values
    assert 'Brazil' in bn.values
    assert 'IN' in bi.values


def test_CIS_output():
    cc = coco.CountryConverter()
    ca = cc.CIS
    ci = cc.CISas(to='ISO2')
    cn = cc.CISas(to=None)
    assert len(ca) == 8 == len(ci) == len(cn)
    assert 'Belarus' in ca.values
    assert 'Armenia' in cn.values
    assert 'RU' in ci.values


def test_G7_20_output():
    cc = coco.CountryConverter()
    G7a = cc.G7
    G7i = cc.G7as(to='ISO2')
    G7n = cc.G7as(to=None)
    G20a = cc.G20
    G20i = cc.G20as(to='ISO2')
    G20n = cc.G20as(to=None)

    assert len(G7a) == 7
    # Not testing the length of G20 b/c of mixup with EU

    assert 'Italy' in G7a.values
    assert 'Japan' in G7n.values
    assert 'US' in G7i.values
    assert 'Slovenia' in G20a.values
    assert 'Turkey' in G20n.values
    assert 'US' in G20i.values


def test_obsolute_output():
    cc = coco.CountryConverter(include_obsolete=True)
    oi = cc.obsoleteas(to='ISO2')
    on = cc.obsoleteas(to=None)
    assert 'Zanzibar' in on.values
    assert 'SU' in oi.values


def test_Cecilia_output():
    cc = coco.CountryConverter()
    cs = cc.Cecilia2050
    ci = cc.Cecilia2050as(to='ISO3').set_index('original')
    assert len(cs) == 4
    assert 'RoW' in ci.values
    assert 'EU' in ci.values
    assert ci.loc['AUT', 'aggregated'] == 'EU'
    assert ci.loc['AFG', 'aggregated'] == 'RoW'


def test_OECD_output():
    cc = coco.CountryConverter()
    oecd = cc.OECDas('ISO3')
    assert cc.convert('Netherlands', to='ISO3') in oecd.values


def test_UN_output():
    cc = coco.CountryConverter()
    un = coco.CountryConverter().UNas('ISO3')
    assert cc.convert('Netherlands', to='ISO3') in un.values


def test_obsolete_output():
    cc = coco.CountryConverter(include_obsolete=True)
    obsolete = coco.CountryConverter(include_obsolete=True).obsoleteas('ISO3')
    assert cc.convert('Netherlands Antilles', to='ISO3') in obsolete.values


def test_properties():
    cc = coco.CountryConverter()
    assert all(cc.EU28 == cc.EU28as(to='name_short'))
    assert all(cc.EU28 == cc.EU28as(to=None))
    assert all(cc.EU27 == cc.EU27as(to='name_short'))
    assert all(cc.EU27 == cc.EU27as(to=None))
    assert all(cc.OECD == cc.OECDas(to='name_short'))
    assert all(cc.OECD == cc.OECDas(to=None))
    assert all(cc.UN == cc.UNas(to='name_short'))
    assert all(cc.UN == cc.UNas(to=None))


def test_parser():
    sys.argv = ['AT', 'US']
    args = _parse_arg(coco.CountryConverter().valid_class)
    assert args.src == None   # noqa
    assert args.to == None    # noqa

    sys.argv = ['EXIO1']
    args = _parse_arg(coco.CountryConverter().valid_class)
    assert args.src == None    # noqa
    assert args.to == None     # noqa


def test_full_cli(capsys):
    # help
    with pytest.raises(SystemExit) as e_sys:
        coco.main()
    out, err = capsys.readouterr()
    assert "usage" in out
    assert "names" in out
    assert e_sys.type == SystemExit

    # country conversion
    _sysargv = sys.argv.copy()
    sys.argv = ['coco', 'AT']
    with pytest.raises(SystemExit) as e_sys:
        coco.main()
    out, err = capsys.readouterr()
    assert "AUT" in out
    assert e_sys.type == SystemExit

    # classification
    sys.argv = ['coco', 'EXIO1']
    with pytest.raises(SystemExit) as e_sys:
        coco.main()
    out, err = capsys.readouterr()
    assert "AT" in out
    assert "WW" in out
    assert e_sys.type == SystemExit
    sys.argv = _sysargv
