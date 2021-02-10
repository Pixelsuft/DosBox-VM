from sys import exit as sys_exit
from sys import argv as start_args
from PyQt5 import QtWidgets as qt_widgets
from boot_menu_ui import Ui_MainWindow as main_window
from clear_cache import clear as clear_cache
from threading import Thread as thread
from time import sleep as time_sleep
from os import remove as del_file
from os import access as file_exists
from os import listdir as scan_dir
from os import F_OK as file_exists_param
from win32api import GetAsyncKeyState as is_pressed
from win32con import VK_F1 as F1
from win32con import VK_F2 as F2
from win32con import VK_F3 as F3
from configparser import ConfigParser as cfg_parse_class


parser = cfg_parse_class()
boot_device = 'c'
vm_running = False
temp_conf_f = open(start_args[3] + '/' + start_args[1] + '.txt')
conf = temp_conf_f.read()
temp_conf_f.close()
parser.read_string(conf)
boot_many_fd = False


def run_vm():
    global conf
    if file_exists('dosbox.conf', file_exists_param):
        del_file('dosbox.conf')
    conf += '\n'
    if not parser['dosboxvm']['mount_a'] == '':
        temp_check = parser['dosboxvm']['mount_a']
        conf += 'mount a "' + temp_check + '"\n'
    if not parser['dosboxvm']['mount_c'] == '':
        temp_check = parser['dosboxvm']['mount_c']
        conf += 'mount c "' + temp_check + '"\n'
    if not parser['dosboxvm']['fdb'] == '':
        temp_check = parser['dosboxvm']['fdb']
        conf += 'imgmount 1 "' + temp_check + '" -t floppy'
        conf += ' -fs none\n'
    if not parser['dosboxvm']['hda'] == '':
        temp_check = parser['dosboxvm']['hda']
        conf += 'imgmount 2 "' + temp_check + '" -t hdd'
        conf += ' -fs none'
        conf += ' -size ' + parser['dosboxvm']['hda_g'] + '\n'
    if not parser['dosboxvm']['hdb'] == '':
        temp_check = parser['dosboxvm']['hdb']
        conf += 'imgmount 3 "' + temp_check + '" -t hdd'
        conf += ' -fs none'
        conf += ' -size ' + parser['dosboxvm']['hdb_g'] + '\n'
    if boot_many_fd:
        temp_boot = '"'
        for i in parser['dosboxvm']['fda'].split(';'):
            if not temp_boot == '"':
                temp_boot += '" "'
            temp_boot += i
        temp_boot += '"'
        conf += 'boot ' + temp_boot
    else:
        if not parser['dosboxvm']['fda'] == '':
            temp_check = parser['dosboxvm']['fda']
            if ' ' in temp_check:
                temp_check = '"' + temp_check + '"'
            conf += 'imgmount 0 "' + temp_check + '" -t floppy'
            conf += ' -fs none\n'
        conf += 'boot -l ' + boot_device
    temp_conf_w = open('dosbox.conf', 'w')
    temp_conf_w.write(conf)
    temp_conf_w.close()
    MainWindow.close()


def trigger_timer():
    global vm_running
    sleep_count = 5
    for i in scan_dir(start_args[2]):
        if i[:6] == 'sleep_':
            sleep_count = int(i[6:-4])
    sleep_count += 1
    while sleep_count > 0 and not vm_running:
        sleep_count -= 1
        ui.startin.setText('Starting in ' + str(sleep_count) + '...')
        time_sleep(1)
    if not vm_running:
        vm_running = True
        run_vm()


def read_keys():
    global boot_device
    global vm_running
    global boot_many_fd
    while not vm_running:
        if is_pressed(F1):
            boot_device = 'a'
            try:
                boot_device = parser['dosboxvm']['fda']
                boot_many_fd = True
            except KeyError:
                pass
            run_vm()
            vm_running = True
            break
        elif is_pressed(F2):
            boot_device = 'c'
            run_vm()
            vm_running = True
            break
        elif is_pressed(F3):
            boot_device = 'd'
            run_vm()
            vm_running = True
            break


argv = len(start_args)
if argv < 3:
    exit()
app = qt_widgets.QApplication([__name__])
MainWindow = qt_widgets.QMainWindow()
ui = main_window()
ui.setupUi(MainWindow)
MainWindow.setWindowTitle(start_args[1] + ' - Pixelsuft DOSBox VM')
MainWindow.show()
thread(target=trigger_timer).start()
thread(target=read_keys).start()
exitcode = app.exec_()
clear_cache()
sys_exit(exitcode)
