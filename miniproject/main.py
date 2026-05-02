import sys
import os
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
import database

def muat_qss(app, file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Peringatan: File {file_path} tidak ditemukan!")

if __name__ == "__main__":
    database.init_db()
    
    app = QApplication(sys.argv)
    
    muat_qss(app, "style.qss")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())