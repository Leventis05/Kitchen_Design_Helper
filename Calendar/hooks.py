# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTableView, QCalendarWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit,  QLineEdit, QMessageBox, QTabWidget
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QBrush
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
    tabs.setTabText(1, f"Εγκρίσεις ({count})")

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

def mark_deadlines(self, dates):
    """
    dates: list of QDate objects ή python dates converted to QDate
    """

    fmt = QTextCharFormat()
    fmt.setBackground(QBrush(QColor("red")))
    fmt.setForeground(QBrush(QColor("white")))
    fmt.setFontWeight(75)  # bold

    for d in dates:
        self.calendar.setDateTextFormat(d, fmt)

def construct_string_from_record(record):
    client = record.value(api.DB_TABLE_COL[api.columns.CLIENT])
    designer = record.value(api.DB_TABLE_COL[api.columns.DESIGNER])
    a_date = record.value(api.DB_TABLE_COL[api.columns.ANALYSIS_DATE])
    c_date = record.value(api.DB_TABLE_COL[api.columns.CERT_DATE])
    pending = record.value(api.DB_TABLE_COL[api.columns.PENDING_ITEMS])
    
    return f"{client} - {designer} - {a_date} - {c_date} - {pending}"

def get_calendar_deadlines(date : QDate, calendar : QCalendarWidget, model : QSqlTableModel):
    str_date = date.toString(api.DB_FORMAT)

    model.setFilter(f"{api.DB_TABLE_COL[api.columns.CERT_DATE]} = '{str_date}")
    model.select()

    deadlines = []
    for row in range(model.rowCount()):
        record = model.record(row)
        deadlines.append(construct_string_from_record(record))

    if not deadlines:
        return
    
    msg = "\n".join(deadlines)

    QMessageBox.information(
        calendar,
        "Deadlines",
        msg
    )

    
    

def calendar_config(calendar : QCalendarWidget, model : QSqlTableModel):
    calendar.clicked.connect(lambda date : get_calendar_deadlines(date, calendar, model))

    

"""
from PyQt5.QtCore import QDate

deadlines = [
    QDate(2026, 5, 10),
    QDate(2026, 5, 12),
    QDate(2026, 5, 20),
]

self.mark_deadlines(deadlines)
"""
# COMMON
def resize_columns(view):
    view.resizeColumnsToContents()

