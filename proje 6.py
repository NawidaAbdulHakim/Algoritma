import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QListWidget, QListWidgetItem

class TarifUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarif Uygulaması")
        self.arayuz_olustur()
        self.veritabani_baglantisi_olustur()

    def arayuz_olustur(self):
        self.duzen = QVBoxLayout()

        # Fancy Heading
        fancy_heading = QLabel("<h1 style='color: #808000; font-family: Arial, sans-serif;'>Tarif Uygulaması</h1>")
        self.duzen.addWidget(fancy_heading)

        # Tarif
        self.tarif_ad_label = QLabel("Tarif Adı:")
        self.tarif_ad_input = QLineEdit()
        self.duzen.addWidget(self.tarif_ad_label)
        self.duzen.addWidget(self.tarif_ad_input)

        self.malzemeler_label = QLabel("Malzemeler:")
        self.malzemeler_input = QTextEdit()
        self.duzen.addWidget(self.malzemeler_label)
        self.duzen.addWidget(self.malzemeler_input)

        self.tarif_label = QLabel("Tarif:")
        self.tarif_input = QTextEdit()
        self.duzen.addWidget(self.tarif_label)
        self.duzen.addWidget(self.tarif_input)

        self.tarif_ekle_button = QPushButton("Tarifi Ekle")
        self.tarif_ekle_button.setStyleSheet("background-color: green;")
        self.tarif_ekle_button.clicked.connect(self.tarif_ekle)
        self.duzen.addWidget(self.tarif_ekle_button)

        # Tarif Listesi
        self.tarif_listesi = QListWidget()
        self.tarif_listesi.itemClicked.connect(self.tarif_detaylari_goster)
        self.duzen.addWidget(self.tarif_listesi)

        # Tarif Sil Button
        self.tarif_sil_button = QPushButton("Seçili Tarifi Sil")
        self.tarif_sil_button.setStyleSheet("background-color: red;")
        self.tarif_sil_button.clicked.connect(self.tarif_sil)
        self.duzen.addWidget(self.tarif_sil_button)

        # Kullanıcı
        self.kullanici_ad_label = QLabel("Kullanıcı Adı:")
        self.kullanici_ad_input = QLineEdit()
        self.duzen.addWidget(self.kullanici_ad_label)
        self.duzen.addWidget(self.kullanici_ad_input)

        self.sifre_label = QLabel("Şifre:")
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.duzen.addWidget(self.sifre_label)
        self.duzen.addWidget(self.sifre_input)

        self.setLayout(self.duzen)

    def veritabani_baglantisi_olustur(self):
        self.veritabani_baglantisi = sqlite3.connect('tarifler.db')
        self.cursor = self.veritabani_baglantisi.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Tarifler
                                (tarif_id INTEGER PRIMARY KEY,
                                tarif_adi TEXT,
                                malzemeler TEXT,
                                tarif_metni TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Kullanicilar
                                (kullanici_id INTEGER PRIMARY KEY,
                                ad TEXT,
                                sifre TEXT)''')
        self.veritabani_baglantisi.commit()

        # Existing recipes fetch and display
        self.cursor.execute("SELECT tarif_adi FROM Tarifler")
        tarifler = self.cursor.fetchall()
        for tarif in tarifler:
            self.tarif_listesi.addItem(tarif[0])

    def tarif_ekle(self):
        tarif_ad = self.tarif_ad_input.text().strip()
        malzemeler = self.malzemeler_input.toPlainText().strip()
        tarif_icerik = self.tarif_input.toPlainText().strip()

        if tarif_ad and malzemeler and tarif_icerik:
            self.cursor.execute("INSERT INTO Tarifler (tarif_adi, malzemeler, tarif_metni) VALUES (?, ?, ?)",
                                (tarif_ad, malzemeler, tarif_icerik))
            self.veritabani_baglantisi.commit()
            QMessageBox.information(self, "Başarılı", "Tarif başarıyla eklendi!")
            self.tarif_listesi.addItem(tarif_ad)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")

    def tarif_detaylari_goster(self, item):
        tarif_adi = item.text()
        self.cursor.execute("SELECT malzemeler, tarif_metni FROM Tarifler WHERE tarif_adi = ?", (tarif_adi,))
        tarif_detaylari = self.cursor.fetchone()
        if tarif_detaylari:
            malzemeler, tarif_metni = tarif_detaylari
            self.malzemeler_input.setPlainText(malzemeler)
            self.tarif_input.setPlainText(tarif_metni)

    def tarif_sil(self):
        selected_items = self.tarif_listesi.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir tarif seçiniz.")
            return

        for item in selected_items:
            self.cursor.execute("DELETE FROM Tarifler WHERE tarif_adi = ?", (item.text(),))
            self.veritabani_baglantisi.commit()
            self.tarif_listesi.takeItem(self.tarif_listesi.row(item))

    def closeEvent(self, event):
        self.veritabani_baglantisi.close()
        event.accept()

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = TarifUygulamasi()
    pencere.show()
    sys.exit(uygulama.exec_())
