# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTableView, QVBoxLayout, QWidget, QCalendarWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QSortFilterProxyModel
from typing import Callable, Optional
import kapi as api


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
    
    def add_init_model(self, name : str, initFunc : Callable, proxy : bool = False):
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

        if configFunc:
            configFunc(self.calendar, model)

    def exec(self):
        self.tabs.resize(1000, 700)
        self.tabs.show()
        self.app.exec_()
