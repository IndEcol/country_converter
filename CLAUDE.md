# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Country Converter (coco) is a Python package that converts and matches country names between different classifications and naming versions. It uses regular expressions internally to match country names and can build aggregation concordance matrices between different classification schemes.

## Core Architecture

The package consists of:

- **Main module**: `country_converter/country_converter.py` - Contains the `CountryConverter` class and core functionality
- **Data file**: `country_converter/country_data.tsv` - Tab-separated file with country data, regular expressions, and classification mappings
- **Command line interface**: Available as `coco` command after installation
- **Testing**: Comprehensive regex testing system that validates country name matching

Key architectural components:
- `CountryConverter` class: Main interface for all conversions
- Regular expression matching: Uses pandas DataFrame with regex patterns for flexible country name matching
- Multiple classification schemes: Supports 40+ different country classification standards (ISO, UN, EU, OECD, etc.)
- Pandas integration: Optimized `pandas_convert()` method for efficient Series processing

## Common Development Commands

### Using uv (modern package manager)
```bash
# Sync dependencies
uv sync --all-extras

# Run tests (fast)
uv run pytest -n auto

# Run full test suite with coverage
uv run coverage erase
uv run coverage run -m pytest --ruff --ruff-format
uv run coverage report

# Format code
uv run ruff format

# Lint code
uv run ruff check
uv run ruff check --fix  # Auto-fix issues
```

### Using poe (task runner)
```bash
# Sync dependencies
poe sync

# Format code
poe format

# Lint with ruff
poe check
poe check --fix

# Fast testing
poe test

# Full test suite with coverage
poe fulltest

# Complete build process (format + test)
poe build
```

### Legacy commands (still available)
```bash
# Format and test everything
./format_and_test.sh

# Manual formatting
ruff format .
ruff check . --fix

# Manual testing
pytest -n auto                    # Fast parallel testing
pytest --ruff --ruff-format      # With linting
coverage run -m pytest --ruff --ruff-format
coverage report
```

## Testing Strategy

The project uses a comprehensive testing approach:

1. **Regex validation**: Tests verify that country names match uniquely to their regular expressions
2. **Classification consistency**: Ensures short names and official names match correctly
3. **Alternative name testing**: Validates that alternative country names still resolve correctly
4. **Custom test data**: Add new test files starting with `test_regex_` to automatically include them

Test files are located in `tests/` directory with specific regex test files for different country name variants.

## Key Development Notes

- The core data is stored in `country_data.tsv` - any new classification can be added as a column
- Regular expressions in the data file must not break existing matches
- The package maintains backward compatibility as it's used in research projects
- Code style follows black formatting and ruff linting
- All new country classifications must be documented in README.md

## Data Structure

The main data structure is a pandas DataFrame loaded from `country_data.tsv` containing:
- Country names in various formats (short, official, alternative)
- Regular expressions for matching
- Classification codes for 40+ different schemes
- Membership information with years where applicable

## Command Line Interface

The package provides a `coco` command-line tool for country conversion:
```bash
coco Cyprus DE Denmark Estonia 4 'United Kingdom' AUT
coco AUT DEU VAT AUS -s ISO3 -t UNcode -o ', '
```