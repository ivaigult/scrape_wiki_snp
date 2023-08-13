"""Setup package."""

from __future__ import annotations

import typing

from setuptools import setup


def _long_description() -> str:
    """
    Parse README.md.

    :return: Readme file parsed.
    """
    with open("README.md", "r", encoding="utf-8") as readme:
        return readme.read()


def _install_requires() -> typing.List[str]:
    """
    Parse requirements files.

    :return: List of requirements.
    """
    requirements: typing.List[str] = []

    with open("requirements/common.txt", "r", encoding="utf-8") as common:
        requirements += common.read().splitlines()

    with open("requirements/prod.txt", "r", encoding="utf-8") as prod:
        requirements += prod.read().splitlines()

    requirements = [req for req in requirements if not req.startswith("-r")]

    return requirements


setup(
    name="scrape_wiki_snp",
    version="0.0.1",
    description="Scrapes Wikipedia pages to get S&P indices components.",
    license="MIT",
    long_description=_long_description(),
    author="Ivan Vaigult",
    author_email="i.vaigult@gmail.com",
    packages=["scrape_wiki_snp"],
    install_requires=_install_requires(),
    python_requires=">=3.11",
)
