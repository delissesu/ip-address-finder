from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..datastructures.nodes import Node
from ..datastructures.splay_tree import SplayTree


class TreeFactory(Protocol):
    def create_tree(self) -> SplayTree: ...


@dataclass
class DefaultTreeFactory:

    def create_tree(self) -> SplayTree:
        return SplayTree()


@dataclass
class PreloadedTreeFactory:

    initial_nodes: tuple[tuple[str, str | None], ...]

    def create_tree(self) -> SplayTree:
        return SplayTree.from_iterable(self.initial_nodes)


def create_node(ip_address: str, data_packet: str | None = None) -> Node:

    return Node(ip_address=ip_address, data_packet=data_packet)
