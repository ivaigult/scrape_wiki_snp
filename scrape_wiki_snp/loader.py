"""yaml loader for index types."""

from __future__ import annotations

import yaml

from . import index


class LoaderException(Exception):
    """Loader exception class."""


# pylint: disable=too-many-ancestors
class Loader(yaml.SafeLoader):
    """yaml loader for index types class."""

    def parse_component(self, node: yaml.Node) -> index.Component:
        """
        Parsse component from a yaml node.

        :param node: Node to parse.
        :return: Component parsed.
        """
        if not isinstance(node, yaml.MappingNode):
            raise LoaderException("Expected a mapping node")

        try:
            args = self.construct_mapping(node)
            return index.Component(**args)  # type: ignore
        except TypeError as exc:
            raise LoaderException("Type error while parsing.") from exc

    def parse_diff(self, node: yaml.Node) -> index.Diff:
        """
        Parsse diff from a yaml node.

        :param node: Node to parse.
        :return: Diff parsed.
        """
        if not isinstance(node, yaml.MappingNode):
            raise LoaderException("Expected a mapping node")

        try:
            args = self.construct_mapping(node)
            return index.Diff(**args)  # type: ignore
        except TypeError as exc:
            raise LoaderException("Type error while parsing.") from exc

    def parse_index(self, node: yaml.Node) -> index.Index:
        """
        Parsse index from a yaml node.

        :param node: Node to parse.
        :return: Index parsed.
        """
        if not isinstance(node, yaml.MappingNode):
            raise LoaderException("Expected a mapping node")

        args = self.construct_mapping(node, deep=True)

        try:
            args = self.construct_mapping(node)
            return index.Index(**args)  # type: ignore
        except TypeError as exc:
            raise LoaderException("Type error while parsing.") from exc


Loader.add_constructor(index.Component.tag, Loader.parse_component)
Loader.add_constructor(index.Diff.tag, Loader.parse_diff)
Loader.add_constructor(index.Index.tag, Loader.parse_index)
