from eel import init as eel_init
from eel import expose as eel_expose
from eel import start as eel_start
from os import access as file_exists
from os import F_OK as file_exists_param
from os import listdir as scan_dir
from os import remove as del_file
from os import system as cmd_run
from threading import Thread as thread
from configparser import ConfigParser as cfg_parse_class


parser = cfg_parse_class()
sets = {
    'mainfile': 'index.html',
    'webfolder': 'web',
    'width': '800',
    'height': '600',
    'start_args': ['--incognito'],
    'port': '1337',
    'vms_dir': 'machines',
    'res_dir': 'res',
    'debug_bootmenu': 'boot_menu.py',
    'compiled_bootmenu': 'boot_menu.exe',
    'use_win7_theme': 'false'
}


debug = False
if file_exists('debug.txt', file_exists_param):
    debug = True
list_of_vms = []
temp_f_to_defconfig = open(sets['res_dir'] + '/defaultconfig.txt')
default_config = temp_f_to_defconfig.read()
temp_f_to_defconfig.close()
if sets['use_win7_theme'].lower() == 'true':
    from os import environ as env
    env['__COMPAT_LAYER'] = 'WinXPSp3'
current_vm = None


@eel_expose
def get_all_vms():
    global list_of_vms
    list_of_vms = []
    for i in scan_dir(sets['vms_dir']):
        list_of_vms.append(i[:-4])
    return list_of_vms


@eel_expose
def add_new_vm(new_vm_name):
    global list_of_vms
    if new_vm_name in list_of_vms:
        return False
    else:
        if not new_vm_name == '':
            list_of_vms.append(new_vm_name)
            tempf = open(sets['vms_dir'] + '/' + new_vm_name + '.txt', 'w')
            tempf.write(default_config)
            tempf.close()
            return True
        else:
            return False


@eel_expose
def remove_old_vm(new_vm_name):
    global list_of_vms
    global current_vm
    if new_vm_name in list_of_vms:
        list_of_vms.remove(new_vm_name)
        del_file(sets['vms_dir'] + '/' + new_vm_name + '.txt')
        current_vm = ''
        return True
    else:
        return False


@eel_expose
def set_current_vm(vm_name):
    global current_vm
    current_vm = vm_name


@eel_expose
def save_config(cfg_to_save):
    temp_conf = ''
    for i in default_config.split('\n'):
        if 'fullscreen' in i:
            temp_conf += 'fullscreen =' + str(cfg_to_save[0]).lower() + '\n'
        elif 'fullresolution =' in i:
            temp_conf += 'fullresolution = ' + cfg_to_save[1].lower() + '\n'
        elif 'windowresolution =' in i:
            temp_conf += 'windowresolution = ' + cfg_to_save[2].lower() + '\n'
        elif 'output =' in i:
            temp_conf += 'output = ' + cfg_to_save[3].lower() + '\n'
        elif 'sensitivity =' in i:
            temp_conf += 'sensitivity = ' + str(cfg_to_save[4]).lower() + '\n'
        elif 'language =' in i:
            temp_conf += 'language = ' + cfg_to_save[5].lower() + '\n'
        elif 'machine =' in i:
            temp_conf += 'machine = ' + cfg_to_save[6].lower() + '\n'
        elif 'memsize =' in i:
            temp_conf += 'memsize = ' + str(cfg_to_save[7]).lower() + '\n'
        elif 'core =' in i:
            temp_conf += 'core = ' + cfg_to_save[8].lower() + '\n'
        elif 'cputype =' in i:
            temp_conf += 'cputype = ' + cfg_to_save[9].lower() + '\n'
        elif 'cycles =' in i:
            temp_conf += 'cycles = ' + cfg_to_save[10].lower() + '\n'
        elif 'xms =' in i:
            temp_conf += 'xms = ' + str(cfg_to_save[11]).lower() + '\n'
        elif 'ems =' in i:
            temp_conf += 'ems = ' + str(cfg_to_save[12]).lower() + '\n'
        elif 'umb =' in i:
            temp_conf += 'umb = ' + str(cfg_to_save[13]).lower() + '\n'
        elif 'keyboardlayout =' in i:
            temp_conf += 'keyboardlayout = ' + cfg_to_save[14].lower() + '\n'
        elif 'fda =' in i:
            temp_conf += 'fda = ' + cfg_to_save[15].lower() + '\n'
        elif 'fdb =' in i:
            temp_conf += 'fdb = ' + cfg_to_save[16].lower() + '\n'
        elif 'hda =' in i:
            temp_conf += 'hda = ' + cfg_to_save[17].lower() + '\n'
        elif 'hdb =' in i:
            temp_conf += 'hdb = ' + cfg_to_save[18].lower() + '\n'
        elif 'hda_g =' in i:
            temp_conf += 'hda_g = ' + cfg_to_save[19].lower() + '\n'
        elif 'hdb_g =' in i:
            temp_conf += 'hdb_g = ' + cfg_to_save[20].lower() + '\n'
        elif 'mount_a =' in i:
            temp_conf += 'mount_a = ' + cfg_to_save[21].lower() + '\n'
        elif 'mount_c =' in i:
            temp_conf += 'mount_c = ' + cfg_to_save[22].lower() + '\n'
        else:
            temp_conf += i + '\n'
    temp_f_to_w = open(sets['vms_dir'] + '/' + current_vm + '.txt', 'w')
    temp_f_to_w.write(temp_conf)
    temp_f_to_w.close()
    return True


