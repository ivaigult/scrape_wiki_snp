"""Index data types."""


import typing
from dataclasses import dataclass


@dataclass
class Component:
    """
    Index component.

    :param symbol: Ticker symbol.
    :param name: Component name.
    """

    tag: typing.ClassVar[str] = "!index-component"

    symbol: str
    name: str


@dataclass
class Diff:
    """
    Index change.

    :param date: Date diff happened.
    :param added: Component added, if any.
    :param removed: Component removed, if any.
    :param reason: Reason for the change.
    """

    tag: typing.ClassVar[str] = "!index-diff"

    date: str
    added: typing.Optional[Component]
    removed: typing.Optional[Component]
    reason: str


@dataclass
class Index:
    """
    Index description.

    :param components: List of components now.
    :param diffs: Component changes.
    """

    tag: typing.ClassVar[str] = "!index"
    components: typing.List[Component]
    diffs: typing.List[Diff]
