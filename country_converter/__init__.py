"""Country converter coco.

Standard abbreviation for that module: coco
"""

from country_converter.country_converter import (
    CountryConverter,
    agg_conc,
    cli_output,
    convert,
    main,
    match,
)

from .version import __version__

__author__ = "Konstantin Stadler"
__all__ = ["CountryConverter", "__version__", "agg_conc", "cli_output", "convert", "main", "match"]
