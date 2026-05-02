from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QDoubleSpinBox, QDateEdit, QHBoxLayout, QPushButton
)
from PySide6.QtCore import QDate

class FormTransaksiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Transaksi")
        self.setFixedSize(350, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Contoh: Bayar SPP")
        form_layout.addRow("Nama Transaksi:", self.input_nama)

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(["Pendidikan", "Konsumsi", "Transportasi", "Lainnya"])
        form_layout.addRow("Kategori:", self.combo_kategori)

        self.combo_tipe = QComboBox()
        self.combo_tipe.addItems(["Pengeluaran", "Pemasukan"])
        form_layout.addRow("Tipe:", self.combo_tipe)

        self.input_nominal = QDoubleSpinBox()
        self.input_nominal.setMaximum(999999999.99)
        self.input_nominal.setPrefix("Rp ")
        form_layout.addRow("Nominal:", self.input_nominal)

        self.input_tanggal = QDateEdit()
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setCalendarPopup(True)
        form_layout.addRow("Tanggal:", self.input_tanggal)

        btn_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("Simpan")
        self.btn_batal = QPushButton("Batal")
        
        self.btn_simpan.clicked.connect(self.accept)
        self.btn_batal.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_simpan)
        btn_layout.addWidget(self.btn_batal)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_data(self):
        return {
            "nama": self.input_nama.text(),
            "kategori": self.combo_kategori.currentText(),
            "tipe": self.combo_tipe.currentText(),
            "nominal": self.input_nominal.value(),
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd")
        }

    def set_data(self, nama, kategori, tipe, nominal, tanggal):
        self.setWindowTitle("Edit Transaksi")
        self.input_nama.setText(nama)
        self.combo_kategori.setCurrentText(kategori)
        self.combo_tipe.setCurrentText(tipe)
        self.input_nominal.setValue(float(nominal))
        self.input_tanggal.setDate(QDate.fromString(tanggal, "yyyy-MM-dd"))