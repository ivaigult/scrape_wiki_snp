"""Index dumper unit test."""

import unittest

import yaml

from scrape_wiki_snp import index
from scrape_wiki_snp.dumper import Dumper


class DumperTest(unittest.TestCase):
    """Dumper class test."""

    def test_dump_component(self) -> None:
        """Test `index.Component` dumpling."""
        component = index.Component("ABC", "A b c.")

        result: str = yaml.dump(component, None, Dumper, sort_keys=False)

        self.assertEqual(
            result, "!index-component\n" + "symbol: ABC\n" + "name: A b c.\n"
        )

    def test_dump_diff(self) -> None:
        """Test `index.Diff` dumpling."""
        added = index.Component("ABC", "A b c.")
        removed = index.Component("XYZ", "X y z.")

        with self.subTest("added_and_removed"):
            diff = index.Diff("01-02-2020", added, removed, "Just because.")
            result: str = yaml.dump(diff, None, Dumper, sort_keys=False)

            self.assertEqual(
                result,
                "!index-diff\n"
                "date: 01-02-2020\n"
                "added: !index-component\n"
                "  symbol: ABC\n"
                "  name: A b c.\n"
                "removed: !index-component\n"
                "  symbol: XYZ\n"
                "  name: X y z.\n"
                "reason: Just because.\n",
            )

        with self.subTest("added_only"):
            diff = index.Diff("01-02-2020", added, None, "Just because.")
            result = yaml.dump(diff, None, Dumper, sort_keys=False)

            self.assertEqual(
                result,
                "!index-diff\n"
                "date: 01-02-2020\n"
                "added: !index-component\n"
                "  symbol: ABC\n"
                "  name: A b c.\n"
                "removed: null\n"
                "reason: Just because.\n",
            )

    def test_dump_index(self) -> None:
        """Test `index.Index` dumpling."""
        added = index.Component("ABC", "A b c.")
        removed = index.Component("XYZ", "X y z.")

        diff = index.Diff("01-02-2020", added, removed, "Just because.")

        idx = index.Index([added], [diff])

        result: str = yaml.dump(idx, None, Dumper, sort_keys=False)

        self.assertEqual(
            result,
            "!index\n"
            "components:\n"
            "- &ABC !index-component\n"
            "  symbol: ABC\n"
            "  name: A b c.\n"
            "diffs:\n"
            "- !index-diff\n"
            "  date: 01-02-2020\n"
            "  added: *ABC\n"
            "  removed: !index-component\n"
            "    symbol: XYZ\n"
            "    name: X y z.\n"
            "  reason: Just because.\n",
        )
