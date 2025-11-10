from __future__ import annotations

import random
import socket
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, scrolledtext, ttk
from typing import Mapping, MutableMapping

from ..config.settings import (
    DEFAULT_BASE_IP,
    DEFAULT_DEVICE_PREFIX,
    DEFAULT_PACKET_PREFIX,
    GUI_STYLE,
    RANDOM_DEVICE_COUNT,
)
from ..datastructures.nodes import Node
from ..datastructures.splay_tree import SplayTree
from ..factories.tree_factory import TreeFactory


@dataclass
class DeviceInfo:
    name: str
    node: Node


class IPAddressFinderGUI:
    def __init__(self, root: tk.Tk, factory: TreeFactory) -> None:
        self.root = root
        self.root.title("Pencarian IP Address - Splay Tree")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.splay_tree: SplayTree = factory.create_tree()
        self.device_names: MutableMapping[str, str] = {}

        self._setup_gui()
        self._load_localhost_info()
        self._refresh_views()


    def _setup_gui(self) -> None:
        style = GUI_STYLE

        title_frame = tk.Frame(self.root, bg=style.background, pady=10)
        title_frame.pack(fill=tk.X)

        tk.Label(
            title_frame,
            text="🌐 IP Address Finder",
            font=("Arial", 20, "bold"),
            bg=style.background,
            fg=style.foreground,
        ).pack()

        tk.Label(
            title_frame,
            text="Management IP Router menggunakan Splay Tree",
            font=("Arial", 10),
            bg=style.background,
            fg=style.subtitle,
        ).pack()

        container = tk.Frame(self.root, padx=10, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        self._build_left_panel(container)
        self._build_right_panel(container)
        self._build_status_bar()

    def _build_left_panel(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        left_panel = tk.LabelFrame(
            parent,
            text="Panel Kontrol",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
        )
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

        info_frame = tk.LabelFrame(left_panel, text="Info Sistem", font=("Arial", 9, "bold"))
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.hostname_label = tk.Label(info_frame, text="Hostname: -", anchor="w")
        self.hostname_label.pack(fill=tk.X, pady=2)

        self.local_ip_label = tk.Label(info_frame, text="IP Lokal: -", anchor="w")
        self.local_ip_label.pack(fill=tk.X, pady=2)

        self.tree_size_label = tk.Label(info_frame, text="Jumlah Device: 0", anchor="w")
        self.tree_size_label.pack(fill=tk.X, pady=2)

        self.search_count_label = tk.Label(info_frame, text="Total Pencarian: 0", anchor="w")
        self.search_count_label.pack(fill=tk.X, pady=2)

        self._build_add_device_section(left_panel)
        self._build_search_section(left_panel)
        self._build_delete_section(left_panel)
        self._build_quick_actions(left_panel)

    def _build_add_device_section(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        frame = tk.LabelFrame(parent, text="Tambah Device", font=("Arial", 9, "bold"))
        frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text="Nama Device:").pack(anchor="w", pady=(5, 0))
        self.device_name_entry = tk.Entry(frame, width=25)
        self.device_name_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text="Alamat IP:").pack(anchor="w")
        self.ip_entry = tk.Entry(frame, width=25)
        self.ip_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text="Data Paket:").pack(anchor="w")
        self.packet_entry = tk.Entry(frame, width=25)
        self.packet_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            frame,
            text="➕ Tambah Device",
            command=self._handle_add_device,
            bg=style.button_add,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=(5, 0))

    def _build_search_section(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        frame = tk.LabelFrame(parent, text="Cari Device", font=("Arial", 9, "bold"))
        frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text="IP Address:").pack(anchor="w", pady=(5, 0))
        self.search_entry = tk.Entry(frame, width=25)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            frame,
            text="🔍 Cari",
            command=self._handle_search_device,
            bg=style.button_search,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=(5, 0))

    def _build_delete_section(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        frame = tk.LabelFrame(parent, text="Hapus Device", font=("Arial", 9, "bold"))
        frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text="IP Address:").pack(anchor="w", pady=(5, 0))
        self.delete_entry = tk.Entry(frame, width=25)
        self.delete_entry.pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            frame,
            text="🗑️ Hapus",
            command=self._handle_delete_device,
            bg=style.button_delete,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=(5, 0))

    def _build_quick_actions(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        frame = tk.LabelFrame(parent, text="Aksi Cepat", font=("Arial", 9, "bold"))
        frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            frame,
            text="📊 Tampilkan Semua Device",
            command=self._handle_show_all_devices,
            bg=style.button_show_all,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            frame,
            text="🎲 Buat Device Random",
            command=self._handle_generate_random_devices,
            bg=style.button_generate,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            frame,
            text="🔄 Hapus Semua",
            command=self._handle_clear_all,
            bg=style.button_clear,
            fg=GUI_STYLE.foreground,
            font=("Arial", 9, "bold"),
            cursor="hand2",
        ).pack(fill=tk.X, pady=2)

    def _build_right_panel(self, parent: tk.Widget) -> None:
        style = GUI_STYLE
        right_panel = tk.Frame(parent)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.tree_display = scrolledtext.ScrolledText(
            notebook,
            wrap=tk.WORD,
            font=("Courier New", 9),
            bg=style.tree_background,
        )
        notebook.add(self.tree_display, text="🌳 Struktur Tree")

        self.device_list_display = scrolledtext.ScrolledText(
            notebook,
            wrap=tk.WORD,
            font=("Courier New", 9),
            bg=style.tree_background,
        )
        notebook.add(self.device_list_display, text="📋 Daftar Device")

        self.log_display = scrolledtext.ScrolledText(
            notebook,
            wrap=tk.WORD,
            font=("Courier New", 9),
            bg=style.tree_background,
        )
        notebook.add(self.log_display, text="📝 Log Aktivitas")

    def _build_status_bar(self) -> None:
        self.status_bar = tk.Label(
            self.root,
            text="Siap",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=GUI_STYLE.status_background,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)


    def _handle_add_device(self) -> None:
        device_name = self.device_name_entry.get().strip()
        ip_address = self.ip_entry.get().strip()
        packet = self.packet_entry.get().strip()

        if not ip_address:
            messagebox.showwarning("Peringatan", "Wajib masukin IP Address dulu!")
            return
        if not self._validate_ip(ip_address):
            messagebox.showerror("Error", "Format IP Address nya salah!")
            return

        if not device_name:
            device_name = f"{DEFAULT_DEVICE_PREFIX}{ip_address.split('.')[-1]}"
        if not packet:
            packet = f"{DEFAULT_PACKET_PREFIX}{random.randint(1000, 9999)}"

        is_new = self.splay_tree.insert(ip_address, packet)
        self.device_names[ip_address] = device_name

        if is_new:
            self._log_message(f"Device baru ditambahkan: {device_name} ({ip_address}) - Packet: {packet}")
            messagebox.showinfo("Berhasil", f"Device {device_name} udah ditambahin!")
        else:
            self._log_message(f"Data diupdate: {device_name} ({ip_address}) - Packet: {packet}")
            messagebox.showinfo("Info", f"IP {ip_address} udah ada, jadi cuma update data packet aja!")

        self.device_name_entry.delete(0, tk.END)
        self.ip_entry.delete(0, tk.END)
        self.packet_entry.delete(0, tk.END)
        self._refresh_views()

    def _handle_search_device(self) -> None:
        ip_address = self.search_entry.get().strip()
        if not ip_address:
            messagebox.showwarning("Peringatan", "Isi IP Address dulu ya!")
            return

        node = self.splay_tree.search(ip_address)
        if node:
            device_name = self.device_names.get(ip_address, "Device Gak Dikenal")
            self._log_message(f"Ketemu nih: {device_name} ({ip_address}) - Packet: {node.data_packet}")
            messagebox.showinfo(
                "Hasil Pencarian",
                "\n".join(
                    [
                        "Device Ketemu!",
                        f"Nama: {device_name}",
                        f"IP Address: {node.ip_address}",
                        f"Data Packet: {node.data_packet}",
                        "",
                        "Catatan: Device udah dipindah ke root biar lebih cepet dicari nanti.",
                    ]
                ),
            )
            self._refresh_views()
        else:
            self._log_message(f"Gagal: IP {ip_address} gak ketemu")
            messagebox.showwarning("Gak Ketemu", f"IP Address {ip_address} gak ada di jaringan!")
        self.search_entry.delete(0, tk.END)

    def _handle_delete_device(self) -> None:
        ip_address = self.delete_entry.get().strip()
        if not ip_address:
            messagebox.showwarning("Peringatan", "Isi IP Address dulu ya!")
            return

        device_name = self.device_names.get(ip_address, "Device Gak Dikenal")
        if not messagebox.askyesno("Konfirmasi Hapus", f"Yakin mau hapus {device_name} ({ip_address})?"):
            return

        success = self.splay_tree.delete(ip_address)
        if success:
            self.device_names.pop(ip_address, None)
            self._log_message(f"Dihapus: {device_name} ({ip_address})")
            messagebox.showinfo("Berhasil", f"Device {device_name} udah dihapus!")
            self._refresh_views()
        else:
            self._log_message(f"Gagal hapus: IP {ip_address} gak ketemu")
            messagebox.showwarning("Gak Ketemu", f"IP Address {ip_address} gak ada!")

        self.delete_entry.delete(0, tk.END)

    def _handle_show_all_devices(self) -> None:
        nodes = self.splay_tree.inorder_traversal()
        if not nodes:
            messagebox.showinfo("Daftar Device", "Belum ada device yang terdaftar!")
            return

        lines = [f"Jumlah Device: {len(nodes)}", "=" * 50, ""]
        for index, node in enumerate(nodes, start=1):
            device_name = self.device_names.get(node.ip_address, "Device Gak Dikenal")
            lines.extend(
                [
                    f"{index}. {device_name}",
                    f"   IP: {node.ip_address}",
                    f"   Packet: {node.data_packet}",
                    "",
                ]
            )

        self._show_message_window("Daftar Semua Device (Urut berdasar IP)", "\n".join(lines))
        self._log_message(f"Menampilkan {len(nodes)} device")

    def _handle_generate_random_devices(self) -> None:
        generated = 0
        for index in range(RANDOM_DEVICE_COUNT):
            ip_address = f"{DEFAULT_BASE_IP}{random.randint(1, 254)}"
            packet = f"{DEFAULT_PACKET_PREFIX}{random.randint(1000, 9999)}"
            device_name = f"{DEFAULT_DEVICE_PREFIX}{index + 1}"

            if self.splay_tree.insert(ip_address, packet):
                self.device_names[ip_address] = device_name
                generated += 1
        if generated:
            self._log_message(f"Dibuat {generated} device random")
            messagebox.showinfo("Berhasil", f"Berhasil bikin {generated} device random!")
            self._refresh_views()
        else:
            messagebox.showinfo("Info", "Semua IP yang digenerate udah ada!")

    def _handle_clear_all(self) -> None:
        if not messagebox.askyesno("Konfirmasi Hapus Semua", "Yakin mau hapus semua device?"):
            return
        self.splay_tree = SplayTree()
        self.device_names.clear()
        self._log_message("Semua device udah dihapus")
        self._refresh_views()
        messagebox.showinfo("Berhasil", "Semua device udah dihapus!")


    def _load_localhost_info(self) -> None:
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except OSError as exc:  # pragma: no cover - depends on environment
            self._log_message(f"Error loading localhost info: {exc}")
            return
        self.hostname_label.config(text=f"Hostname: {hostname}")
        self.local_ip_label.config(text=f"IP Lokal: {local_ip}")
        self._log_message(f"System initialized - Hostname: {hostname}, IP: {local_ip}")

    def _refresh_views(self) -> None:
        self.tree_size_label.config(text=f"Jumlah Device: {self.splay_tree.size}")
        self.search_count_label.config(
            text=f"Total Pencarian: {self.splay_tree.search_count}"
        )

        self.tree_display.delete(1.0, tk.END)
        self.tree_display.insert(tk.END, self.splay_tree.get_tree_structure())

        self.device_list_display.delete(1.0, tk.END)
        nodes = self.splay_tree.inorder_traversal()
        if nodes:
            self.device_list_display.insert(tk.END, "=" * 60 + "\n")
            self.device_list_display.insert(tk.END, "DAFTAR DEVICE (Urut berdasar IP Address)\n")
            self.device_list_display.insert(tk.END, f"Total Device: {len(nodes)}\n")
            self.device_list_display.insert(tk.END, "=" * 60 + "\n\n")
            for index, node in enumerate(nodes, start=1):
                device_name = self.device_names.get(node.ip_address, "Device Gak Dikenal")
                self.device_list_display.insert(tk.END, f"{index}. {device_name}\n")
                self.device_list_display.insert(tk.END, f"   Alamat IP   : {node.ip_address}\n")
                self.device_list_display.insert(tk.END, f"   Data Paket  : {node.data_packet}\n")
                self.device_list_display.insert(tk.END, "-" * 60 + "\n")
        else:
            self.device_list_display.insert(tk.END, "Belum ada device yang terdaftar.\n")

        self.status_bar.config(
            text=f"Status: {self.splay_tree.size} device terdaftar, {self.splay_tree.search_count} kali pencarian"
        )

    def _validate_ip(self, ip_address: str) -> bool:
        parts = ip_address.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    def _log_message(self, message: str) -> None:
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_display.see(tk.END)

    def _show_message_window(self, title: str, message: str) -> None:
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("500x400")
        text_widget = scrolledtext.ScrolledText(
            window, wrap=tk.WORD, font=("Courier New", 9)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)
        tk.Button(
            window,
            text="Tutup",
            command=window.destroy,
            bg=GUI_STYLE.button_search,
            fg=GUI_STYLE.foreground,
            font=("Arial", 10, "bold"),
        ).pack(pady=5)
