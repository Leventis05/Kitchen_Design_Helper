from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QLineEdit, QMessageBox
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt

def add_row():
    row = model.rowCount()
    model.insertRow(row)

def on_text_changed(text):
    proxy.setFilterWildcard(text)

def delete_row():
    reply = QMessageBox.question(
        None,
        "Delete",
        "Are you sure?",
        QMessageBox.Yes | QMessageBox.No
    )
    p_index = view.currentIndex()
    s_index = proxy.mapToSource(p_index)
    if s_index.isValid():
        model.removeRow(s_index.row())
        model.submitAll()
        model.select()

class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("dd-MM-yyyy")
        editor.setDate(QDate.currentDate())
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

    proxy = QSortFilterProxyModel()
    proxy.setSourceModel(model)
    proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
    proxy.setFilterKeyColumn(1)  # column to search (e.g. name)

    date_delegate = DateDelegate()

    view = QTableView()
    view.setModel(proxy)
    view.horizontalHeader().setStretchLastSection(True)
    view.setColumnHidden(0, True)
    view.setItemDelegateForColumn(3, date_delegate)
    view.setItemDelegateForColumn(4, date_delegate)

    search = QLineEdit()
    search.setPlaceholderText("Search...")

    search.textChanged.connect(on_text_changed)

    add_tuple_btn = QPushButton("Add Row")

    dltRowButton = QPushButton("Delete Row")

    add_tuple_btn.clicked.connect(add_row)
    dltRowButton.clicked.connect(delete_row)

    layout.addWidget(search)
    layout.addWidget(view)
    layout.addWidget(add_tuple_btn)
    layout.addWidget(dltRowButton)


    window.setLayout(layout)
    window.resize(1000, 700)
    window.show()
    app.exec_()




