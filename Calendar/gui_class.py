# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QTableView, QVBoxLayout, QWidget, QCalendarWidget, QTabWidget
)
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QDate
from PyQt5.QtGui import QColor, QBrush
from typing import Callable, Optional
import kapi as api
import hooks as hks


class K_GUI:
    def __init__(self):
        self.app = QApplication([])
        self.tabs = QTabWidget()
        self.db = api.database()
        self.models = {}
        self.views = {}
        self.layouts = {}

        # dedicated calendar model
        self.calendar_model = QSqlTableModel()
        self.calendar_model.setTable(api.DB_MAIN_TABLE)
        self.calendar_model.select()
    
    def add_init_model(self, name : str, initFunc : Callable, proxy : bool = False, model = None):
        if not model:
            model = QSqlTableModel()

        _proxy = QSortFilterProxyModel() if proxy else None
        entry = (model, _proxy)
        self.models[name] = entry
        # Calling func(model, proxy)
        initFunc(model, _proxy)
    
    def add_init_view(self, name : str, initFunc : Callable):
        entry = QTableView()
        self.views[name] = entry
        # Calling func(model, view)
        initFunc(self.models[name], entry)
    
    def add_init_layout(self, name : str, initFunc : Callable):
        entry = QVBoxLayout()
        self.layouts[name] = entry
        # Calling func(model, view, layout)
        initFunc(self.models[name], self.views[name], entry)

    def add_config_tab(self, name : str, header : str, configFunc : Callable):
        newTab = QWidget()
        newTab.setLayout(self.layouts[name])
        self.tabs.addTab(newTab, header)
        # Calling func(model_tuple, vw_lout_tuple, tab, index)
        configFunc(self.models[name], (self.views[name], self.layouts[name]), self.tabs)

    # def add_calendar(self, configFunc: Optional[Callable] = None):
    def add_calendar(self, configFunc=None, model=None):
        self.calendar_tab = QWidget()
        self.calendar_layout = QVBoxLayout(self.calendar_tab)

        self.calendar = QCalendarWidget()
        self.calendar_layout.addWidget(self.calendar)

        self.tabs.addTab(self.calendar_tab, "Ημερολόγιο")

        self.tabs.currentChanged.connect(lambda i: hks.refresh_calendar_deadlines(self.calendar, model) if i == 2 else None)

        if configFunc:
            configFunc(self.calendar, model)

    def exec(self):
        self.tabs.resize(1000, 700)
        self.tabs.show()
        self.app.exec_()


class DeadlineModel(QSqlTableModel):

    def __init__(self, date_column, parent=None):
        super().__init__(parent)

        self.date_column = date_column

    def data(self, index, role=Qt.DisplayRole):

        # normal database value
        value = super().data(index, role)

        if not index.isValid():
            return value

        # get deadline date from the row
        date_index = self.index(index.row(), self.date_column)

        date_str = super().data(date_index, Qt.DisplayRole)

        deadline = QDate.fromString(date_str, "yyyy-MM-dd")

        if not deadline.isValid():
            return value

        today = QDate.currentDate()

        deadline = deadline.addDays(3)
        days_left = today.daysTo(deadline)

        # RED rows
        if days_left <= 1:

            if role == Qt.BackgroundRole:
                return QBrush(QColor("red"))

            if role == Qt.ForegroundRole:
                return QBrush(QColor("white"))

        # ORANGE rows
        elif days_left <= 2:

            if role == Qt.BackgroundRole:
                return QBrush(QColor("orange"))

            if role == Qt.ForegroundRole:
                return QBrush(QColor("black"))

        return value