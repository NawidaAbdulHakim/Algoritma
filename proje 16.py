import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QDialog, QFormLayout, QGroupBox, QGridLayout, QTextEdit
import sqlite3

class FilmDiziIzlemeServisi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film ve Dizi İzleme Servisi")
        self.setGeometry(100, 100, 600, 300)

        self.baglanti_olustur()
        self.init_ui()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("film_dizi_veritabani.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS filmler (id INTEGER PRIMARY KEY, ad TEXT, yonetmen TEXT, tur TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, kullanici_adi TEXT, sifre TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS izleme_gecmisi (kullanici_id INTEGER, film_id INTEGER, FOREIGN KEY(kullanici_id) REFERENCES kullanicilar(id), FOREIGN KEY(film_id) REFERENCES filmler(id))")
        self.baglanti.commit()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Kullanıcı girişi
        self.giris_groupbox = QGroupBox("Kullanıcı Girişi")
        self.layout.addWidget(self.giris_groupbox)

        self.giris_layout = QGridLayout()
        self.giris_groupbox.setLayout(self.giris_layout)

        self.lbl_kullanici_adi = QLabel("Kullanıcı Adı:")
        self.txt_kullanici_adi = QLineEdit()
        self.lbl_sifre = QLabel("Şifre:")
        self.txt_sifre = QLineEdit()
        self.btn_giris = QPushButton("Giriş Yap")
        self.btn_giris.clicked.connect(self.giris_yap)

        self.giris_layout.addWidget(self.lbl_kullanici_adi, 0, 0)
        self.giris_layout.addWidget(self.txt_kullanici_adi, 0, 1)
        self.giris_layout.addWidget(self.lbl_sifre, 1, 0)
        self.giris_layout.addWidget(self.txt_sifre, 1, 1)
        self.giris_layout.addWidget(self.btn_giris, 2, 0, 1, 2)

        # Film listesi
        self.film_listesi_groupbox = QGroupBox("Film Listesi")
        self.layout.addWidget(self.film_listesi_groupbox)

        self.film_listesi_layout = QVBoxLayout()
        self.film_listesi_groupbox.setLayout(self.film_listesi_layout)

        self.liste_widget = QListWidget()
        self.film_listesi_layout.addWidget(self.liste_widget)

        # Film ekleme
        self.film_ekle_groupbox = QGroupBox("Film Ekle")
        self.layout.addWidget(self.film_ekle_groupbox)

        self.film_ekle_layout = QFormLayout()
        self.film_ekle_groupbox.setLayout(self.film_ekle_layout)

        self.txt_film_adi = QLineEdit()
        self.txt_yonetmen = QLineEdit()
        self.txt_tur = QLineEdit()
        self.btn_film_ekle = QPushButton("Film Ekle")
        self.btn_film_ekle.clicked.connect(self.film_ekle)

        self.film_ekle_layout.addRow("Film Adı:", self.txt_film_adi)
        self.film_ekle_layout.addRow("Yönetmen:", self.txt_yonetmen)
        self.film_ekle_layout.addRow("Tür:", self.txt_tur)
        self.film_ekle_layout.addRow(self.btn_film_ekle)

    def giris_yap(self):
        kullanici_adi = self.txt_kullanici_adi.text()
        sifre = self.txt_sifre.text()

        self.cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
        kullanici = self.cursor.fetchone()

        if kullanici:
            self.btn_giris.setEnabled(False)
            self.txt_kullanici_adi.setEnabled(False)
            self.txt_sifre.setEnabled(False)

            self.cursor.execute("SELECT ad, yonetmen, tur FROM filmler")
            filmler = self.cursor.fetchall()
            for film in filmler:
                self.liste_widget.addItem(f"{film[0]} - {film[1]} - {film[2]}")
        else:
            QMessageBox.warning(self, "Uyarı", "Kullanıcı adı veya şifre hatalı!")

    def film_ekle(self):
        film_adi = self.txt_film_adi.text()
        yonetmen = self.txt_yonetmen.text()
        tur = self.txt_tur.text()

        self.cursor.execute("INSERT INTO filmler (ad, yonetmen, tur) VALUES (?, ?, ?)", (film_adi, yonetmen, tur))
        self.baglanti.commit()
        QMessageBox.information(self, "Bilgi", "Film başarıyla eklendi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmDiziIzlemeServisi()
    window.show()
    sys.exit(app.exec_())
