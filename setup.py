from setuptools import setup

exec(open("country_converter/version.py").read())

setup(
    name="country_converter",
    description=(
        "The country converter (coco) - "
        "a Python package for converting country names "
        "between different classifications schemes."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    url="https://github.com/konstantinstadler/country_converter",
    author="Konstantin Stadler",
    author_email="konstantin.stadler@ntnu.no",
    version=__version__,  # noqa
    packages=["country_converter"],
    package_data={"country_converter": ["country_data.tsv", "../LICENSE"]},
    entry_points={
        "console_scripts": ["coco = country_converter.country_converter:main"]
    },
    install_requires=["pandas >= 1.0"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)
