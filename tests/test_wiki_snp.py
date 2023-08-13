"""snp index parsed unit test."""

from __future__ import annotations

import typing
import unittest

import bs4
from parameterized import parameterized  # type: ignore

from scrape_wiki_snp import index, wiki_snp

_DIFFS_HEADER = """
<thead>
<tr>
  <th rowspan="2">Date</th>
  <th colspan="2">Added</th>
  <th colspan="2">Removed</th>
  <th rowspan="2">Reason</th>
</tr>
<tr>
  <th>Ticker</th><th>Security</th>
  <th>Ticker</th><th>Security</th>
</tr>
</thead>
"""


def to_html_row(component: typing.Optional[index.Component]) -> str:
    """
    Convert index component to a html table row.

    :param component: Component to convert.
    :return: html row converted.
    """
    if not component:
        return "<td></td><td></td>"
    return f"<td>{component.symbol}</td><td>{component.name}</td>"


class WikiSnpTest(unittest.TestCase):
    "snp index parsed unit test."

    @parameterized.expand(  # type: ignore
        [
            ("Ticker symbol", "Security"),
            ("Symbol", "Security"),
            ("Ticker", "Security"),
            ("Ticker", "Company"),
            ("Ticker\n", "Company\n"),
        ]
    )
    def test_parse_components(self, symbol_hdr, company_hdr) -> None:
        """
        Test components parsing.

        :param symbol_hdr: Symbol header name.
        :param company_hdr: Company header name.
        """
        expected = index.Component("ABC", "A b c.")
        html = f"""<table>
        <thead>
        <tr><th>{symbol_hdr}</th><th>{company_hdr}</th></tr>
        </thead>
        <tbody>
        <tr>{to_html_row(expected)}</tr>
        </tbody>
        </table>
        """

        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        assert isinstance(table, bs4.Tag)

        components = wiki_snp.parse_components(table)

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0], expected)

    @parameterized.expand(  # type: ignore
        [
            (
                index.Diff(
                    "June 8, 2022",
                    index.Component("ABC", "A b c."),
                    index.Component("XYZ", "X y z."),
                    "Market capitalization change.",
                ),
            ),
            (
                index.Diff(
                    "June 8, 2022",
                    None,
                    index.Component("XYZ", "X y z."),
                    "Market capitalization change.",
                ),
            ),
            (
                index.Diff(
                    "June 8, 2022",
                    index.Component("ABC", "A b c."),
                    None,
                    "Market capitalization change.",
                ),
            ),
        ]
    )
    def xtest_parse_diffs(self, expected: index.Diff) -> None:
        """
        Test index diffs parsing (no colspan).
        """
        html = f"""
        <table>
        {_DIFFS_HEADER}
        <tbody>
        <tr>
          <td>June 8, 2022</td>
          {to_html_row(expected.added)}
          {to_html_row(expected.removed)}
          <td>Market capitalization change.</td>
        </tr>
        </tbody>
        </table>
        """

        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        assert isinstance(table, bs4.Tag)

        diffs = wiki_snp.parse_diffs(table)

        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0], expected)

    def test_pare_diffs_rowspan(self) -> None:
        """
        Test index diffs parsing (with colspan).
        """
        diff1 = index.Diff(
            "June 8, 2022",
            index.Component("AAA", "A a a."),
            index.Component("BBB", "B b b."),
            "Market capitalization change.",
        )
        diff2 = index.Diff(
            "June 8, 2022",
            index.Component("CCC", "C c c."),
            index.Component("DDD", "D d d."),
            "Market capitalization change.",
        )
        diff3 = index.Diff(
            "June 9, 2022",
            index.Component("EEE", "E e e."),
            index.Component("FFF", "F f f."),
            "FFF was acquired by XXX.",
        )

        html = f"""
        <table>
        {_DIFFS_HEADER}
        <tbody>
        <tr>
          <td rowspan="2">{diff1.date}</td>
          {to_html_row(diff1.added)}
          {to_html_row(diff1.removed)}
          <td rowspan="2">{diff1.reason}</td>
        </tr>
        <tr>
          {to_html_row(diff2.added)}
          {to_html_row(diff2.removed)}
        </tr>
        <tr>
          <td>{diff3.date}</td>
          {to_html_row(diff3.added)}
          {to_html_row(diff3.removed)}
          <td>{diff3.reason}</td>
        </tr>

        </tbody>
        </table>
        """

        soup = bs4.BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        self.assertIsNotNone(table)

        diffs = wiki_snp.parse_diffs(typing.cast(bs4.element.Tag, table))

        self.assertEqual(diffs, [diff1, diff2, diff3])

    @parameterized.expand(  # type: ignore
        [
            (
                """
            <table>one</table>
            <table>two</table>
            """,
                0,
                1,
            ),
            (
                """
            <table>one</table>
            <table>two</table>
            <table>three</table>
            """,
                1,
                2,
            ),
        ]
    )
    def test_parse_index(self, html: str, components_idx: int, diffs_idx: int) -> None:
        """
        Test index parsing.

        :param html: html to parse.
        :param components_idx: Talbe index with the components.
        :param diffs_idx: Talbe index with the diffs.
        """
        soup = bs4.BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")

        parse_componetns_called = False
        parse_diffs_called = False

        def _parse_componetns(table: bs4.element.Tag) -> typing.List[index.Component]:
            nonlocal parse_componetns_called
            self.assertEqual(table, tables[components_idx])
            parse_componetns_called = True

            return []

        def _parse_diffs(table: bs4.element.Tag) -> typing.List[index.Diff]:
            nonlocal parse_diffs_called
            self.assertEqual(table, tables[diffs_idx])
            parse_diffs_called = True

            return []

        wiki_snp.parse(html, _parse_componetns, _parse_diffs)

        self.assertTrue(parse_componetns_called)
        self.assertTrue(parse_diffs_called)