@eel_expose
def get_config():
    if not file_exists(
        sets['vms_dir'] + '/' + current_vm + '.txt', file_exists_param
    ):
        return False
    temp_conf_f = open(sets['vms_dir'] + '/' + current_vm + '.txt')
    conf = temp_conf_f.read()
    temp_conf_f.close()
    parser.read_string(conf)
    config_mas = []
    config_mas.append(parser['sdl']['fullscreen'])
    config_mas.append(parser['sdl']['fullresolution'])
    config_mas.append(parser['sdl']['windowresolution'])
    config_mas.append(parser['sdl']['output'])
    config_mas.append(parser['sdl']['sensitivity'])
    config_mas.append(parser['dosbox']['language'])
    config_mas.append(parser['dosbox']['machine'])
    config_mas.append(parser['dosbox']['memsize'])
    config_mas.append(parser['cpu']['core'])
    config_mas.append(parser['cpu']['cputype'])
    config_mas.append(parser['cpu']['cycles'])
    config_mas.append(parser['dos']['xms'])
    config_mas.append(parser['dos']['ems'])
    config_mas.append(parser['dos']['umb'])
    config_mas.append(parser['dos']['keyboardlayout'])
    config_mas.append(parser['dosboxvm']['fda'])
    config_mas.append(parser['dosboxvm']['fdb'])
    config_mas.append(parser['dosboxvm']['hda'])
    config_mas.append(parser['dosboxvm']['hdb'])
    config_mas.append(parser['dosboxvm']['hda_g'])
    config_mas.append(parser['dosboxvm']['hdb_g'])
    config_mas.append(parser['dosboxvm']['mount_a'])
    config_mas.append(parser['dosboxvm']['mount_c'])
    return config_mas


@eel_expose
def get_vm_name():
    return current_vm


def run_cmd(to_run):
    if cmd_run(to_run) == 228:
        result = cmd_run('"' + sets['res_dir'] + '\\dosbox.exe" -noconsole')
        if result == 1337:
            run_cmd(to_run)


def call_boot_menu(vm_name):
    run_str = None
    if debug:
        run_str = 'python "' + sets['debug_bootmenu']
        run_str += '" "' + vm_name + '" "' + sets['res_dir'] + '"'
        run_str += ' "' + sets['vms_dir'] + '"'
    else:
        run_str = '"' + sets['compiled_bootmenu']
        run_str += '" "' + vm_name + '" "' + sets['res_dir'] + '"'
        run_str += ' "' + sets['vms_dir'] + '"'
    thread(target=lambda: run_cmd(run_str)).start()


@eel_expose
def run_vm(vm_name):
    if vm_name in list_of_vms:
        call_boot_menu(vm_name)


eel_init(sets['webfolder'])
if __name__ == '__main__':
    eel_start(
        sets['mainfile'],
        size=(int(sets['width']), int(sets['height'])),
        cmdline_args=sets['start_args'],
        port=int(sets['port'])
    )
