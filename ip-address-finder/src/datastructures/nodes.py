from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:

    ip_address: str
    data_packet: str | None = None
    left: Optional[Node] = field(default=None, repr=False)
    right: Optional[Node] = field(default=None, repr=False)
    parent: Optional[Node] = field(default=None, repr=False)

    def __str__(self) -> str:
        packet = self.data_packet or "-"
        return f"IP: {self.ip_address}, Packet: {packet}"
