# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTableView, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QLineEdit, QMessageBox, QTabWidget
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt

def add_row():
    row = all_model.rowCount()
    all_model.insertRow(row)

def on_text_changed(text):
    proxy.setFilterWildcard(text)

def delete_row():
    reply = QMessageBox.question(
        None,
        "Delete",
        "Are you sure?",
        QMessageBox.Yes | QMessageBox.No
    )
    p_index = all_view.currentIndex()
    s_index = proxy.mapToSource(p_index)
    if s_index.isValid():
        all_model.removeRow(s_index.row())
        all_model.submitAll()
        all_model.select()

def refresh_reminders():
    reminder_model.setFilter(f"deadline BETWEEN '{start}' AND '{end}'")
    reminder_model.select()
    update_badge()

def resize_all():
    all_view.resizeColumnsToContents()

def resize_rem():
    reminder_view.resizeColumnsToContents()

def update_badge():
    count = reminder_model.rowCount()
    tabs.setTabText(1, f"Reminders ({count})")

class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("dd-MM-yyyy")
        editor.setDate(QDate.currentDate())
        return editor

    def setEditorData(self, editor, index):
        date_str = index.model().data(index)
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        editor.setDate(date)

    def setModelData(self, editor, all_model, index):
        date = editor.date().toString("dd-MM-yyyy")
        all_model.setData(index, date)


# MAIN

if __name__ == "__main__":

    app = QApplication([])
    
    tabs = QTabWidget()

    db = QSqlDatabase.addDatabase("QSQLITE")
    
    all_model = QSqlTableModel()
    all_view = QTableView()
    all_tab = QWidget()
    all_layout = QVBoxLayout()
    proxy = QSortFilterProxyModel()
    date_delegate = DateDelegate()

    reminder_model = QSqlTableModel()
    reminder_view = QTableView()
    reminder_tab = QWidget()


    # Connect to SQLite
    db.setConnectOptions("QSQLITE_ENABLE_SHARED_CACHE=1")
    db.setDatabaseName("test.db")
    db.open()

    #ALL TUPLES TAB
    all_model.setTable("kitchens")   # table name
    all_model.select()            # load data
    all_model.setEditStrategy(QSqlTableModel.OnFieldChange)
    all_model.setHeaderData(1, Qt.Horizontal, "Πελάτης")
    all_model.setHeaderData(2, Qt.Horizontal, "Σχεδιαστής")
    all_model.setHeaderData(3, Qt.Horizontal, "Ημ/νία Αποδοχής")
    all_model.setHeaderData(4, Qt.Horizontal, "Ημ/νία Παράδωσης")
    all_model.setHeaderData(5, Qt.Horizontal, "Εκκρεμότητες")

    proxy.setSourceModel(all_model)
    proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
    proxy.setFilterKeyColumn(1)  # column to search (e.g. name)


    all_view.setModel(proxy)
    all_view.resizeColumnsToContents()
    all_view.horizontalHeader().setStretchLastSection(True)
    all_view.setColumnHidden(0, True)
    all_view.setItemDelegateForColumn(3, date_delegate)
    all_view.setItemDelegateForColumn(4, date_delegate)

    #BUTTONS AND SEARCHBAR
    search = QLineEdit()
    search.setPlaceholderText("Search...")

    search.textChanged.connect(on_text_changed)

    add_tuple_btn = QPushButton("Add Row")

    dltRowButton = QPushButton("Delete Row")

    add_tuple_btn.clicked.connect(add_row)
    dltRowButton.clicked.connect(delete_row)
    
    #CREATE TAB
    
    all_layout.addWidget(all_view)

    all_layout.addWidget(search)
    all_layout.addWidget(add_tuple_btn)
    all_layout.addWidget(dltRowButton)

    all_tab.setLayout(all_layout)


    #REMINDER TAB
    today = QDate.currentDate()
    two_days_later = today.addDays(2)

    start = today.toString("yyyy-MM-dd")
    end = two_days_later.toString("yyyy-MM-dd")

    reminder_model.setTable("kitchens")
    refresh_reminders()
    reminder_model.setHeaderData(1, Qt.Horizontal, "Πελάτης")
    reminder_model.setHeaderData(2, Qt.Horizontal, "Σχεδιαστής")
    reminder_model.setHeaderData(3, Qt.Horizontal, "Ημ/νία Αποδοχής")
    reminder_model.setHeaderData(4, Qt.Horizontal, "Ημ/νία Παράδωσης")
    reminder_model.setHeaderData(5, Qt.Horizontal, "Εκκρεμότητες")

    reminder_view.setModel(reminder_model)
    reminder_view.resizeColumnsToContents()
    reminder_view.setColumnHidden(0, True)
    reminder_view.horizontalHeader().setStretchLastSection(True)

    reminder_layout = QVBoxLayout()
    reminder_layout.addWidget(reminder_view)
    reminder_tab.setLayout(reminder_layout)


    #INIT TABS

    tabs.addTab(all_tab, "All Works")
    tabs.currentChanged.connect(lambda i: resize_all() if i == 1 else None)

    tabs.addTab(reminder_tab, "Reminders")
    update_badge()
    tabs.currentChanged.connect(lambda i: refresh_reminders() if i == 1 else None)
    tabs.currentChanged.connect(lambda i: resize_rem() if i == 1 else None)

    tabs.resize(1000, 700)
    tabs.show()

    app.exec_()




