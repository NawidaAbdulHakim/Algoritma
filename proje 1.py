from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QLineEdit

class Arac:
    def __init__(self, arac_id, model, arac_yili, fiyat, kiralama_durumu):
        self.arac_id = arac_id
        self.model = model
        self.arac_yili = arac_yili
        self.fiyat = fiyat
        self.kiralama_durumu = kiralama_durumu
    
    def arac_durumu_guncelle(self, durum):
        self.kiralama_durumu = durum

# 5 araç verisi ekle
arac1 = Arac(1, "Toyota Corolla", 2019, 25000, "Müsait")
arac2 = Arac(2, "Honda Civic", 2020, 30000, "Müsait")
arac3 = Arac(3, "Ford Focus", 2018, 20000, "Kiralandı")
arac4 = Arac(4, "Volkswagen Golf", 2017, 18000, "Müsait")
arac5 = Arac(5, "Renault Megane", 2019, 22000, "Kiralandı")

class Musteri:
    def __init__(self, adi, soyadi, telefon, kredi_kart_bilgileri):
        self.adi = adi
        self.soyadi = soyadi
        self.telefon = telefon
        self.kredi_kart_bilgileri = kredi_kart_bilgileri

# Kullanıcıdan müşteri bilgilerini al
adi = input("Adınız: ")
soyadi = input("Soyadınız: ")
telefon = input("Telefon Numaranız: ")
kredi_kart_bilgileri = input("Kredi Kartı Bilgileriniz: ")

musteri = Musteri(adi, soyadi, telefon, kredi_kart_bilgileri)

class Kiralama:
    def kiralama_yap(self, musteri, arac):
        if arac.kiralama_durumu == "Müsait":
            arac.arac_durumu_guncelle("Kiralandı")
            print(f"{musteri.adi} {musteri.soyadi}, {arac.model} aracını kiraladı.")
        else:
            print("Araba şu anda kiralanamaz.")
    
    def kiralama_iptal_et(self, arac):
        if arac.kiralama_durumu == "Kiralandı":
            arac.arac_durumu_guncelle("Müsait")
            print(f"{arac.model} aracının kiralama işlemi iptal edildi.")
        else:
            print("Araba zaten kiralanmamış.")
    
    def kiralama_bilgisi(self, arac):
        print(f"{arac.model} aracının kiralama durumu: {arac.kiralama_durumu}")

# Örnek kullanım
kiralama = Kiralama()

kiralama.kiralama_yap(musteri, arac1)
kiralama.kiralama_bilgisi(arac1)
kiralama.kiralama_iptal_et(arac1)
kiralama.kiralama_bilgisi(arac1)

# Araç sınıfı ve araç verileri burada tanımlanmış olarak varsayılmıştır

app = QApplication([])

window = QWidget()
window.setWindowTitle("Araç Kiralama Sistemi")

label_adi = QLabel("Adınız:")
input_adi = QLineEdit()

label_soyadi = QLabel("Soyadınız:")
input_soyadi = QLineEdit()

label_telefon = QLabel("Telefon Numaranız:")
input_telefon = QLineEdit()

label_kredi_kart = QLabel("Kredi Kartı Bilgileriniz:")
input_kredi_kart = QLineEdit()

label_arac_sec = QLabel("Araç Seçimi:")
combo_arac_sec = QComboBox()

button_kiralama_yap = QPushButton("Kiralama Yap")
button_kiralama_iptal_et = QPushButton("Kiralama İptal Et")

layout = QVBoxLayout()
layout.addWidget(label_adi)
layout.addWidget(input_adi)
layout.addWidget(label_soyadi)
layout.addWidget(input_soyadi)
layout.addWidget(label_telefon)
layout.addWidget(input_telefon)
layout.addWidget(label_kredi_kart)
layout.addWidget(input_kredi_kart)
layout.addWidget(label_arac_sec)
layout.addWidget(combo_arac_sec)
layout.addWidget(button_kiralama_yap)
layout.addWidget(button_kiralama_iptal_et)

window.setLayout(layout)

window.show()

app.exec_()


