""" Testing the country_converter functionality
"""

import collections
import logging
import os
import sys
import warnings
from collections import OrderedDict

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

import country_converter as coco  # noqa
from country_converter.country_converter import _parse_arg  # noqa

TESTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TESTPATH, ".."))


# Additional test data
regex_test_files = [
    nn
    for nn in os.listdir(TESTPATH)
    if (nn[:10] == "test_regex") and (os.path.splitext(nn)[1] == ".txt")
]
non_matching_data = os.path.join(TESTPATH, "should_not_match.txt")
custom_data = os.path.join(TESTPATH, "custom_data_example.txt")


@pytest.fixture(scope="module", params=regex_test_files)
def get_regex_test_data(request):
    retval = collections.namedtuple("regex_test_data", ["data_name", "data"])
    return retval(
        request.param,
        pd.read_csv(os.path.join(TESTPATH, request.param), sep="\t", encoding="utf-8"),
    )


def test_name_short():
    """Tests if there is a unique matching of name_short to regular expressions"""
    converter = coco.CountryConverter()
    not_found_id = "XXX"
    for row in converter.data.iterrows():
        name_test = row[1].name_short
        name_result = converter.convert(
            name_test,
            src="regex",
            to="name_short",
            not_found=not_found_id,
            enforce_list=False,
        )
        assert (
            len(name_result) > 2
        ), "Name {} matched several regular expressions: {}".format(
            name_test, " ,".join(name_result)
        )
        assert (
            name_result != not_found_id
        ), "Name {} did not match any regular expression".format(name_test)
        assert (
            name_result == name_test
        ), "Name {} did match the wrong regular expression: {}".format(
            name_test, name_result
        )


def test_name_official():
    """Tests if there is a unique matching of name_official to regular expressions"""
    converter = coco.CountryConverter()
    not_found_id = "XXX"
    for row in converter.data.iterrows():
        name_test = row[1].name_official
        name_result = converter.convert(
            name_test,
            src="regex",
            to="name_official",
            not_found=not_found_id,
            enforce_list=False,
        )
        assert (
            len(name_result) > 2
        ), "Name {} matched several regular expressions: {}".format(
            name_test, " ,".join(name_result)
        )
        assert (
            name_result != not_found_id
        ), "Name {} did not match any regular expression".format(name_test)
        assert (
            name_result == name_test
        ), "Name {} did match the wrong regular expression: {}".format(
            name_test, name_result
        )


def test_alternative_names(get_regex_test_data):
    converter = coco.CountryConverter(include_obsolete=True)
    not_found_id = "XXX"
    for row in get_regex_test_data.data.iterrows():
        name_test = row[1].name_test
        name_short = row[1].name_short
        name_result = converter.convert(
            name_test,
            src="regex",
            to="name_short",
            not_found=not_found_id,
            enforce_list=False,
        )
        assert len(name_result) > 2, (
            "File {0} - row {1}: Name {2} matched several "
            "regular expressions: {3}".format(
                get_regex_test_data.data_name, row[0], name_test, " ,".join(name_result)
            )
        )
        if name_short != not_found_id:
            assert name_result != not_found_id, (
                "File {0} - row {1}: Name {2} did not match any "
                "regular expression".format(
                    get_regex_test_data.data_name, row[0], name_test
                )
            )
        assert name_result == name_short, (
            "File {0} - row {1}: Name {2} did match the "
            "wrong regular expression: {3}".format(
                get_regex_test_data.data_name, row[0], name_test, name_result
            )
        )


def test_toISO2_conversion():
    converter = coco.CountryConverter()
    assert "DE" == converter.convert("DEU", src="ISO3", to="ISO2")
    assert "GB" == converter.convert("GBR", src="ISO3", to="ISO2")
    assert "GB" == converter.convert("UK", src="ISO2", to="ISO2")
    assert "GB" == converter.convert("UK", to="ISO2")
    assert "GB" == converter.convert("GB", to="ISO2")
    assert "GR" == converter.convert("GR", to="ISO2")
    assert "GR" == converter.convert("EL", src="ISO2", to="ISO2")
    assert "GR" == converter.convert("EL", to="ISO2")
    assert "GB" == converter.convert("GBR", to="ISO2")
    assert "TR" == converter.convert("TR", src="ISO2", to="ISO2")
    assert "TR" == converter.convert("TUR", src="ISO3", to="ISO2")


