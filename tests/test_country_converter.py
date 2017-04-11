import os
import sys
import pytest
import pandas as pd
import collections

TESTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TESTPATH, '..'))

regex_test_files = [nn for nn in os.listdir(TESTPATH)
                    if (nn[:10] == 'test_regex') and
                    (os.path.splitext(nn)[1] == '.txt')]

import country_converter as coco  # nopep8


@pytest.fixture(scope='module', params=regex_test_files)
def get_regex_test_data(request):
    retval = collections.namedtuple('regex_test_data',
                                    ['data_name', 'data'])
    return retval(
        request.param,
        pd.read_table(os.path.join(TESTPATH, request.param),
                      encoding='utf-8'))


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
    converter = coco.CountryConverter()
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
