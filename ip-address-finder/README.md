# IP Address Finder

<p align="center">
<a href="https://github.com/delissesu/Hello-Wold-and-Other-Disasters"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version"></a>
<a href="https://github.com/delissesu/Hello-Wold-and-Other-Disasters"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
</p>

## About IP Address Finder

IP Address Finder adalah aplikasi GUI yang aku gunakan untuk memenuhi proyek akhir  mata kuliah Struktur Data yang bertujuan menerapkan konsep struktur data tingkat lanjut dalam studi kasus atau real case. Aplikasi ini sederhananya digunakan untuk mengelola dan memvisualisasikan IP address dalam jaringan lokal menggunakan struktur data Splay Tree. Aplikasi ini mengimplementasikan beberapa hal berikut:

-  **Splay Tree Implementation** - Menggunakan self-adjusting BST untuk akses
-  **Fast Search Operations** - Recently accessed nodes dibawa ke root
-  **Modern Tkinter GUI** - Interface yang bersih dan responsif
-  **Factory Pattern** - Implementasi Factory Method untuk inisialisasi tree
-  **Unit Testing** - Test suite untuk validasi fungsi

## Requirements

IP Address Finder memiliki beberapa requirement:

- Python 3.8+
- Tkinter

## Installation

1. Clone repository ini:

```bash
git clone https://github.com/delissesu/Hello-Wold-and-Other-Disasters.git
cd ip-address-finder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Basic Usage

Untuk menjalankan aplikasi:

```bash
python ip_address_finder.py
```

### Features

#### 1. Device Management
- Tambah device baru dengan IP address
- Hapus device yang ada
- Update data packet device

#### 2. Search & Visualization
- Cari device berdasarkan IP address
- Visualisasi struktur Splay Tree
- Daftar device terurut

#### 3. Simulasi
- Generate random devices untuk testing
- Monitoring operasi search
- Activity logging

## Code Structure

```
ip-address-finder/
 src/
    config/
       settings.py
    datastructures/
       nodes.py
       splay_tree.py
    factories/
       tree_factory.py
    gui/
        app.py
 ip_address_finder.py
 requirements.txt
 test_splay_tree.py
```

## Testing

Untuk menjalankan test suite:

```bash
python -m pytest test_splay_tree.py
```

## Contributing

Kontribusi selalu diterima dengan senang hati. Silahkan buat pull request untuk:

- Melaporkan bug
- Memperbaiki masalah
- Menambah fitur baru
- Memperbaiki dokumentasi

## Security

Jika kamu menemukan masalah keamanan dalam aplikasi ini, silakan kirim email ke [@naveriaworks@gmail.com].

## License

IP Address Finder adalah open-sourced software yang dilisensikan di bawah [MIT license](https://opensource.org/licenses/MIT).