def test_additional_country_file():
    converter_basic = coco.CountryConverter()
    converter_extended = coco.CountryConverter(additional_data=custom_data)

    assert converter_basic.convert("Congo") == "COG"
    assert converter_extended.convert("Congo") == "COD"
    assert converter_extended.convert("wirtland", to="name_short") == "Wirtland"
    assert 250 == converter_extended.convert("Congo", to="FAOcode")


def test_additional_country_data():
    add_data = pd.DataFrame.from_dict(
        {
            "name_short": ["xxx country"],
            "name_official": ["longer xxx country name"],
            "regex": ["xxx country"],
            "ISO3": ["XXX"],
            "ISO2": ["XX"],
        }
    )
    converter_extended = coco.CountryConverter(additional_data=add_data)
    assert "xxx country" == converter_extended.convert(
        "XXX", src="ISO3", to="name_short"
    )
    assert pd.isna(converter_extended.convert("XXX", src="ISO3", to="continent"))


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
    """Some test for special cases which occurred during development.

    These are test for specific issues turned up.
    """
    converter = coco.CountryConverter().convert

    # issue 22 - namibia iso2 na interpreted as not a number
    assert converter("NA", to="ISO3") == "NAM"
    assert converter("NAM", to="ISO2") == "NA"


def test_iterable_inputs():
    """Test the different possibilites to input lists

    This guards agains issue #54
    """
    _inp_list = ["AT", "BE", "DE", "GB", "TW"]

    inputs = dict(
        type_list=list(_inp_list),
        type_tuple=tuple(_inp_list),
        type_set=set(_inp_list),
        type_series=pd.Series(_inp_list),
        type_df_index=pd.Index(_inp_list),
    )

    outputs = {tt: sorted(coco.convert(val)) for tt, val in inputs.items()}

    input_error = 23.8

    with pytest.raises(TypeError) as e_sys:
        coco.convert(input_error)


def test_get_correspondance_dict_standard():
    """Standard test case for get_correspondence_dict method"""
    classA = "EXIO1"
    classB = "continent"
    cc = coco.CountryConverter()
    corr = cc.get_correspondence_dict(classA=classA, classB=classB)
    assert type(corr) == dict
    assert len(corr) == 44
    assert corr["DE"] == ["Europe"]
    assert corr["ZA"] == ["Africa"]
    assert corr["WW"] == [
        "Asia",
        "Europe",
        "Africa",
        "Oceania",
        "America",
        "Antarctica",
    ]


def test_get_correspondence_dict_numeric_replace():
    """Numeric replacement test of get_correspondence_dict method"""
    classA = "EXIO1"
    classB = "OECD"
    cc = coco.CountryConverter()
    corr_str = cc.get_correspondence_dict(
        classA=classA, classB=classB, replace_numeric=True
    )

    assert type(corr_str) == dict
    assert len(corr_str) == 44
    assert corr_str["JP"] == ["OECD"]
    assert corr_str["ZA"] == [None]
    assert None in corr_str["WW"]
    assert "OECD" in corr_str["WW"]
    assert len(corr_str["WW"]) == 2

    corr_num = cc.get_correspondence_dict(
        classA=classA, classB=classB, replace_numeric=False
    )

    assert type(corr_num) == dict
    assert len(corr_num) == 44
    assert corr_num["JP"] == [1964]
    assert pd.isna(corr_num["ZA"])
    assert 2010 in corr_num["WW"]
    assert 1961 in corr_num["WW"]
    assert len(corr_num["WW"]) == 6


