from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from .nodes import Node


@dataclass
class SplayTree:

    root: Optional[Node] = None
    size: int = 0
    search_count: int = 0
    _comparison_trace: List[str] = field(default_factory=list, init=False, repr=False)


    def _left_rotate(self, x: Node) -> None:
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node) -> None:
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


    def _splay(self, node: Node) -> None:
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:
                self._left_rotate(parent)
                self._right_rotate(parent)
            else:
                self._right_rotate(parent)
                self._left_rotate(parent)


    def insert(self, ip_address: str, data_packet: Optional[str] = None) -> bool:
        node = Node(ip_address, data_packet)
        parent: Optional[Node] = None
        current = self.root

        while current:
            parent = current
            if node.ip_address < current.ip_address:
                current = current.left
            elif node.ip_address > current.ip_address:
                current = current.right
            else:
                current.data_packet = data_packet
                self._splay(current)
                return False

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.ip_address < parent.ip_address:
            parent.left = node
        else:
            parent.right = node

        self._splay(node)
        self.size += 1
        return True

    def _find_node(self, ip_address: str) -> Optional[Node]:
        """Mencari node tanpa splay dan tanpa increment search_count."""
        current = self.root
        while current:
            if ip_address < current.ip_address:
                current = current.left
            elif ip_address > current.ip_address:
                current = current.right
            else:
                return current
        return None

    def search(self, ip_address: str) -> Optional[Node]:
        self.search_count += 1
        current = self.root
        while current:
            if ip_address < current.ip_address:
                current = current.left
            elif ip_address > current.ip_address:
                current = current.right
            else:
                self._splay(current)
                return current
        return None

    def delete(self, ip_address: str) -> bool:
        node = self.search(ip_address)
        if node is None:
            return False

        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            successor = self._minimum(node.right)
            if successor.parent is not node:
                self._replace(successor, successor.right)
                successor.right = node.right
                if successor.right:
                    successor.right.parent = successor
            self._replace(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor

        self.size -= 1
        return True

    def update(
        self,
        old_ip_address: str,
        new_ip_address: str | None = None,
        new_data_packet: str | None = None
    ) -> tuple[bool, str | None, str | None]:
        """
        Update IP address dan/atau data_packet pada node yang sudah ada.
        
        Jika IP berubah, akan delete node lama dan insert node baru.
        Node yang diupdate akan di-splay ke root.
        
        Args:
            old_ip_address: IP address yang akan diupdate
            new_ip_address: IP address baru (opsional, None = tidak diubah)
            new_data_packet: Data packet baru (opsional, None = tidak diubah)
            
        Returns:
            tuple: (success: bool, old_ip: str | None, old_packet: str | None)
        """
        # Cari node yang akan diupdate (tanpa splay, tanpa increment counter)
        node = self._find_node(old_ip_address)
        if node is None:
            return (False, None, None)
        
        old_packet = node.data_packet
        
        # Jika IP tidak berubah, hanya update packet
        if new_ip_address is None or new_ip_address == old_ip_address:
            if new_data_packet is not None:
                node.data_packet = new_data_packet
            # Splay node ke root setelah update
            self._splay(node)
            return (True, None, old_packet)
        
        # IP berubah: delete lama, insert baru
        # Simpan packet yang akan digunakan
        packet_to_use = new_data_packet if new_data_packet is not None else old_packet
        
        # Delete node lama (ini akan splay successor/predecessor)
        self.delete(old_ip_address)
        
        # Insert node baru (ini akan splay node baru ke root)
        self.insert(new_ip_address, packet_to_use)
        
        return (True, old_ip_address, old_packet)

    def inorder_traversal(self) -> List[Node]:
        result: List[Node] = []
        self._inorder_helper(self.root, result)
        return result

    def get_tree_structure(self) -> str:
        if self.root is None:
            return "Tree is empty\n"
        lines: List[str] = []
        self._tree_structure_helper(self.root, "", True, lines)
        return "".join(lines)


    def _replace(self, u: Node, v: Optional[Node]) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _minimum(self, node: Node) -> Node:
        current = node
        while current.left:
            current = current.left
        return current

    def _inorder_helper(self, node: Optional[Node], result: List[Node]) -> None:
        if node is None:
            return
        self._inorder_helper(node.left, result)
        result.append(node)
        self._inorder_helper(node.right, result)

    def _tree_structure_helper(
        self, node: Optional[Node], prefix: str, is_tail: bool, result: List[str]
    ) -> None:
        if node is None:
            return
        connector = "└── " if is_tail else "├── "
        result.append(prefix + connector + f"{node.ip_address} (Packet: {node.data_packet})\n")
        children: List[Optional[Node]] = [child for child in (node.left, node.right) if child]
        for index, child in enumerate(children):
            next_prefix = prefix + ("    " if is_tail else "│   ")
            self._tree_structure_helper(child, next_prefix, index == len(children) - 1, result)


    @classmethod
    def from_iterable(cls, items: Iterable[tuple[str, str | None]]) -> "SplayTree":
        tree = cls()
        for ip_address, packet in items:
            tree.insert(ip_address, packet)
        return tree
