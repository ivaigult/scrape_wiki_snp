"""Pare S&P index data from a wiki page."""

import re
import typing

import bs4

from . import index


class ParseError(Exception):
    """HTML parsing error."""


_SYMBOL_REGEX = re.compile("^(Ticker symbol|Symbol|Ticker)$")
_NAME_REGEX = re.compile("^(Security|Company)$")


def parse_components(table: bs4.element.Tag) -> typing.List[index.Component]:
    """
    Parse current index components.

    :param table: Table tag to parse.
    :return: List of components parsed.
    """
    symbol_idx = -1
    name_idx = -1

    for idx, tag_th in enumerate(table.find_all("th")):
        text = tag_th.getText()
        if _SYMBOL_REGEX.match(text):
            symbol_idx = idx
        elif _NAME_REGEX.match(text):
            name_idx = idx

    if symbol_idx == -1:
        raise ParseError("'Symbol' column not found")
    if name_idx == -1:
        raise ParseError("'Name' column not found")

    result = []

    for row in table.find_all("tr")[1:]:
        cells = [cell.getText().strip() for cell in row.find_all("td")]

        result.append(index.Component(cells[symbol_idx], cells[name_idx]))

    return result


_DIFFS_HEADER = [
    "Date",
    "Added",
    "Removed",
    "Reason",
    "Ticker",
    "Security",
    "Ticker",
    "Security",
]

_DATE_IDX = 0
_ADDED_SYM_IDX = 1
_ADDED_NAME_IDX = 2
_REMOVED_SYM_IDX = 3
_REMOVED_NAME_IDX = 4
_REASON_IDX = 5


def parse_diffs(table: bs4.element.Tag) -> typing.List[index.Diff]:
    """
    Parse index changes.

    :param table: Tale tag to parse.
    :return: List of index diffs parsed.
    """
    header_names = [hdr.getText().strip() for hdr in table.find_all("th")]

    if header_names != _DIFFS_HEADER:
        raise ParseError("Diffs table structure is not recognized")

    result = []

    date_tag = None
    date_counter = 0
    reason_tag = None
    reason_counter = 0

    for row in table.find_all("tr")[2:]:
        td_tags = list(row.find_all("td"))

        if date_counter:
            td_tags = [date_tag] + td_tags
        if reason_counter:
            td_tags = td_tags + [reason_tag]

        if not date_counter:
            date_tag = td_tags[_DATE_IDX]
            date_counter = int(date_tag.get("rowspan", 0))
        if not reason_counter:
            reason_tag = td_tags[_REASON_IDX]
            reason_counter = int(reason_tag.get("rowspan", 0))

        cells = [cell.getText().strip() for cell in td_tags]

        added: typing.Optional[index.Component] = None
        removed: typing.Optional[index.Component] = None

        if cells[_ADDED_SYM_IDX]:
            added = index.Component(cells[_ADDED_SYM_IDX], cells[_ADDED_NAME_IDX])
        if cells[_REMOVED_SYM_IDX]:
            removed = index.Component(cells[_REMOVED_SYM_IDX], cells[_REMOVED_NAME_IDX])

        date = cells[_DATE_IDX]
        reason = cells[_REASON_IDX]

        result.append(index.Diff(date, added, removed, reason))

        date_counter = max(date_counter - 1, 0)
        reason_counter = max(reason_counter - 1, 0)

    return result


_ParseComponentsFn = typing.Callable[[bs4.element.Tag], typing.List[index.Component]]
_ParseDiffsFn = typing.Callable[[bs4.element.Tag], typing.List[index.Diff]]


def parse(
    stream: str,
    parse_components_fn: _ParseComponentsFn = parse_components,
    parse_diffs_fn: _ParseDiffsFn = parse_diffs,
) -> index.Index:
    """
    Pare S&P index data from a wiki page.

    :param stream: Stream to parse.
    :param parse_components_fn: Parse components function (unit tests only).
    :param parse_diffs_fn: Parse diffs function (unit tests only).
    :return: index object parsed.
    """
    soup = bs4.BeautifulSoup(stream, "html.parser")

    tables = soup.find_all("table")

    if len(tables) != 2:
        components = parse_components_fn(tables[1])
        diffs = parse_diffs_fn(tables[2])
    else:
        components = parse_components_fn(tables[0])
        diffs = parse_diffs_fn(tables[1])

    return index.Index(components, diffs)
