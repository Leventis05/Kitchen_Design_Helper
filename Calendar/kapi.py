from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QComboBox
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from enum import Enum

DB_FORMAT = "yyyy-MM-dd"
UI_FORMAT = "dd-MM-yyyy"

DB_T = "QSQLITE"
DB_OPTIONS = "QSQLITE_ENABLE_SHARED_CACHE=1"
DB_NAME = "test.db"
DB_MAIN_TABLE = "kitchens"

# DON'T CHANGE NAMES change only numbers
class columns(Enum):
    ID              = 0
    CLIENT          = 1
    DESIGNER        = 2
    ANALYSIS_DATE   = 3
    CERT_DATE       = 4
    PENDING_ITEMS   = 5
    STATUS          = 6


DB_TABLE_COL = {
    columns.ID              : "id",
    columns.CLIENT          : "client",
    columns.DESIGNER        : "designer",
    columns.ANALYSIS_DATE   : "analysis_date",
    columns.CERT_DATE       : "certification_date",
    columns.PENDING_ITEMS   : "pending",
    columns.STATUS          : "checklist"
}

DB_COL_LABELS = {
    columns.ID              :"",
    columns.CLIENT          :"Πελάτης",
    columns.DESIGNER        :"Σχεδιαστής",
    columns.ANALYSIS_DATE   :"Ημ/νία Αποστολής Ανάλυσης",
    columns.CERT_DATE       :"Ημ/νία Έγκρισης",
    columns.PENDING_ITEMS   :"Εκκρεμότητες",
    columns.STATUS          :"Status"
}


class database:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase(DB_T)
        self.db.setConnectOptions(DB_OPTIONS)
        self.db.setDatabaseName(DB_NAME)
        self.db.open()


# I use this for dates
class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat(UI_FORMAT)
        editor.setDate(QDate.currentDate())
        return editor

    def setEditorData(self, editor, index):
        date_str = index.model().data(index)
        date = QDate.fromString(date_str, DB_FORMAT)
        editor.setDate(date)

    def setModelData(self, editor, all_model, index):
        date = editor.date().toString(DB_FORMAT)
        all_model.setData(index, date)


class PendingDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)

        # Add choices
        editor.addItems([
            "a",
            "b",
            "c",
            "a, b",
            "a, c",
            "b, c",
            "a, b, c"
        ])

        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index)

        idx = editor.findText(value)

        if idx >= 0:
            editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value)