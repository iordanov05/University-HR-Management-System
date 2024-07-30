import sys
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
sys_path_loc = config['Settings']['library_module']
sys.path.append(sys_path_loc)  # Добавляем путь к каталогу, содержащему module_universal

import tkinter as tk

import os
import time
from module_specialized import create_report_page
from module_universal_new import upload_files

        
def apply_styles(widget, label_type=None)->None:
    '''
    Настраивает стили для указанного виджета в соответствии с текущей темой.

    Parameters
    ----------
    widget : Tkinter widget
        Виджет, для которого применяются стили.
    label_type : str, optional
       Тип стилизации метки. По умолчанию None.

    Returns
    -------
    None

    '''
    config = configparser.ConfigParser()
    config.read('config.ini')
    bg_color = config.get('Theme', config.get('Settings', 'current_theme') + 'Background')
    text_color = config.get('Theme', config.get('Settings', 'current_theme') + 'Text')
    button_bg = config.get('Theme', config.get('Settings', 'current_theme') + 'Button')
    font = config.get('Settings', 'Font')
    darktext = config.get('Theme', 'DarkText')
    violetbutton=config.get('Theme', 'violetbutton')

    if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
        widget.configure(bg=bg_color)
    elif isinstance(widget, tk.Label):
        if label_type == 'type1':
            widget.config(fg=text_color, bg=bg_color, font=(font, 20))
        elif label_type == 'type2':
            widget.config(fg=darktext, bg=button_bg, font=(font, 20))
    elif isinstance(widget, tk.Button) or isinstance(widget, tk.OptionMenu):
        if label_type == 'violet':
            widget.config(bg=violetbutton, fg="white", font=(font, 14))
        elif label_type == 'normal':
            widget.config(bg=button_bg, fg="white", font=(font, 14))
    elif isinstance(widget, tk.Frame):
        if label_type == 'dark':
            widget.config(bg=button_bg)
        elif label_type == 'light':
            widget.config(bg=bg_color)
    elif isinstance(widget, tk.Radiobutton):
        widget.config(bg=bg_color, fg=text_color)
    elif isinstance(widget, tk.Checkbutton):
        widget.config(bg=bg_color, fg=text_color)
    elif isinstance(widget, tk.Toplevel):
        widget.config(bg=violetbutton, fg='white',font=(font, 14))


def reload_configuration()->None:
    '''
    Повторно настраивает стили интерфейса в соответствии с текущей конфигурацией.

    Returns
    -------
    None
    '''
    apply_styles(window)
    apply_styles(title_label_1, label_type='type1')  
    apply_styles(title_label_2, label_type='type1')
    apply_styles(load_data_button, label_type='normal')
    apply_styles(exit_button, label_type='normal')
    if DATA:
        apply_styles(show_reports_button,label_type='normal' )
    else:
        show_reports_button.config(state="disabled", bg=config.get('Theme', 'DisabledButton'),\
                                   fg=config.get('Theme', 'DarkText'))
    apply_styles(settings_button,label_type='normal')
    window.update()

def monitor_config_changes(filepath, callback, interval=1)->None:
    '''
    Мониторит изменения в указанном файле конфигурации и вызывает указанную функцию обратного вызова при обнаружении изменений.

    Parameters
    ----------
    filepath : str
        Путь к файлу конфигурации.
    callback : function
        Функция обратного вызова, которая будет вызвана при изменении файла конфигурации.
    interval : int, optional
        Интервал проверки изменений в секундах. По умолчанию 1.

    Returns
    -------
    None
   '''
    last_mtime = os.path.getmtime(filepath)
    while True:
        time.sleep(interval)
        try:
            current_mtime = os.path.getmtime(filepath)
        except FileNotFoundError:
            continue
        if current_mtime != last_mtime:
            last_mtime = current_mtime
            callback()

# Чтение из файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')

# Создание окна
window = tk.Tk()
window.title("Университетская система управления персоналом")
window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
apply_styles(window)  # Применяем стили при создании окна

# Другие элементы интерфейса
title_label_1 = tk.Label(window, text="Университетская система управления")
title_label_1.pack(pady=(200, 0))
apply_styles(title_label_1, label_type='type1')

title_label_2 = tk.Label(window, text="персоналом", wraplength=400)
title_label_2.pack(pady=0)  
apply_styles(title_label_2, label_type='type1')

load_data_button = tk.Button(window, text="Загрузить данные", bd=0, width=40, height=2)
load_data_button.pack(pady=(100, 30))
load_data_button.config(command=lambda: upload_files(apply_styles))
apply_styles(load_data_button, label_type='normal')

exit_button = tk.Button(window, text="Завершить", bd=0, command=window.destroy)
exit_button.place(x=10, y=10)
apply_styles(exit_button, label_type='normal')

def check_folder(folder_path)->bool:
    '''
    Проверяет наличие файлов в указанной папке.

    Parameters
    ----------
    folder_path : str
        Путь к целевой папке.

    Returns
    -------
    bool
        True, если папка содержит файлы, иначе False.
    '''
    # Проверяем, есть ли файлы в папке
    return any(os.scandir(folder_path))

folder_path = config.get('Settings', 'data_folder')
DATA = check_folder(folder_path)

show_reports_button = tk.Button(window, text="Отчеты", bd=0, width=40, height=2)
show_reports_button.config(state="disabled")
if DATA:
    show_reports_button.config(state="normal")
    show_reports_button.config(command=lambda: create_report_page(apply_styles))
show_reports_button.pack(pady=10)
apply_styles(show_reports_button, label_type='normal')

def open_settings()->None:
    '''
    Открывает окно настроек, запуская скрипт settings.py.

    Returns
    -------
    None
    '''
    os.system('python settings.py')

settings_button = tk.Button(window, text="⚙", borderwidth=0, command=open_settings)
settings_button.place(x=1475, y=10)
apply_styles(settings_button,label_type='normal')

def poll_config_changes()->None:
    '''
    Периодически проверяет изменения в файле конфигурации и перезагружает конфигурацию при обнаружении изменений.

    Returns
    -------
    None
    '''
    current_mtime = os.path.getmtime('config.ini')
    if current_mtime != poll_config_changes.last_mtime:
        poll_config_changes.last_mtime = current_mtime
        reload_configuration()
    
    window.after(1000, poll_config_changes)  # Повторяем проверку каждую секунду

poll_config_changes.last_mtime = os.path.getmtime('config.ini')  # Инициализация времени последнего изменения
poll_config_changes()  # Запуск функции мониторинга

window.mainloop()

