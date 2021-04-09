""" Testing admin stuff
"""

import sys
import warnings
import os
import re

import pytest

import country_converter as coco  # noqa

TESTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TESTPATH, ".."))

CHANGELOG_FILE = os.path.join(TESTPATH, "..", "CHANGELOG.rst")


def test_version_consistency():
    """Test CHANGELOG.rst latest version consistency with module version"""
    version_match = re.compile(r"\d+\.\d+\.\d+[a-zA-Z0-9_.]*")
    with open(CHANGELOG_FILE, "r") as cf:
        for line in cf:
            pot_match = re.match(version_match, line)
            if pot_match:
                version_changelog = pot_match.group()
                break
        else:
            raise ValueError("No version information found in the CHANGELOG file")
    assert (
        coco.__version__ == version_changelog
    ), "Version module - CHANGELOG.rst do not match"
