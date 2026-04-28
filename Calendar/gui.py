from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit
from PyQt5.QtCore import QDate

def add_row():
    row = model.rowCount()
    model.insertRow(row)
    today = QDate.currentDate().toString("dd-MM-yyyy")
    model.setData(model.index(row, 3), today)


class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("dd-MM-yyyy")
        return editor

    def setEditorData(self, editor, index):
        date_str = index.model().data(index)
        date = QDate.fromString(date_str, "dd-MM-yyyy")
        editor.setDate(date)

    def setModelData(self, editor, model, index):
        date = editor.date().toString("dd-MM-yyyy")
        model.setData(index, date)




# MAIN

if __name__ == "__main__":

    app = QApplication([])
    layout = QVBoxLayout()
    window = QWidget()

    # Connect to SQLite
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("test.db")
    db.open()

    model = QSqlTableModel()
    model.setTable("users")   # table name
    model.select()            # load data
    model.setEditStrategy(QSqlTableModel.OnFieldChange)

    view = QTableView()
    view.setModel(model)
    view.horizontalHeader().setStretchLastSection(True)
    view.setItemDelegateForColumn(3, DateDelegate())

    add_tuple_btn = QPushButton("Add Row")

    add_tuple_btn.clicked.connect(add_row)

    layout.addWidget(view)
    layout.addWidget(add_tuple_btn)


    window.setLayout(layout)
    window.resize(800, 500)
    window.show()
    app.exec_()




