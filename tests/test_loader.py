"""Index loader unit test."""

import unittest

import yaml

from scrape_wiki_snp import index
from scrape_wiki_snp.loader import Loader


class LoaderTest(unittest.TestCase):
    "Loader class test."

    def test_parse_component(self) -> None:
        "Test index.Component parsing."
        yaml_str = """
        !index-component
        symbol: ABC
        name: A b c.
        """
        got = yaml.load(yaml_str, Loader)
        expected = index.Component("ABC", "A b c.")

        self.assertIsInstance(got, index.Component)
        self.assertEqual(expected, got)

    def test_parse_diff(self) -> None:
        "Test index.Diff parsing."
        yaml_str = """
        !index-diff
        date: Jan 1, 2000
        added: !index-component
          symbol: ABC
          name: A b c.
        removed: !index-component
          name: X y z.
          symbol: XYZ
        reason: Just because.
        """
        got = yaml.load(yaml_str, Loader)
        expected = index.Diff(
            "Jan 1, 2000",
            index.Component("ABC", "A b c."),
            index.Component("XYZ", "X y z."),
            "Just because.",
        )

        self.assertIsInstance(got, index.Diff)
        self.assertEqual(expected, got)

    def test_parse_index(self) -> None:
        "Test index.Index parsing."
        yaml_str = """
        !index
        components:
          - &ABC !index-component
            symbol: ABC
            name: A b c.
          - &XYZ !index-component
            symbol: XYZ
            name: X y z.
        diffs:
          - !index-diff
            date: Jan 1, 2000
            added: *ABC
            removed: *XYZ
            reason: Just because.
        """
        added = index.Component("ABC", "A b c.")
        removed = index.Component("XYZ", "X y z.")
        diff = index.Diff("Jan 1, 2000", added, removed, "Just because.")
        expected = index.Index([added, removed], [diff])

        got = yaml.load(yaml_str, Loader)

        self.assertIsInstance(got, index.Index)
        self.assertEqual(expected, got)
