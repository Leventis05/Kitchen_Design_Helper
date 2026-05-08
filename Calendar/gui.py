# -*- coding: utf-8 -*-
from dataclasses import dataclass
import gui_class as kgui
import init_funcs as init

import db_api

class Keys:
    MAIN = "main"
    REMINDERS_SHORT = "rem sh"
    REMINDERS_LONG = "rem lg"

MDL = Keys
VW = Keys
LOUT = Keys

MDL_INIT = init.mdl_init_funcs
VW_INIT = init.vw_init_funcs
LOUT_INIT = init.lout_init_funcs
TAB_CONFIGS = init.tab_config_funcs


# TODO add rem long
def gui_insert_models(gui : kgui.K_GUI):
    gui.add_init_model(MDL.MAIN, MDL_INIT.main_init, True)
    gui.add_init_model(MDL.REMINDERS_SHORT, MDL_INIT.rem_short_init)
    

def gui_insert_views(gui : kgui.K_GUI):
    gui.add_init_view(VW.MAIN, VW_INIT.main_init)
    gui.add_init_view(VW.REMINDERS_SHORT, VW_INIT.rem_short_init)

def gui_insert_layouts(gui : kgui.K_GUI):
    gui.add_init_layout(LOUT.MAIN, LOUT_INIT.main_init)
    gui.add_init_layout(LOUT.REMINDERS_SHORT, LOUT_INIT.rem_short_init)

def gui_insert_tabs(gui : kgui.K_GUI):
    gui.add_config_tab(MDL.MAIN, "Όλες οι δουλειές", TAB_CONFIGS.main_config)
    gui.add_config_tab(MDL.REMINDERS_SHORT, "Εγκρίσεις", TAB_CONFIGS.rem_short_config)
    gui.add_calendar()

# MAIN
def main():
    # api1 = db_api.api()
    # api1.select_all()

    gui = kgui.K_GUI()

    gui_insert_models(gui)
    gui_insert_views(gui)
    gui_insert_layouts(gui)
    gui_insert_tabs(gui)

    gui.exec()


if __name__ == "__main__":
    main()
