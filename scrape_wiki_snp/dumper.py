"""yaml dumper for index types."""

from __future__ import annotations

import typing

import yaml

from . import index


class Dumper(yaml.SafeDumper):
    """yaml dumper for index types class."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """
        Init dumper.

        :param args: Args to forward to SafeDumper constructor.
        :param kwargs: Keyword args to forward to SafeDumper constructor.
        """
        super().__init__(*args, **kwargs)

        self._node2component: typing.Dict[yaml.Node, index.Component] = {}

    def represent_component(self, component: index.Component) -> yaml.Node:
        """
        Represent index component.

        :param component: Component to represent.
        :return: yaml node dumped.
        """
        node = self.represent_mapping(
            index.Component.tag,
            {
                "symbol": component.symbol,
                "name": component.name,
            },
        )

        self._node2component[node] = component

        return node

    def represent_diff(self, diff: index.Diff) -> yaml.Node:
        """
        Represent index diff.

        :param diff: Index diff to represent.
        :return: yaml node dumped.
        """
        return self.represent_mapping(
            index.Diff.tag,
            {
                "date": diff.date,
                "added": diff.added,
                "removed": diff.removed,
                "reason": diff.reason,
            },
        )

    def represent_index(self, idx: index.Index) -> yaml.Node:
        """
        Represent index.

        :param idx: Index to represent.
        :return: yaml node dumped.
        """
        return self.represent_mapping(
            index.Index.tag,
            {
                "components": idx.components,
                "diffs": idx.diffs,
            },
        )

    def generate_anchor(self, node: yaml.Node) -> str:
        """
        Generate yaml anchor.

        :param node: node to generate anchor for.
        :return: Anchor string.
        """
        if isinstance(node, yaml.MappingNode) and node.tag == index.Component.tag:
            return self._node2component[node].symbol

        result: str = super().generate_anchor(node)  # type: ignore
        return result


Dumper.add_representer(index.Component, Dumper.represent_component)
Dumper.add_representer(index.Diff, Dumper.represent_diff)
Dumper.add_representer(index.Index, Dumper.represent_index)
