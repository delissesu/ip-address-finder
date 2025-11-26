from __future__ import annotations

import tkinter as tk

from src.factories.tree_factory import DefaultTreeFactory
from src.gui.app import IPAddressFinderGUI


def main() -> None:
    root = tk.Tk()
    factory = DefaultTreeFactory()
    IPAddressFinderGUI(root, factory)
    root.mainloop()


if __name__ == "__main__":
    main()
