from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QComboBox
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from enum import Enum

DB_FORMAT = "yyyy-MM-dd"
UI_FORMAT = "dd-MM-yyyy"

DB_T = "QSQLITE"
DB_OPTIONS = "QSQLITE_ENABLE_SHARED_CACHE=1"
DB_NAME = "test.db"
DB_MAIN_TABLE = "kitchens"

pending_s = ["υλικά", "πάγκος", "συσκευές"]

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
    columns.PENDING_ITEMS   : "pending"
}

DB_COL_LABELS = {
    columns.ID              :"",
    columns.CLIENT          :"Πελάτης",
    columns.DESIGNER        :"Σχεδιαστής",
    columns.ANALYSIS_DATE   :"Ημ/νία Αποστολής Ανάλυσης",
    columns.CERT_DATE       :"Ημ/νία Έγκρισης",
    columns.PENDING_ITEMS   :"Εκκρεμότητες"
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


# class CheckableComboBox(QComboBox):

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.setModel(QStandardItemModel(self))

#         # Editable so we can control displayed text
#         self.setEditable(True)

#         # Prevent user typing
#         self.lineEdit().setReadOnly(True)

#         for text in ["a", "b", "c"]:

#             item = QStandardItem(text)

#             item.setFlags(
#                 Qt.ItemIsEnabled |
#                 Qt.ItemIsUserCheckable
#             )

#             item.setData(Qt.Unchecked, Qt.CheckStateRole)

#             self.model().appendRow(item)

#         self.view().pressed.connect(self.handle_item_pressed)

#     def handle_item_pressed(self, index):

#         item = self.model().itemFromIndex(index)

#         if item.checkState() == Qt.Checked:
#             item.setCheckState(Qt.Unchecked)
#         else:
#             item.setCheckState(Qt.Checked)

#         self.update_text()

#     def update_text(self):

#         checked = []

#         for i in range(self.model().rowCount()):

#             item = self.model().item(i)

#             if item.checkState() == Qt.Checked:
#                 checked.append(item.text())

#         self.lineEdit().setText(", ".join(checked))

#     def get_checked_items(self):

#         checked = []

#         for i in range(self.model().rowCount()):

#             item = self.model().item(i)

#             if item.checkState() == Qt.Checked:
#                 checked.append(item.text())

#         return checked

#     def set_checked_items(self, values):

#         values = [v.strip() for v in values]

#         for i in range(self.model().rowCount()):

#             item = self.model().item(i)

#             if item.text() in values:
#                 item.setCheckState(Qt.Checked)
#             else:
#                 item.setCheckState(Qt.Unchecked)

#         self.update_text()

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        for text in pending_s:
            item = QStandardItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model().appendRow(item)

        self.view().pressed.connect(self.handle_item_pressed)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)
        self.update_text()

    def update_text(self):
        checked = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.Checked:
                checked.append(item.text())
        self.lineEdit().setText(", ".join(checked))

    def get_checked_items(self):
        checked = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.Checked:
                checked.append(item.text())
        return checked

    def set_checked_items(self, values):
        values = [v.strip() for v in values]
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            item.setCheckState(Qt.Checked if item.text() in values else Qt.Unchecked)
        self.update_text()

class PendingDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = CheckableComboBox(parent)
        editor.model().dataChanged.connect(
            lambda: self.commitData.emit(editor)
        )
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index)
        if value:
            editor.set_checked_items(value.split(","))

    def setModelData(self, editor, model, index):
        values = editor.get_checked_items()
        model.setData(index, ", ".join(values))