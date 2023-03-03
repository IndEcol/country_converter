""" Testing admin stuff
"""

import os
import re
import sys
import warnings

import pytest

import country_converter as coco  # noqa

TESTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TESTPATH, ".."))

CHANGELOG_FILE = os.path.join(TESTPATH, "..", "CHANGELOG.md")


def test_version_consistency():
    """Test CHANGELOG.md latest version consistency with module version"""
    # Assumption: version info is in a header line (starting with #)
    # We capture the version info in the second group
    version_match = re.compile(r"(#*.*)(\d+\.\d+\.\d+[a-zA-Z0-9_.]*)")
    with open(CHANGELOG_FILE, "r") as cf:
        for line in cf:
            pot_match = re.match(version_match, line)
            if pot_match:
                version_changelog = pot_match.groups()[1]
                break
        else:
            raise ValueError("No version information found in the CHANGELOG file")
    assert (
        coco.__version__ == version_changelog
    ), f"Version module({coco.__version__}) - CHANGELOG.rst do not match({version_changelog})"
