import argparse
import logging

import country_converter as coco

# Instantiate once for all instances
print("Instantiation of CountryConverter obj ...")
cc = coco.CountryConverter()
print("Done")


def parse_args():
    parser = argparse.ArgumentParser(description="Profiling disco performance")
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        required=True,
        help="Provide filepath to the file with a list of names to process",
    )

    return parser.parse_args()


def read_names(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f_names:
        for line in f_names:
            yield line.strip()


def clean_all_names(filepath: str):
    try:
        cc._apply_multiregex.cache_clear()
    except Exception:
        pass
    logging.basicConfig(level=logging.ERROR)
    names = read_names(filepath)
    cc.convert(names=names, to="name_short")
    print(".", sep="")


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()
    filepath = args.data
    clean_all_names(filepath)


if __name__ == "__main__":
    main()
