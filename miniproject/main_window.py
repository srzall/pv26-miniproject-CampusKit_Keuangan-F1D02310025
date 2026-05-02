from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, 
    QMessageBox, QHeaderView, QFrame
)
from dialog_form import FormTransaksiDialog
import database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CampusKit - Keuangan Mahasiswa")
        self.resize(1000, 600)
        
        self.setup_ui()
        self.muat_data_tabel()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebarFrame")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        
        lbl_logo = QLabel("🎓 CampusKit\nKeuangan")
        lbl_logo.setObjectName("lblLogo")
        sidebar_layout.addWidget(lbl_logo)
        sidebar_layout.addSpacing(20)

        btn_dashboard = QPushButton("📊 Dashboard Transaksi")
        btn_dashboard.setObjectName("btnMenu")
        btn_bantuan = QPushButton("ℹ️ Tentang Aplikasi")
        btn_bantuan.setObjectName("btnMenu")
        btn_bantuan.clicked.connect(self.tampilkan_tentang)
        
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_bantuan)
        sidebar_layout.addStretch()

        lbl_identitas = QLabel("Samsul Rizal\nNIM: F1D02310025")
        lbl_identitas.setObjectName("lblIdentitasSidebar")
        sidebar_layout.addWidget(lbl_identitas)

        konten_frame = QFrame()
        konten_frame.setObjectName("kontenFrame")
        konten_layout = QVBoxLayout(konten_frame)
        konten_layout.setContentsMargins(20, 20, 20, 20)
        konten_layout.setSpacing(15)

        layout_saldo = QHBoxLayout()
        self.card_pemasukan = self.buat_kartu_saldo("Total Pemasukan", "Rp 0", "#27ae60")
        self.card_pengeluaran = self.buat_kartu_saldo("Total Pengeluaran", "Rp 0", "#e74c3c")
        self.card_total = self.buat_kartu_saldo("Sisa Saldo", "Rp 0", "#2980b9")
        
        layout_saldo.addWidget(self.card_pemasukan)
        layout_saldo.addWidget(self.card_pengeluaran)
        layout_saldo.addWidget(self.card_total)
        konten_layout.addLayout(layout_saldo)

        layout_header = QHBoxLayout()
        lbl_judul_tabel = QLabel("Riwayat Transaksi")
        lbl_judul_tabel.setObjectName("judulTabel")
        
        self.btn_tambah = QPushButton("➕ Tambah Transaksi")
        self.btn_tambah.clicked.connect(self.buka_dialog_tambah)
        
        layout_header.addWidget(lbl_judul_tabel)
        layout_header.addStretch()
        layout_header.addWidget(self.btn_tambah)
        konten_layout.addLayout(layout_header)

        self.tabel = QTableWidget()
        self.tabel.setColumnCount(7) 
        self.tabel.setHorizontalHeaderLabels(["ID", "Tanggal", "Nama Transaksi", "Kategori", "Tipe", "Nominal (Rp)", "Aksi"])
        
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) 
        
        self.tabel.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabel.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabel.setColumnHidden(0, True) 
        konten_layout.addWidget(self.tabel)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(konten_frame)
        central_widget.setLayout(main_layout)

    def buat_kartu_saldo(self, judul, nilai, warna):
        kartu = QFrame()
        kartu.setObjectName("kartuSaldo")
        kartu.setStyleSheet(f"background-color: {warna}; border-radius: 8px;")
        layout = QVBoxLayout(kartu)
        lbl_judul = QLabel(judul)
        lbl_judul.setStyleSheet("color: #ecf0f1; font-weight: bold; border: none; background: transparent;")
        lbl_nilai = QLabel(nilai)
        lbl_nilai.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none; background: transparent;")
        kartu.lbl_nilai = lbl_nilai 
        layout.addWidget(lbl_judul)
        layout.addWidget(lbl_nilai)
        
        return kartu

    def update_ringkasan_saldo(self):
        pemasukan, pengeluaran, saldo = database.hitung_saldo()
        self.card_pemasukan.lbl_nilai.setText(f"Rp {pemasukan:,.0f}")
        self.card_pengeluaran.lbl_nilai.setText(f"Rp {pengeluaran:,.0f}")
        self.card_total.lbl_nilai.setText(f"Rp {saldo:,.0f}")

    def muat_data_tabel(self):
        data = database.ambil_semua_transaksi()
        self.tabel.setRowCount(len(data))
        
        for baris_idx, baris_data in enumerate(data):
            self.tabel.setItem(baris_idx, 0, QTableWidgetItem(str(baris_data[0])))
            self.tabel.setItem(baris_idx, 1, QTableWidgetItem(baris_data[5]))
            self.tabel.setItem(baris_idx, 2, QTableWidgetItem(baris_data[1]))
            self.tabel.setItem(baris_idx, 3, QTableWidgetItem(baris_data[2]))
            self.tabel.setItem(baris_idx, 4, QTableWidgetItem(baris_data[3]))
            self.tabel.setItem(baris_idx, 5, QTableWidgetItem(f"{baris_data[4]:,.0f}"))

            widget_aksi = QWidget()
            layout_aksi = QHBoxLayout(widget_aksi)
            layout_aksi.setContentsMargins(5, 2, 5, 2)
            layout_aksi.setSpacing(5)

            btn_edit = QPushButton("✏ Edit")
            btn_edit.setObjectName("btnAksiEdit")
            btn_edit.clicked.connect(lambda checked=False, data_baris=baris_data: self.edit_transaksi(data_baris))

            btn_hapus = QPushButton("🗑 Hapus")
            btn_hapus.setObjectName("btnAksiHapus")
            btn_hapus.clicked.connect(lambda checked=False, id_tx=baris_data[0]: self.hapus_transaksi(id_tx))

            layout_aksi.addWidget(btn_edit)
            layout_aksi.addWidget(btn_hapus)
            self.tabel.setCellWidget(baris_idx, 6, widget_aksi)
            
        self.update_ringkasan_saldo()

    def buka_dialog_tambah(self):
        dialog = FormTransaksiDialog(self)
        if dialog.exec():
            konfirmasi = QMessageBox.question(
                self, "Konfirmasi", "Simpan data transaksi ini?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if konfirmasi == QMessageBox.StandardButton.Yes:
                data = dialog.get_data()
                database.tambah_transaksi(
                    data["nama"], data["kategori"], data["tipe"], 
                    data["nominal"], data["tanggal"]
                )
                self.muat_data_tabel()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")

    def edit_transaksi(self, data_baris):
        id_transaksi, nama, kategori, tipe, nominal, tanggal = data_baris
        
        dialog = FormTransaksiDialog(self)
        dialog.set_data(nama, kategori, tipe, nominal, tanggal)
        
        if dialog.exec():
            data = dialog.get_data()
            database.update_transaksi(
                id_transaksi, data["nama"], data["kategori"], 
                data["tipe"], data["nominal"], data["tanggal"]
            )
            self.muat_data_tabel()
            QMessageBox.information(self, "Sukses", "Data berhasil diubah!")

    def hapus_transaksi(self, id_transaksi):
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if konfirmasi == QMessageBox.StandardButton.Yes:
            database.hapus_transaksi(id_transaksi)
            self.muat_data_tabel()
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")

    def tampilkan_tentang(self):
        pesan = "Aplikasi Pencatat Keuangan\n\nDikembangkan oleh:\nNama: Samsul Rizal\nNIM: F1D02310025"
        QMessageBox.information(self, "Tentang Aplikasi", pesan)