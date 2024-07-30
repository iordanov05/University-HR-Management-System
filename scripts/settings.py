import tkinter as tk
from tkinter import ttk
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

root = tk.Tk()
root.title("Настройка стиля приложения")
root.minsize(width=400, height=300)

# Убедитесь, что начальные значения установлены
if not config.has_option('Settings', 'Font'):
    config.set('Settings', 'Font', 'Arial')
if not config.has_option('Settings', 'current_theme'):
    config.set('Settings', 'current_theme', 'Light')

selected_font = config.get('Settings', 'Font', fallback='Arial')
theme = config.get('Settings', 'current_theme', fallback='Light')

def apply_style():
    selected_font = font_combobox.get()
    theme = theme_var.get()
    if theme == 'Dark':
        root.config(bg=config.get('Theme', 'DarkBackground'))
        selected_button_color = config.get('Theme', 'violetbutton')
        theme_label.config(fg=config.get('Theme', 'DarkText'), 
                     bg=config.get('Theme', 'DarkBackground'), font=(selected_font, 20))
        font_label.config(fg=config.get('Theme', 'DarkText'), 
                     bg=config.get('Theme', 'DarkBackground'), font=(selected_font, 20))
        button_apply.config(fg=config.get('Theme', 'DarkText'), 
                      bg=config.get('Theme', 'DarkButton'), font=(selected_font, 12))
        button_back.config(fg=config.get('Theme', 'DarkText'), 
                      bg=config.get('Theme', 'DarkButton'), font=(selected_font, 12))
        light_theme_button.config(relief=tk.RAISED,fg=config.get('Theme', 'DarkText'), 
                      bg=config.get('Theme', 'DarkButton'), font=(selected_font, 12))
        dark_theme_button.config(relief=tk.SUNKEN,fg=config.get('Theme', 'DarkText'), 
                      bg=selected_button_color, font=(selected_font, 12))
        theme_frame.config(bg=config.get('Theme', 'DarkBackground'))
        
    elif theme == 'Light':
        root.config(bg=config.get('Theme', 'LightBackground'))
        selected_button_color = config.get('Theme', 'violetbutton')
        theme_label.config(fg=config.get('Theme', 'LightText'), 
                   bg=config.get('Theme', 'LightBackground'), font=(selected_font, 20))
        theme_frame.config(bg=config.get('Theme', 'LightBackground'))
        font_label.config(fg=config.get('Theme', 'LightText'), 
                   bg=config.get('Theme', 'LightBackground'), font=(selected_font, 20))
        button_apply.config(fg=config.get('Theme', 'LightText'), 
                      bg=config.get('Theme', 'LightButton'), font=(selected_font, 12))
        button_back.config(fg=config.get('Theme', 'DarkText'), 
                      bg=config.get('Theme', 'LightButton'), font=(selected_font, 12))
        light_theme_button.config(relief=tk.SUNKEN,fg=config.get('Theme', 'DarkText'), 
                      bg=selected_button_color, font=(selected_font, 12))
        dark_theme_button.config(relief=tk.RAISED,fg=config.get('Theme', 'LightText'), 
                      bg=config.get('Theme', 'LightButton'), font=(selected_font, 12))
        

    # Сохранение выбора в конфигурацию
    if 'Fonts' in config:
        for option in config.options('Fonts'):
            if config.get('Fonts', option) == selected_font:
                config.set('Settings', 'Font', selected_font)
                break

    config.set('Settings', 'current_theme', theme)
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def font_selected(event):
    apply_style()

def theme_changed(theme_choice):
    theme_var.set(theme_choice)
    apply_style()

if 'Fonts' in config:
    fonts = [config.get('Fonts', font) for font in config.options('Fonts')]
    font_label = tk.Label(root, text="Выберите шрифт:", font=(selected_font, 16))
    font_label.pack(pady=10)

    font_combobox = ttk.Combobox(root, values=fonts)
    font_combobox.pack(pady=10)
    font_combobox.set(selected_font)  # Устанавливаем начальное значение
    font_combobox.bind("<<ComboboxSelected>>", font_selected)

theme_label = tk.Label(root, text="Выберите тему:", font=(selected_font, 12))
theme_label.pack(pady=10)

theme_var = tk.StringVar(value=theme)
theme_frame = tk.Frame(root)
theme_frame.pack(pady=10)

light_theme_button = tk.Button(theme_frame, text="Светлая тема", command=lambda: theme_changed("Light"), relief=tk.SUNKEN if theme == "Light" else tk.RAISED)
dark_theme_button = tk.Button(theme_frame, text="Темная тема", command=lambda: theme_changed("Dark"), relief=tk.SUNKEN if theme == "Dark" else tk.RAISED)
light_theme_button.pack(side=tk.LEFT, padx=10)
dark_theme_button.pack(side=tk.LEFT)

button_apply = tk.Button(root, text="Применить везде", font=(selected_font, 12), command=root.destroy, bd=0)
button_apply.pack(pady=10)

button_back = tk.Button(root, text="Назад", font=(selected_font, 12), command=root.destroy, bd=0)
button_back.pack(pady=10)

apply_style()  # Применяем начальные стили

root.mainloop()
