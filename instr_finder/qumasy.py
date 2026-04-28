import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QLabel
)

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

class InsertApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DB Insert Tool")

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")

        self.city = QLineEdit()
        self.city.setPlaceholderText("City")

        self.btn = QPushButton("Insert")
        self.btn.clicked.connect(self.insert_data)

        self.status = QLabel("")

        layout.addWidget(self.name)
        layout.addWidget(self.age)
        layout.addWidget(self.city)
        layout.addWidget(self.btn)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def insert_data(self):
        name = self.name.text()
        age = self.age.text()
        city = self.city.text()

        cursor.execute(
            "INSERT INTO people (name, age, city) VALUES (?, ?, ?)",
            (name, age, city)
        )
        conn.commit()

        self.status.setText("Inserted successfully!")

        self.name.clear()
        self.age.clear()
        self.city.clear()


app = QApplication(sys.argv)
window = InsertApp()
window.show()
sys.exit(app.exec_())