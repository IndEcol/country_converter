from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("country_converter")
except PackageNotFoundError:
    __version__ = "unknown"
