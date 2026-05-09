# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QTableView, QMainWindow, QPushButton, 
    QVBoxLayout, QWidget, QComboBox, QStyledItemDelegate, QDateEdit,  
    QLineEdit, QMessageBox, QTabWidget
)
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from dataclasses import dataclass
from typing import Optional
import kapi as api
import hooks as hks

# Calling func(model, proxy)
class mdl_init_funcs:
    def main_init(model : QSqlTableModel, proxy : Optional[QSortFilterProxyModel]):
        model.setTable(api.DB_MAIN_TABLE)   # table name
        model.select()            # load data
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.setHeaderData(1, Qt.Horizontal, "Ονοματεπώνυμο Πελάτη")
        model.setHeaderData(2, Qt.Horizontal, "Ονοματεπώνυμο Σχεδιαστή")
        model.setHeaderData(3, Qt.Horizontal, "Ημερομηνία Έγκρισης")
        model.setHeaderData(4, Qt.Horizontal, "Ημερομηνία Ανάλυσης")
        model.setHeaderData(5, Qt.Horizontal, "Εκκρεμότητες")

        proxy.setSourceModel(model)
        proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy.setFilterKeyColumn(1)  # column to search (e.g. name)

    def rem_short_init(model : QSqlTableModel, proxy : Optional[QSortFilterProxyModel]):
        model.setTable(api.DB_MAIN_TABLE)
        model.setHeaderData(1, Qt.Horizontal, "Ονοματεπώνυμο Πελάτη")
        model.setHeaderData(2, Qt.Horizontal, "Ονοματεπώνυμο Σχεδιαστή")
        model.setHeaderData(3, Qt.Horizontal, "Ημερομηνία Έγκρισης")
        model.setHeaderData(4, Qt.Horizontal, "Ημερομηνία Ανάλυσης")
        model.setHeaderData(5, Qt.Horizontal, "Εκκρεμότητες")
        hks.refresh_reminders_short(model)

    def rem_long_init(model : QSqlTableModel, proxy : Optional[QSortFilterProxyModel]):
        pass



# Calling func((model, proxy), view)
class vw_init_funcs:
    def main_init(tuple, view : QTableView):
        test, proxy = tuple
        view.date_delegate = api.DateDelegate()
        view.pending_delegate = api.PendingDelegate()

        view.setModel(proxy)
        view.resizeColumnsToContents()
        view.horizontalHeader().setStretchLastSection(True)
        view.setColumnHidden(0, True)
        view.setItemDelegateForColumn(3, view.date_delegate)
        view.setItemDelegateForColumn(4, view.date_delegate)

        view.setItemDelegateForColumn(5, view.pending_delegate)

    def rem_short_init(tuple, view : QTableView):
        model, proxy = tuple
        view.setModel(model)
        view.resizeColumnsToContents()
        view.setColumnHidden(0, True)
        view.horizontalHeader().setStretchLastSection(True)

    def rem_long_init(tuple, view : QTableView):
        pass



# Calling func(model, view, layout)
class lout_init_funcs:
    def main_init(tuple, view : QTableView, layout : QVBoxLayout):
        model, proxy = tuple

        #BUTTONS AND SEARCHBAR
        search = QLineEdit()
        search.setPlaceholderText("Search...")
        search.textChanged.connect(lambda text: hks.on_text_changed(text, proxy))

        add_tuple_btn = QPushButton("Εισαγωγή Δεδομένων")
        add_tuple_btn.clicked.connect(lambda i: hks.add_row(model))

        dltRowButton = QPushButton("Διαγραφή Γραμμής")
        dltRowButton.clicked.connect(lambda i: hks.delete_row(tuple, view))
        
        #CREATE TAB
        layout.addWidget(view)
        layout.addWidget(search)
        layout.addWidget(add_tuple_btn)
        layout.addWidget(dltRowButton)

    def rem_short_init(tuple, view : QTableView, layout : QVBoxLayout):
        layout.addWidget(view)

    def rem_long_init(tuple, view : QTableView, layout : QVBoxLayout):
        model, proxy = tuple
        pass




# Calling func(model_tuple, vw_lout_tuple, tabs)
class tab_config_funcs:
    def main_config(m_tuple, vl_tuple, tabs : QWidget):
        view, layout = vl_tuple
        index = tabs.count() - 1
        tabs.currentChanged.connect(lambda i: hks.resize_columns(view) if i == index else None)
    
    def rem_short_config(m_tuple, vl_tuple, tabs : QWidget):
        model, proxy = m_tuple
        view, layout = vl_tuple

        hks.update_badge(model, tabs)
        tabs.currentChanged.connect(lambda i: hks.refresh_reminders_short(model, tabs) if i == 1 else None)
        tabs.currentChanged.connect(lambda i: hks.resize_columns(view) if i == 1 else None)
    
    def rem_long_config(m_tuple, vl_tuple, tabs : QWidget):
        pass