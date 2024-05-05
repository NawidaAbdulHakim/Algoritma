import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QDialog, QFormLayout, QComboBox
import sqlite3

class EducationMaterialPlatform(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Egitim Materyali Paylasim Platformu")
        self.setGeometry(100, 100, 600, 400)

        self.baglanti_olustur()
        self.init_ui()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("egitim_materyali_veritabani.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS dersler (id INTEGER PRIMARY KEY, ad TEXT, ogretmen TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS materyaller (id INTEGER PRIMARY KEY, ders_id INTEGER, ad TEXT, tur TEXT, icerik TEXT, FOREIGN KEY(ders_id) REFERENCES dersler(id))")
        self.baglanti.commit()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.v_box = QVBoxLayout()
        self.central_widget.setLayout(self.v_box)

        self.lbl_ders_adi = QLabel("Ders Adi:")
        self.txt_ders_adi = QLineEdit()
        self.lbl_ogretmen = QLabel("Ogretmen:")
        self.cmb_ogretmen = QComboBox()
        self.cmb_ogretmen.addItems(["Öğr.Ahmet Kara", "Öğr.Zeynep Arslan", "Öğr.Tarik Burak", "Öğr.Melissa Koç"])
        self.btn_ders_olustur = QPushButton("Ders Olustur")
        self.btn_ders_olustur.clicked.connect(self.ders_olustur)

        self.v_box.addWidget(self.lbl_ders_adi)
        self.v_box.addWidget(self.txt_ders_adi)
        self.v_box.addWidget(self.lbl_ogretmen)
        self.v_box.addWidget(self.cmb_ogretmen)
        self.v_box.addWidget(self.btn_ders_olustur)

        self.lbl_ogrenci_bilgileri = QLabel("Öğrenci Bilgileri:")
        self.txt_ogrenci_bilgileri = QLineEdit()
        self.v_box.addWidget(self.lbl_ogrenci_bilgileri)
        self.v_box.addWidget(self.txt_ogrenci_bilgileri)

        self.lbl_materyal_adi = QLabel("Materyal Adı:")
        self.txt_materyal_adi = QLineEdit()
        self.lbl_materyal_turu = QLabel("Materyal Türü:")
        self.txt_materyal_turu = QLineEdit()
        self.lbl_materyal_icerik = QLabel("Materyal İçeriği:")
        self.txt_materyal_icerik = QLineEdit()
        self.btn_materyal_ekle = QPushButton("Materyal Ekle")
        self.btn_materyal_ekle.clicked.connect(self.materyal_ekle)

        self.v_box.addWidget(self.lbl_materyal_adi)
        self.v_box.addWidget(self.txt_materyal_adi)
        self.v_box.addWidget(self.lbl_materyal_turu)
        self.v_box.addWidget(self.txt_materyal_turu)
        self.v_box.addWidget(self.lbl_materyal_icerik)
        self.v_box.addWidget(self.txt_materyal_icerik)
        self.v_box.addWidget(self.btn_materyal_ekle)

        self.liste_widget = QListWidget()
        self.v_box.addWidget(self.liste_widget)

    def ders_olustur(self):
        ders_adi = self.txt_ders_adi.text()
        ogretmen = self.cmb_ogretmen.currentText()

        self.cursor.execute("INSERT INTO dersler (ad, ogretmen) VALUES (?, ?)", (ders_adi, ogretmen))
        self.baglanti.commit()
        self.txt_ders_adi.clear()

        self.liste_widget.addItem(ders_adi)

    def materyal_ekle(self):
        materyal_adi = self.txt_materyal_adi.text()
        materyal_turu = self.txt_materyal_turu.text()
        materyal_icerik = self.txt_materyal_icerik.text()

        self.cursor.execute("INSERT INTO materyaller (ad, tur, icerik) VALUES (?, ?, ?)", (materyal_adi, materyal_turu, materyal_icerik))
        self.baglanti.commit()
        self.txt_materyal_adi.clear()
        self.txt_materyal_turu.clear()
        self.txt_materyal_icerik.clear()

        self.liste_widget.addItem(materyal_adi)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EducationMaterialPlatform()
    window.show()
    sys.exit(app.exec())