def test_build_agg_conc_custom():
    """Minimal test of the aggregation concordance building functionality"""

    original_countries = ["c1", "c2", "c3", "c4"]
    aggregates = [{"c1": "r1", "c2": "r1", "c3": "r2"}]

    agg_dict_wmiss = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=None,
        missing_countries=True,
        log_missing_countries=(lambda x: logging.error("Country {} missing".format(x))),
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert agg_dict_wmiss == OrderedDict(
        [("c1", "r1"), ("c2", "r1"), ("c3", "r2"), ("c4", "c4")]
    )

    agg_dict_replace = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=None,
        missing_countries="RoW",
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert agg_dict_replace == OrderedDict(
        [("c1", "r1"), ("c2", "r1"), ("c3", "r2"), ("c4", "RoW")]
    )

    agg_vec_womiss = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=None,
        missing_countries=False,
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe="sparse",
    )

    expected_vec = pd.DataFrame(
        data=[["c1", "r1"], ["c2", "r1"], ["c3", "r2"]],
        columns=["original", "aggregated"],
    )

    assert_frame_equal(agg_vec_womiss, expected_vec)

    agg_matrix_womiss = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=None,
        missing_countries=False,
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe="full",
    )

    expected_matrix = pd.DataFrame(
        data=[[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
        columns=["r1", "r2"],
        index=["c1", "c2", "c3"],
    )
    expected_matrix.index.names = ["original"]
    expected_matrix.columns.names = ["aggregated"]

    assert_frame_equal(agg_matrix_womiss, expected_matrix)

    original_countries = ["c1", "c2", "c3", "c4"]
    aggregates = [{"c1": ["r1", "r2"], "c2": "r1", "c3": "r2"}]
    agg_matrix_double_region = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string="_&_",
        missing_countries=False,
        log_missing_countries=None,
        log_merge_multiple_strings=(
            lambda x: logging.warning(
                "Country {} belongs to " "multiple " "regions".format(x)
            )
        ),
        as_dataframe="full",
    )
    expected_matrix = pd.DataFrame(
        data=[[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
        columns=["r1", "r1_&_r2", "r2"],
        index=["c1", "c2", "c3"],
    )
    expected_matrix.index.names = ["original"]
    expected_matrix.columns.names = ["aggregated"]

    assert_frame_equal(agg_matrix_double_region, expected_matrix)


def test_build_agg_conc_exio():
    """Some agg_conc test with a subset of exio countries"""

    original_countries = ["TW", "XX", "AT", "US", "WA"]
    aggregates = ["EU", "OECD", "continent"]

    agg_dict_replace = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=False,
        missing_countries="RoW",
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert agg_dict_replace == OrderedDict(
        [("TW", "Asia"), ("XX", "RoW"), ("AT", "EU"), ("US", "OECD"), ("WA", "RoW")]
    )

    agg_dict_skip = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=False,
        missing_countries=False,
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert agg_dict_skip == OrderedDict([("TW", "Asia"), ("AT", "EU"), ("US", "OECD")])

    agg_matrix_skip = coco.agg_conc(
        original_countries,
        aggregates,
        merge_multiple_string=False,
        missing_countries=False,
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe="full",
    )

    assert agg_matrix_skip.index.tolist() == ["TW", "AT", "US"]

    aggregates_oecd_first = ["OECD", "EU", {"WA": "RoW", "WF": "RoW"}]

    agg_dict_oecd_eu = coco.agg_conc(
        original_countries,
        aggregates_oecd_first,
        merge_multiple_string=False,
        missing_countries=True,
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert agg_dict_oecd_eu == OrderedDict(
        [("TW", "TW"), ("XX", "XX"), ("AT", "OECD"), ("US", "OECD"), ("WA", "RoW")]
    )

    aggregates = "EU"
    agg_dict_full_exio = coco.agg_conc(
        "EXIO2",
        aggregates,
        merge_multiple_string=False,
        missing_countries="RoW",
        log_missing_countries=None,
        log_merge_multiple_strings=None,
        as_dataframe=False,
    )

    assert len(agg_dict_full_exio) == 48
    assert agg_dict_full_exio["US"] == "RoW"
    assert agg_dict_full_exio["AT"] == "EU"


def test_match():
    match_these = ["norway", "united_states", "china", "taiwan"]
    master_list = [
        "USA",
        "The Swedish Kingdom",
        "Norway is a Kingdom too",
        "Peoples Republic of China",
        "Republic of China",
    ]
    matching_dict = coco.match(match_these, master_list)
    assert matching_dict["china"] == "Peoples Republic of China"
    assert matching_dict["taiwan"] == "Republic of China"
    assert matching_dict["norway"] == "Norway is a Kingdom too"
    match_string_from = "united states"
    match_string_to_correct = "USA"
    matching_dict = coco.match(match_string_from, match_string_to_correct)
    assert matching_dict["united states"] == "USA"
    match_from = ("united states",)
    match_false = ("abc",)
    matching_dict = coco.match(match_from, match_false)
    assert matching_dict["united states"] == "not_found"
    matching_dict = coco.match(match_false, match_false)
    assert matching_dict["abc"] == "not_found"


def test_regex_warnings(caplog):
    # for rec in caplog.records:
    coco.convert("abc", src="regex")
    assert "not found in regex" in caplog.text


def test_cli_output(capsys):
    inp_list = ["a", "b"]
    exp_string = "a-b"
    inp_df1col = pd.DataFrame(data=inp_list, columns=["names"], index=["co1", "co2"])
    inp_df2col = inp_df1col.T
    coco.cli_output(inp_list, sep="-")
    out, err = capsys.readouterr()
    assert exp_string in out

    coco.cli_output(inp_df1col, sep="-")
    out, err = capsys.readouterr()
    assert exp_string in out

    coco.cli_output(inp_df2col, sep="-")
    out, err = capsys.readouterr()
    assert exp_string in out


def test_wrapper_convert():
    assert "US" == coco.convert("usa", src="regex", to="ISO2")
    assert "AT" == coco.convert("40", to="ISO2")


def test_convert_wrong_classification():
    with pytest.raises(KeyError) as _:
        coco.convert("usa", src="abc")


def test_EU_output():
    cc = coco.CountryConverter()
    EU28 = cc.EU28as("ISO2")
    assert len(EU28 == 28)
    assert cc.convert("Croatia", to="ISO2") in EU28.ISO2.tolist()
    EU27 = cc.EU27as("ISO2")
    assert len(EU27 == 27)
    assert cc.convert("Croatia", to="ISO2") in EU27.ISO2.tolist()
    assert cc.convert("UK", src="regex", to="ISO2") not in EU27.ISO2.tolist()
    EU27_2007 = cc.EU27_2007as("ISO2")
    assert len(EU27_2007 == 27)
    assert cc.convert("Croatia", to="ISO2") not in EU27_2007.ISO2.tolist()
    assert cc.convert("GB", src="regex", to="ISO2") in EU27_2007.ISO2.tolist()


def test_EXIO_output():
    cc = coco.CountryConverter()
    exio1 = cc.EXIO1.EXIO1.unique()
    exio2 = cc.EXIO2.EXIO2.unique()
    exio3 = cc.EXIO3.EXIO3.unique()
    assert len(exio1) == 44
    assert len(exio2) == 48
    assert len(exio3) == 49
    assert "WW" in exio1
    assert "WA" in exio2
    assert "WA" in exio3


def test_WIOD_output():
    cc = coco.CountryConverter()
    ws = cc.WIOD.WIOD.unique()
    assert len(ws) == 41
    assert "RoW" in ws
    assert "NLD" in ws


def test_Eora_output():
    cc = coco.CountryConverter()
    es = cc.Eora.Eora.unique()
    assert "AUT" in es
    assert "AFG" in es


def test_MESSAGE_output():
    cc = coco.CountryConverter()
    ms = cc.MESSAGE.MESSAGE.unique()
    assert len(ms) == 11
    assert "PAO" in ms
    assert "SAS" in ms


def test_properties():
    cc = coco.CountryConverter()
    assert all(cc.EU28 == cc.EU28as(to="name_short"))
    assert all(cc.EU27 == cc.EU27as(to="name_short"))
    assert all(cc.OECD == cc.OECDas(to="name_short"))
    assert all(cc.UN == cc.UNas(to="name_short"))


def test_parser():
    sys.argv = ["AT", "US"]
    args = _parse_arg(coco.CountryConverter().valid_class)
    assert args.src == None  # noqa
    assert args.to == None  # noqa

    sys.argv = ["EXIO1"]
    args = _parse_arg(coco.CountryConverter().valid_class)
    assert args.src == None  # noqa
    assert args.to == None  # noqa


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
    sys.argv = ["coco", "AT"]
    with pytest.raises(SystemExit) as e_sys:
        coco.main()
    out, err = capsys.readouterr()
    assert "Austria" in out
    assert e_sys.type == SystemExit

    # classification
    sys.argv = ["coco", "EXIO1"]
    with pytest.raises(SystemExit) as e_sys:
        coco.main()
    out, err = capsys.readouterr()
    assert "AT" in out
    assert "WW" in out
    assert e_sys.type == SystemExit
    sys.argv = _sysargv


def test_ISO_number_codes():
    """This is for ISO 3166 numeric"""
    cc = coco.CountryConverter()
    assert 32 == cc.convert("Argentina", to="ISOnumeric")
    assert 208 == cc.convert("Denmark", to="isocode")
    # based on https://www.worlddata.info/countrycodes.php
    # some claim it 383, but this is the telefone calling code
    assert 412 == cc.convert("Kosovo", to="ISOnumeric")


def test_fao_number_codes():
    cc = coco.CountryConverter()
    assert 21 == cc.convert("BRA", to="FAOcode")
    assert 223 == cc.convert("TUR", to="FAOcode")
    assert 67 == cc.convert("FIN", to="FAOcode")
    assert 117 == cc.convert("KOR", to="FAOcode")


def test_GBD_codes():
    cc = coco.CountryConverter()
    assert 35 == cc.convert("Georgia", to="GBDcode")
    assert 6 == cc.convert("China", to="GBDcode")
    assert 92 == cc.convert("Spain", to="GBDcode")


def test_non_matching():
    with open(non_matching_data, "r") as nmd:
        content = [line.strip() for line in nmd.readlines()]
    non_countries = [nc for nc in content if not nc.startswith("#") and nc != ""]

    not_found_indicator = "nope"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="not found")
        for reg_name in non_countries:
            assert not_found_indicator == coco.convert(
                reg_name, src="regex", to="ISO3", not_found=not_found_indicator
            )


def test_exio_three_letter():
    converter = coco.CountryConverter()
    assert "HRV" == converter.convert("Croatia", to="exio3_3l")
    assert "WWE" == converter.convert("Croatia", to="exio2_3l")
    assert "WWW" == converter.convert("Croatia", to="exio1_3l")
    assert "WWM" == converter.convert("Egypt", to="exio3_3l")
    assert "WWM" == converter.convert("Egypt", to="exio2_3l")
    assert "WWW" == converter.convert("Egypt", to="exio1_3l")

    assert len(converter.data.EXIO1_3L.squeeze().unique()) == len(
        converter.data.EXIO1.squeeze().unique()
    )
    assert len(converter.data.EXIO2_3L.squeeze().unique()) == len(
        converter.data.EXIO2.squeeze().unique()
    )

    for rr in converter.data.iterrows():
        if rr[1].EXIO3[0] == "W":
            assert rr[1].EXIO3_3L == "W" + rr[1].EXIO3, f"Mismatch: {rr}"
            assert rr[1].EXIO2_3L == "W" + rr[1].EXIO2, f"Mismatch: {rr}"
            assert rr[1].EXIO1_3L == "W" + rr[1].EXIO1, f"Mismatch: {rr}"

    for rr in converter.data.iterrows():
        assert converter.convert(
            rr[1].EXIO3_3L, src="EXIO3_3L", to="name_short"
        ) == converter.convert(
            rr[1].EXIO3, src="EXIO3", to="name_short"
        ), f"Mismatch in: {rr} "
        assert converter.convert(
            rr[1].EXIO2_3L, src="EXIO2_3L", to="name_short"
        ) == converter.convert(
            rr[1].EXIO2, src="EXIO2", to="name_short"
        ), f"Mismatch in: {rr} "
        assert converter.convert(
            rr[1].EXIO1_3L, src="EXIO1_3L", to="name_short"
        ) == converter.convert(
            rr[1].EXIO1, src="EXIO1", to="name_short"
        ), f"Mismatch in: {rr} "


def test_DAC_number_codes():
    cc = coco.CountryConverter()
    assert 1 == cc.convert("AUT", to="DACcode")
    assert 301 == cc.convert("CAN", to="DACcode")
    assert 347 == cc.convert("GTM", to="DACcode")
    assert 854 == cc.convert("VUT", to="DACcode")


def test_ccTLD():
    cc = coco.CountryConverter()
    assert "am" == cc.convert("Armenia", to="ccTLD")
    assert "er" == cc.convert("Eritrea", to="ccTLD")
    assert (
        cc.convert("Zambia", to="ccTLD").upper()
        == cc.convert("Zambia", to="ISO2").upper()
    )


def test_GWcode():
    cc = coco.CountryConverter()
    assert 305 == cc.convert("AUT", to="GWcode")
    assert 771 == cc.convert("BD", to="GWcode")
    assert 694 == cc.convert("Qatar", to="GWcode")
    assert np.isnan(cc.convert("United States Minor Outlying Islands", to="GWcode"))


def test_pandas_convert():
    """This will test that the behaviour of pandas_convert is equivalent
    to convert for Pandas Series"""

    # Load the series
    test_series = pd.read_csv(f"{TESTPATH}/test_series_data.csv", header=0)

    # Create cc object
    cc = coco.CountryConverter()

    # Check type validation by passing the DataFrame
    with pytest.raises(TypeError):
        cc.pandas_convert(test_series, to="ISO3")

    # Convert version
    convert = pd.Series(
        cc.convert(test_series.data, to="ISO3"), index=test_series.index, name="data"
    )

    # pandas_convert version
    pandas_convert = cc.pandas_convert(test_series.data, to="ISO3")

    assert_series_equal(convert, pandas_convert)


def test_pandas_convert_options():
    """This will test that the behaviour of pandas_convert is equivalent
    to convert for Pandas Series, using various options"""

    # Load the series
    test_series = pd.read_csv(f"{TESTPATH}/test_series_data.csv", header=0)

    # Create cc object
    cc = coco.CountryConverter()

    # -- Test the not_found option --
    # Convert version
    convert_not_found = pd.Series(
        cc.convert(test_series.data, to="ISO2", not_found="empty"),
        index=test_series.index,
        name="data",
    )

    # pandas_convert version
    pandas_not_found = cc.pandas_convert(test_series.data, to="ISO2", not_found="empty")

    # Check that the Series are equal
    assert_series_equal(convert_not_found, pandas_not_found)

    # -- Test the enforce_list option --
    # Convert version
    convert_enforce_list = pd.Series(
        cc.convert(test_series.data, to="UNRegion", enforce_list=True),
        index=test_series.index,
        name="data",
    )

    # pandas_convert version
    pandas_enforce_list = cc.pandas_convert(
        test_series.data, to="UNRegion", enforce_list=True
    )

    # Check that the Series are equal
    assert_series_equal(convert_enforce_list, pandas_enforce_list)

    # -- Test the exclude_prefix option --

    # Convert version
    convert_exclude_prefix = pd.Series(
        cc.convert(
            test_series.data, to="name", exclude_prefix=["without", "excluding"]
        ),
        index=test_series.index,
        name="data",
    )

    # pandas_convert version
    pandas_exclude_prefix = cc.pandas_convert(
        test_series.data, to="name", exclude_prefix=["without", "excluding"]
    )

    # Check that the Series are equal
    assert_series_equal(convert_exclude_prefix, pandas_exclude_prefix)


def test_CC41_output():
    cc = coco.CountryConverter()
    cs = cc.CC41.CC41.unique()
    assert len(cs) == 41
    assert "Rest of World" in cs
    assert "Great Britain and N.I." in cs


#### RUN PYTEST USING THE BELLOW CODE
# python -m pytest tests\test_functionality.py
# run the PYTEST BLACK test: python -m pytest -vv --black tests\test_functionality.py
###New Update
