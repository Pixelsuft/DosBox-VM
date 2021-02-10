@echo off
del boot_menu_ui.py
pyuic5 boot_menu_ui.ui -o boot_menu_ui.py -x
