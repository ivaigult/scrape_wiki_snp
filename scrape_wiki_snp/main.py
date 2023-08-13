"""Command line main entrypoint."""

import argparse
import io
import sys
import typing
from dataclasses import dataclass

import yaml

from . import wiki_snp
from .download import download
from .dumper import Dumper


@dataclass
class Options:
    """
    Script's options.

    :param url: URL to scrape the data from.
    :param out: Where to write output data. If not set, write to stdout.
    """

    url: str
    out: typing.Optional[str]


def main(options: Options) -> int:
    """
    Main entry point.

    :param options: Program options.
    :return: Return code.
    """
    html = download(options.url)
    idx = wiki_snp.parse(html)

    if options.out is not None:
        with io.open(options.out, "w", encoding="utf-8") as out_file:
            yaml.dump(idx, out_file, Dumper)
    else:
        yaml.dump(idx, sys.stdout, Dumper)

    return 0


def cli_main() -> int:
    """
    Main command line entry point.

    :return: Return code.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="URL to scrape the data from.")
    parser.add_argument(
        "out",
        help="Where to write output data. " "If not set, write to stdout.",
        default=None,
        nargs="?",
    )

    args = parser.parse_args()

    return main(Options(args.url, args.out))


if __name__ == "__main__":
    sys.exit(cli_main())
