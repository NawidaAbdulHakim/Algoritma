import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class StokTakipSistemi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok Takip Sistemi")  # Set background color to green
        self.arayuz_olustur()
        self.veritabani_baglantisi_olustur()
        self.urunleri_yukle()

    def arayuz_olustur(self):
        self.duzen = QVBoxLayout()

        # Title
        self.baslik_label = QLabel("Stok Takip Sistemi")
        self.baslik_label.setAlignment(Qt.AlignCenter)
        self.baslik_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.duzen.addWidget(self.baslik_label)

        # Product (Ürün) Section
        self.urun_label = QLabel("Ürün Adı:")
        self.urun_input = QLineEdit()
        self.duzen.addWidget(self.urun_label)
        self.duzen.addWidget(self.urun_input)

        self.stok_label = QLabel("Stok Miktarı:")
        self.stok_input = QLineEdit()
        self.duzen.addWidget(self.stok_label)
        self.duzen.addWidget(self.stok_input)

        self.urun_ekle_button = QPushButton("Ürün Ekle")
        self.urun_ekle_button.setStyleSheet("background-color: #E9967A;")
        self.urun_ekle_button.clicked.connect(self.urun_ekle)
        self.duzen.addWidget(self.urun_ekle_button)

        # Product List
        self.urun_listesi_label = QLabel("Ürün Listesi:")
        self.urun_listesi = QListWidget()
        self.urun_listesi.itemClicked.connect(self.urun_secildi)
        self.duzen.addWidget(self.urun_listesi_label)
        self.duzen.addWidget(self.urun_listesi)

        # Delete Product Button
        self.urun_sil_button = QPushButton("Ürün Sil")
        self.urun_sil_button.setStyleSheet("background-color: #DC143C;")
        self.urun_sil_button.clicked.connect(self.urun_sil)
        self.duzen.addWidget(self.urun_sil_button)

        # Purchase Section
        self.satin_al_label = QLabel("Satın Al:")
        self.satin_al_input = QLineEdit()
        self.duzen.addWidget(self.satin_al_label)
        self.duzen.addWidget(self.satin_al_input)

        self.satin_al_button = QPushButton("Satın Al")
        self.satin_al_button.setStyleSheet("background-color: #483D8B;")
        self.satin_al_button.clicked.connect(self.satin_al)
        self.duzen.addWidget(self.satin_al_button)

        self.setLayout(self.duzen)

    def veritabani_baglantisi_olustur(self):
        self.veritabani_baglantisi = sqlite3.connect('stok_takip.db')
        self.cursor = self.veritabani_baglantisi.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Urunler
                                (id INTEGER PRIMARY KEY,
                                ad TEXT,
                                stok INTEGER)''')

        self.veritabani_baglantisi.commit()

    def urun_ekle(self):
        urun_adi = self.urun_input.text().strip()
        stok_miktari = int(self.stok_input.text().strip()) if self.stok_input.text().strip().isdigit() else 0

        if urun_adi and stok_miktari >= 0:
            self.cursor.execute("INSERT INTO Urunler (ad, stok) VALUES (?, ?)", (urun_adi, stok_miktari))
            self.veritabani_baglantisi.commit()
            self.urunleri_yukle()
            QMessageBox.information(self, "Başarılı", "Ürün başarıyla eklendi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir stok miktarı girin.")

    def urunleri_yukle(self):
        self.urun_listesi.clear()
        self.cursor.execute("SELECT ad, stok FROM Urunler")
        urunler = self.cursor.fetchall()
        for urun in urunler:
            item_text = f"{urun[0]} - Stok: {urun[1]}"
            item = QListWidgetItem(item_text)
            item.urun_adi = urun[0]
            self.urun_listesi.addItem(item)

    def urun_secildi(self, item):
        urun_adi = item.urun_adi
        self.cursor.execute("SELECT stok FROM Urunler WHERE ad = ?", (urun_adi,))
        stok_miktari = self.cursor.fetchone()[0]
        QMessageBox.information(self, "Stok Durumu", f"{urun_adi} ürününün stok miktarı: {stok_miktari}")

    def satin_al(self):
        satin_al_input = self.satin_al_input.text().strip()
        if " " in satin_al_input:
            urun_adi, miktar = satin_al_input.split(" ", 1)
            satin_alinan_miktar = int(miktar) if miktar.isdigit() else 0
        else:
            urun_adi = satin_al_input
            satin_alinan_miktar = 1

        if urun_adi and satin_alinan_miktar > 0:
            self.cursor.execute("SELECT stok FROM Urunler WHERE ad = ?", (urun_adi,))
            stok_miktari = self.cursor.fetchone()
            if stok_miktari is not None:
                stok_miktari = stok_miktari[0]
                if stok_miktari >= satin_alinan_miktar:
                    yeni_stok = stok_miktari - satin_alinan_miktar
                    self.cursor.execute("UPDATE Urunler SET stok = ? WHERE ad = ?", (yeni_stok, urun_adi))
                    self.veritabani_baglantisi.commit()
                    QMessageBox.information(self, "Başarılı", f"{urun_adi} ürününden {satin_alinan_miktar} adet satın alındı.")
                    self.urunleri_yukle()
                else:
                    QMessageBox.warning(self, "Uyarı", "Stokta yeterli ürün yok!")
            else:
                QMessageBox.warning(self, "Uyarı", "Geçersiz ürün adı!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir ürün adı ve miktarı girin.")

    def urun_sil(self):
        selected_items = self.urun_listesi.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz bir ürünü seçin.")
            return
        for item in selected_items:
            urun_adi = item.urun_adi
            self.cursor.execute("DELETE FROM Urunler WHERE ad = ?", (urun_adi,))
            self.veritabani_baglantisi.commit()
        self.urunleri_yukle()

    def closeEvent(self, event):
        self.veritabani_baglantisi.close()
        event.accept()

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = StokTakipSistemi()
    pencere.show()
    sys.exit(uygulama.exec_())
