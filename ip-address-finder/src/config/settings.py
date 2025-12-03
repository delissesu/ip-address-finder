from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuiStyle:

    background: str = "#2c3e50"
    foreground: str = "white"
    subtitle: str = "#ecf0f1"
    tree_background: str = "#f8f9fa"
    status_background: str = "#ecf0f1"
    button_add: str = "#27ae60"
    button_search: str = "#3498db"
    button_delete: str = "#e74c3c"
    button_update: str = "#e67e22"
    button_generate: str = "#f39c12"
    button_show_all: str = "#9b59b6"
    button_clear: str = "#95a5a6"


GUI_STYLE = GuiStyle()

RANDOM_DEVICE_COUNT: int = 11
DEFAULT_BASE_IP: str = "192.168.1."
DEFAULT_PACKET_PREFIX: str = "PKT-"
DEFAULT_DEVICE_PREFIX: str = "Device-"
