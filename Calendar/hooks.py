# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTableView, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QLineEdit, QMessageBox, QTabWidget
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from dataclasses import dataclass
from typing import Optional
import kapi as api
import gui_class as kgui

# Main model
def on_text_changed(text, proxy):
    proxy.setFilterWildcard(text)

def add_row(model):
    row = model.rowCount()
    model.insertRow(row)

def delete_row(tuple, view):
    model, proxy = tuple
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


# Reminders Short
def update_badge(model : QSqlTableModel, tabs : QTabWidget):
    count = model.rowCount()
    tabs.setTabText(1, f"Reminders ({count})")

def refresh_reminders_short(model : QSqlTableModel, tabs : Optional[QTabWidget] = None):
    today = QDate.currentDate()
    two_days_later = today.addDays(2)

    start = today.toString("yyyy-MM-dd")
    end = two_days_later.toString("yyyy-MM-dd")

    columns = api.columns
    col = api.DB_TABLE_COL[columns.CERT_DATE]
    model.setFilter(f"{col} BETWEEN '{start}' AND '{end}'")

    model.setFilter(f"{col} BETWEEN '{start}' AND '{end}'")
    model.select()
    if tabs:
        update_badge(model, tabs)

# COMMON
def resize_columns(view):
    view.resizeColumnsToContents()

