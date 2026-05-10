from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMainWindow
)

import sys

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Setup Wizard")

        layout = QVBoxLayout()

        self.label = QLabel("Εισάγετε το όνομα τις βάσης")
        self.input = QLineEdit()

        self.ok_button = QPushButton("Συνέχεια")
        self.cancel_button = QPushButton("Ακύρωση")

        # connect buttons
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_db_name(self):
        return self.input.text()

