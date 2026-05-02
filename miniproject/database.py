import sqlite3

DB_NAME = "keuangan.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            kategori TEXT,
            tipe TEXT,
            nominal REAL,
            tanggal TEXT
        )
    ''')
    conn.commit()
    conn.close()

def tambah_transaksi(nama, kategori, tipe, nominal, tanggal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transaksi (nama, kategori, tipe, nominal, tanggal)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, kategori, tipe, nominal, tanggal))
    conn.commit()
    conn.close()

def ambil_semua_transaksi():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transaksi ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def hapus_transaksi(id_transaksi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transaksi WHERE id = ?', (id_transaksi,))
    conn.commit()
    conn.close()

def update_transaksi(id_transaksi, nama, kategori, tipe, nominal, tanggal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transaksi
        SET nama=?, kategori=?, tipe=?, nominal=?, tanggal=?
        WHERE id=?
    ''', (nama, kategori, tipe, nominal, tanggal, id_transaksi))
    conn.commit()
    conn.close()

def hitung_saldo():
    """Menghitung total pemasukan, pengeluaran, dan sisa saldo."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tipe, SUM(nominal) FROM transaksi GROUP BY tipe")
    data = cursor.fetchall()
    conn.close()

    pemasukan = 0.0
    pengeluaran = 0.0
    
    for baris in data:
        if baris[0] == "Pemasukan":
            pemasukan = baris[1]
        elif baris[0] == "Pengeluaran":
            pengeluaran = baris[1]
            
    saldo_akhir = pemasukan - pengeluaran
    return pemasukan, pengeluaran, saldo_akhir