# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QTableView, QCalendarWidget, QPushButton, QVBoxLayout, 
    QWidget, QStyledItemDelegate, QDateEdit,  QLineEdit, QMessageBox, QTabWidget,
    QDialog, QLabel
)
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QBrush
from dataclasses import dataclass
from typing import Optional
import kapi as api
import gui_class as kgui

# Main model
def on_text_changed(text, proxy):
    proxy.setFilterWildcard(text)

# def add_row(model):
#     row = model.rowCount()
#     model.insertRow(row)

def add_row(model, calendar_model=None, parent=None):
    dialog = AddKitchenDialog()

    if dialog.exec_() == dialog.Accepted:
        data = dialog.get_data()

        row = model.rowCount()
        model.insertRow(row)

        model.setData(model.index(row, 1), data["client"])
        model.setData(model.index(row, 2), data["designer"])
        model.setData(model.index(row, 3), data["analysis"])
        model.setData(model.index(row, 4), data["cert"])
        model.setData(model.index(row, 5), data["pending"])

        model.submitAll()

        if calendar_model:
            calendar_model.select()

def delete_row(tuple, view):
    model, proxy = tuple
    reply = QMessageBox.question(
        None,
        "Διαγραφή γραμμής",
        "Σίγουρα;",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply is None or reply == QMessageBox.No:
        return
    p_index = view.currentIndex()
    s_index = proxy.mapToSource(p_index)
    if s_index.isValid():
        model.removeRow(s_index.row())
        model.submitAll()
        model.select()


# Reminders Short
def update_badge(model : QSqlTableModel, tabs : QTabWidget):
    count = model.rowCount()
    tabs.setTabText(1, f"Υπενθυμίσεις ({count})")

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

def get_calendar_deadlines(date, calendar, model):
    str_date = date.toString(api.DB_FORMAT)

    # save current filter
    old_filter = model.filter()

    # temporary filter
    model.setFilter(
        f"{api.DB_TABLE_COL[api.columns.CERT_DATE]} = '{str_date}'"
    )

    model.select()

    deadlines = []

    for row in range(model.rowCount()):
        record = model.record(row)
        deadlines.append(construct_string_from_record(record))

    # RESTORE ORIGINAL FILTER
    model.setFilter(old_filter)
    model.select()

    if not deadlines:
        return

    msg = "\n".join(deadlines)

    QMessageBox.information(
        calendar,
        "Deadlines",
        msg
    )

def refresh_calendar_deadlines(calendar, model):

    # clear previous formatting
    calendar.setDateTextFormat(QDate(), QTextCharFormat())

    today = QDate.currentDate()

    cert_col = api.DB_TABLE_COL[api.columns.CERT_DATE]

    # IMPORTANT:
    # save current filter
    old_filter = model.filter()

    # temporarily remove ALL filters
    model.setFilter("")
    model.select()

    for row in range(model.rowCount()):

        record = model.record(row)

        date_str = record.value(cert_col)

        deadline = QDate.fromString(date_str, api.DB_FORMAT)

        if not deadline.isValid():
            continue

        days_left = today.daysTo(deadline)

        fmt = QTextCharFormat()

        # RED -> 24h or overdue
        if days_left <= 1:
            fmt.setBackground(QBrush(QColor("red")))
            fmt.setForeground(QBrush(QColor("white")))

        # ORANGE -> 48h
        elif days_left <= 2:
            fmt.setBackground(QBrush(QColor("orange")))
            fmt.setForeground(QBrush(QColor("black")))

        else:
            continue

        fmt.setFontWeight(75)

        calendar.setDateTextFormat(deadline, fmt)

    # restore original filter
    model.setFilter(old_filter)
    model.select()

# def calendar_config(calendar : QCalendarWidget, model : QSqlTableModel):
#     calendar.clicked.connect(lambda date : get_calendar_deadlines(date, calendar, model))

def calendar_config(calendar, model):
    refresh_calendar_deadlines(calendar, model)

    calendar.clicked.connect(
        lambda date: get_calendar_deadlines(date, calendar, model)
    )

"""
from PyQt5.QtCore import QDate

deadlines = [
    QDate(2026, 5, 10),
    QDate(2026, 5, 12),
    QDate(2026, 5, 20),
]

self.mark_deadlines(deadlines)
"""


class AddKitchenDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Προσθήκη νέας σειράς")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.client = QLineEdit()
        self.client.setPlaceholderText("Ονοματεπώνυμο")

        self.designer = QLineEdit()
        self.designer.setPlaceholderText("Ονοματεπώνυμο")

        self.analysis_date = QDateEdit()
        self.analysis_date.setCalendarPopup(True)
        self.analysis_date.setDate(QDate.currentDate())

        self.cert_date = QDateEdit()
        self.cert_date.setCalendarPopup(True)
        self.cert_date.setDate(QDate.currentDate())

        self.pending = api.CheckableComboBox()

        self.save_btn = QPushButton("Save")

        layout.addWidget(QLabel("Πελάτης"))
        layout.addWidget(self.client)

        layout.addWidget(QLabel("Σχεδιαστής"))
        layout.addWidget(self.designer)

        layout.addWidget(QLabel("Ημερομηνία Έγκρισης"))
        layout.addWidget(self.analysis_date)

        layout.addWidget(QLabel("Ημερομηνία Ανάλυσης"))
        layout.addWidget(self.cert_date)

        layout.addWidget(QLabel("Εκρεμμότητες"))
        layout.addWidget(self.pending)

        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self.accept)

    def get_data(self):
        return {
            "client": self.client.text(),
            "designer": self.designer.text(),
            "analysis": self.analysis_date.date().toString("yyyy-MM-dd"),
            "cert": self.cert_date.date().toString("yyyy-MM-dd"),
            "pending": ", ".join(self.pending.get_checked_items())
        }


# COMMON
def resize_columns(view):
    view.resizeColumnsToContents()
