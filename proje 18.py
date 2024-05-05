import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QComboBox
import sqlite3

class HistoryDatabase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarihçi - Tarihi Olaylar Veritabanı")
        self.setGeometry(100, 100, 500, 300)

        self.create_connection()
        self.init_ui()

    def create_connection(self):
        self.connection = sqlite3.connect("history_database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, name TEXT, date TEXT, description TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS figures (id INTEGER PRIMARY KEY, name TEXT, periods TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS periods (id INTEGER PRIMARY KEY, name TEXT, start_date TEXT, end_date TEXT)")
        self.connection.commit()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.v_box = QVBoxLayout()
        self.central_widget.setLayout(self.v_box)

        self.lbl_event_name = QLabel("Olay Adı:")
        self.txt_event_name = QLineEdit()
        self.lbl_event_date = QLabel("Olay Tarihi:")
        self.txt_event_date = QLineEdit()
        self.lbl_event_description = QLabel("Olay Açıklaması:")
        self.txt_event_description = QLineEdit()
        self.btn_add_event = QPushButton("Olay Ekle")
        self.btn_add_event.clicked.connect(self.add_event)

        self.v_box.addWidget(self.lbl_event_name)
        self.v_box.addWidget(self.txt_event_name)
        self.v_box.addWidget(self.lbl_event_date)
        self.v_box.addWidget(self.txt_event_date)
        self.v_box.addWidget(self.lbl_event_description)
        self.v_box.addWidget(self.txt_event_description)
        self.v_box.addWidget(self.btn_add_event)

        self.lbl_figure_name = QLabel("Şahsiyet Adı:")
        self.txt_figure_name = QLineEdit()
        self.lbl_figure_periods = QLabel("Şahsiyetin Yaşadığı Dönemler:")
        self.txt_figure_periods = QLineEdit()
        self.btn_add_figure = QPushButton("Şahsiyet Ekle")
        self.btn_add_figure.clicked.connect(self.add_figure)

        self.v_box.addWidget(self.lbl_figure_name)
        self.v_box.addWidget(self.txt_figure_name)
        self.v_box.addWidget(self.lbl_figure_periods)
        self.v_box.addWidget(self.txt_figure_periods)
        self.v_box.addWidget(self.btn_add_figure)

        self.lbl_period_name = QLabel("Dönem Adı:")
        self.txt_period_name = QLineEdit()
        self.lbl_period_start_date = QLabel("Başlangıç Tarihi:")
        self.txt_period_start_date = QLineEdit()
        self.lbl_period_end_date = QLabel("Bitiş Tarihi:")
        self.txt_period_end_date = QLineEdit()
        self.btn_add_period = QPushButton("Dönem Ekle")
        self.btn_add_period.clicked.connect(self.add_period)

        self.v_box.addWidget(self.lbl_period_name)
        self.v_box.addWidget(self.txt_period_name)
        self.v_box.addWidget(self.lbl_period_start_date)
        self.v_box.addWidget(self.txt_period_start_date)
        self.v_box.addWidget(self.lbl_period_end_date)
        self.v_box.addWidget(self.txt_period_end_date)
        self.v_box.addWidget(self.btn_add_period)

        self.list_widget = QListWidget()
        self.v_box.addWidget(self.list_widget)

    def add_event(self):
        event_name = self.txt_event_name.text()
        event_date = self.txt_event_date.text()
        event_description = self.txt_event_description.text()

        self.cursor.execute("INSERT INTO events (name, date, description) VALUES (?, ?, ?)", (event_name, event_date, event_description))
        self.connection.commit()
        self.txt_event_name.clear()
        self.txt_event_date.clear()
        self.txt_event_description.clear()

        self.list_widget.addItem(event_name)

    def add_figure(self):
        figure_name = self.txt_figure_name.text()
        figure_periods = self.txt_figure_periods.text()

        self.cursor.execute("INSERT INTO figures (name, periods) VALUES (?, ?)", (figure_name, figure_periods))
        self.connection.commit()
        self.txt_figure_name.clear()
        self.txt_figure_periods.clear()

        self.list_widget.addItem(figure_name)

    def add_period(self):
        period_name = self.txt_period_name.text()
        period_start_date = self.txt_period_start_date.text()
        period_end_date = self.txt_period_end_date.text()

        self.cursor.execute("INSERT INTO periods (name, start_date, end_date) VALUES (?, ?, ?)", (period_name, period_start_date, period_end_date))
        self.connection.commit()
        self.txt_period_name.clear()
        self.txt_period_start_date.clear()
        self.txt_period_end_date.clear()

        self.list_widget.addItem(period_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistoryDatabase()
    window.show()
    sys.exit(app.exec())
