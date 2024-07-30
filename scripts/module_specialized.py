import tkinter as tk
import configparser
from tkinter import messagebox, filedialog, scrolledtext, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

arr_text = ['Простой текстовый отчет', 'Сводная таблица', \
            'Отчет о частоте предметов', 'Статистический отчет']
arr_graph = ['Распределение часов в неделю в зависимости от курса', \
            'Распределение часов в неделю по предметам для каждого преподавателя',\
                'Распределение количества отработанных часов по предметам', \
                        'Статистика часов преподавания по предметам']

arr_func = ['create_simple_report','create_pivot_table','create_frequency_report','create_text_statistics','create_scatter_plot',\
            'create_bar_chart','create_categorize_gist',\
                'create_boxwhisker_diagram']
    
df_chasy_path = config['Settings']['df_chasy']
df_prepodavateli_path = config['Settings']['df_prepodavateli']
df_kursy_napravleniya_path = config['Settings']['df_kursy_napravleniya']
df_predmety_path = config['Settings']['df_predmety']
graphics_report_dir = config['Settings']['graphics_report']
text_report_dir = config['Settings']['text_report']

# Основные интерфейсы
def go_back(report_window)->None:
    '''
    Закрывает окно отчетов.

    Parameters
    ----------
    report_window : tk.Toplevel
        Окно отчетов, которое необходимо закрыть.

    Returns
    -------
    None
    '''
    report_window.destroy()    
    
def save_plot(fig)->None:
    '''
    Сохраняет график в формате PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Объект графика, который необходимо сохранить.

    Returns
    -------
    None
    '''
    file_path = filedialog.asksaveasfilename(initialdir=graphics_report_dir,\
                                             defaultextension=".png",\
                                            filetypes=(("PNG files", "*.png"),\
                                                       ("All files", "*.*")))
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Сохранено", "Отчет успешно сохранен!")
    else:
        messagebox.showinfo("Отмена", "Сохранение отчета отменено")

def create_report_page(apply_styles)->None:
    '''
    Создает страницу с отчетами.

    Parameters
    ----------
    apply_styles : function
        Функция для применения стилей к виджетам.

    Returns
    -------
    None
    '''
    report_window = tk.Toplevel()
    report_window.title("Отчеты")
    report_window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))

    apply_styles(report_window)
    
    header_frame = tk.Frame(report_window, bg="#0D99FF")
    header_frame.place(relwidth=1, relheight=0.1)  # Покрывает всю ширину окна
    apply_styles(header_frame, label_type='dark')
    header_label = tk.Label(header_frame, text="Отчеты")
    header_label.place(relx=0.5, rely=0.5, anchor='center')
    apply_styles(header_label, label_type='type2')
    
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, \
                                command=lambda: go_back(report_window))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type='normal')

    # Заголовки
    text_reports_label = tk.Label(report_window, text="Текстовые отчеты")
    text_reports_label.grid(row=0, column=0, padx=(50, 100), pady=(100, 20)) 
    apply_styles(text_reports_label, label_type='type1')
    graphical_reports_label = tk.Label(report_window,\
                                       text="Графические отчеты")
    graphical_reports_label.grid(row=0, column=1, padx=(100, 50),\
                                 pady=(100, 20))  # Добавлен отступ между колонками
    apply_styles(graphical_reports_label,  label_type='type1')
# Кнопки
    for i in range(1, 5):
        text_reports_button = tk.Button(report_window, text=arr_text[i-1],\
                                        bd=0, width=52, height=3,\
                                                    wraplength=440)
        text_reports_button.grid(row=i, column=0, padx=(50, 50), pady=20)
        apply_styles(text_reports_button, label_type='normal')
        text_reports_button.config(command=lambda i=i: globals()[arr_func[i-1]](apply_styles))    
        graphical_reports_button = tk.Button(report_window,\
                                            text=arr_graph[i-1], bg="#0D99FF", bd=0, width=57,\
                                                     height=3, \
                                                         wraplength=440)
        graphical_reports_button.grid(row=i, column=1, padx=(50, 50), pady=0)
        graphical_reports_button.config(command=lambda i=i:globals()[arr_func[i-1+4]](apply_styles))
        apply_styles(graphical_reports_button,label_type='normal')


# Текстовые отчеты
def create_pivot_table(apply_styles)->None:
    '''
    Создает сводную таблицу и показывает ее текстовое представление.

    Parameters
    ----------
    apply_styles : function
        Функция для применения стилей к виджетам.

    Returns
    -------
    None
    '''
    def display_report()->None:
        '''
        Генерирует сводную таблицу и отображает ее в текстовом виде.

        Returns
        -------
        None.

        '''
        global report
        report = pivotTable(df_chasy, df_prepodavateli, df_predmety)
        
        # Форматирование данных сводной таблицы в строку
        formatted_report = ""
        
        # Добавление заголовка
        headers = " | ".join([str(col) for col in report.columns])
        formatted_report += f"{headers}\n"
        
        # Добавление разделителя между заголовком и данными
        formatted_report += "-" * len(headers) + "\n"
        
        for index, row in report.iterrows():
            formatted_row = " | ".join([str(val) for val in row.values])
            formatted_report += f"{formatted_row}\n"
        
        report_text.config(state="normal")
        report_text.delete("1.0", "end")
        report_text.insert("1.0", formatted_report)
        report_text.config(state="disabled")
        save_report_button.config(state="normal")

    def saveReport()->None:
        '''
        Сохраняет сводную таблицу в файл формата Excel.

        Returns
        -------
        None
            DESCRIPTION.

        '''
        default_filename = "Сводная таблица.xlsx" 
        file_path = filedialog.asksaveasfilename(initialdir=text_report_dir, defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=default_filename)
        if file_path:
            report.to_excel(file_path, index=False)
            messagebox.showinfo(f"Отчет сохранен в файл '{file_path}'")

    # Загрузка данных
    df_chasy = pd.read_pickle(df_chasy_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    df_prepodavateli = pd.read_pickle(df_prepodavateli_path)

    # Графический интерфейс
    window = tk.Toplevel()
    window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(window)

    header_frame = tk.Frame(window)
    header_frame.place(relwidth=1, relheight=0.1)
    apply_styles(header_frame, label_type="dark")    
    header_label = tk.Label(header_frame, text="Cводная таблица", height=2)
    header_label.place(relx=0.5, rely=0.5, anchor='center')    
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0,\
                               command=lambda: go_back(window))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")

    # Настройка шрифта для текста отчета
    text_font = font.Font(family="Courier", size=10)

    # Создание кнопки для генерации и отображения отчета
    generate_report_button = tk.Button(window, text="Создать отчет", command=display_report, bd=0, width=40, height=3)
    generate_report_button.pack(pady=(100,10))
    apply_styles(generate_report_button, label_type="violet")

    # Настройка текстового виджета для отображения отчета
    report_text = scrolledtext.ScrolledText(window, height=20, width=80, wrap="none", font=text_font)
    report_text.pack(pady=20)

    # Создание кнопки для сохранения отчета
    save_report_button = tk.Button(window, text="Сохранить отчет", command=saveReport, bd=0, width=40, height=3)
    save_report_button.pack(pady=10)
    save_report_button.config(state="disabled")
    apply_styles(save_report_button, label_type="normal")

def create_text_statistics(apply_styles)->None:
    '''
    Создает статистику часов преподавания по предметам и показывает ее в виде таблицы.

    Parameters
    ----------
    apply_styles : function
        Функция для применения стилей к виджетам.

    Returns
    -------
    None
    '''
    def calculateStatistics()->None:
        '''Вычисляет статистику по выбранному атрибуту и отображает ее.

       Returns
       -------
       None
       '''
        chosen_attribute = selected_attribute.get()
        
        if chosen_attribute == "Выберите атрибут":
            messagebox.showerror("Ошибка", "Выберите атрибут для статистики.")
            return

        merged_data = pd.merge(df_chasy, df_predmety, on='ID_ПРЕДМ')
        merged_data = pd.merge(merged_data, df_kursy_napravleniya, on='ID_КУРСА')
        merged_data = pd.merge(merged_data, df_prepodavateli, on='ID_ПРЕП')

        global statistics
        statistics = merged_data[chosen_attribute].describe().transpose()
        display_statistics(statistics)

    def display_statistics(statistics)->None:
        '''Отображает статистику в виде таблицы.

       Parameters
       ----------
       statistics : pd.Series
           Статистика для отображения.

       Returns
       -------
       None
       '''
        for widget in plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(facecolor='#BFDCFF')
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=statistics.values.reshape(1, -1), colLabels=statistics.index, cellLoc='center', loc='center')
        table.scale(1.2, 2)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for (i, label) in enumerate(statistics.index):
            cell = table[0, i]  # Получение конкретной ячейки заголовка
            cell.set_facecolor('#0D99FF')  # Установка синего цвета фона для заголовка
            cell.set_text_props(color='white')  # Установка белого цвета текста
            cell.set_fontsize(14)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        button_save.config(state="normal")
        
    def save_statistics(statistics)->None:
        '''Сохраняет статистику в файл Excel.

       Parameters
       ----------
       statistics : pd.Series
           Статистика для сохранения.
    
       Returns
       -------
       None
       '''
        default_filename="Статистический отчет.xlsx"
        file_path = filedialog.asksaveasfilename(initialdir=text_report_dir, defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=default_filename)
        if file_path:
            statistics.to_excel(file_path)
            messagebox.showinfo(f"Статистика сохранена в файл '{file_path}'")
            
    # Загрузка данных
    df_chasy = pd.read_pickle(df_chasy_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    df_kursy_napravleniya = pd.read_pickle(df_kursy_napravleniya_path)
    df_prepodavateli = pd.read_pickle(df_prepodavateli_path)

    # Графический интерфейс
    window = tk.Toplevel()
    window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(window)

    header_frame = tk.Frame(window)
    header_frame.place(relwidth=1, relheight=0.1)
    apply_styles(header_frame, label_type="dark")    

    header_label = tk.Label(header_frame, text="Статистический отчет", height=2)
    header_label.place(relx=0.5, rely=0.5, anchor='center')    
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0,\
                               command=lambda: go_back(window))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")
    
    
    button_save = tk.Button(header_frame, text="Сохранить", command=lambda: save_statistics(statistics), bd=0, width=10, height=2) 
    button_save.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, ipadx=100, ipady=10) 
    button_save.config(state="disabled")
    apply_styles(button_save, label_type="violet") 


    frame = tk.Frame(window, bg="#BFDCFF")
    frame.pack(pady=(100,10))
    apply_styles(frame, label_type="light")
    plot_frame = tk.Frame(window, bg="#BFDCFF")
    plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    apply_styles(plot_frame, label_type="light")

    selected_attribute = tk.StringVar(value="Выберите атрибут")

    possible_attributes = [
        "ID_ПРЕП",
        "ФАМ_ПРЕП",
        "ПОЧТА_ПРЕП",
        "ID_ПРЕДМ",
        "НАЗВ_ПРЕДМ",
        "ID_КУРСА",
        "НАПРАВ",
        "КУРС",
        "ЧАСЫ_НЕД"
    ]

    attribute_dropdown = tk.OptionMenu(frame, selected_attribute, *possible_attributes)
    attribute_dropdown.config(bg='#0D99FF', fg='white', width=40, height=3)
    attribute_dropdown.pack(pady=20)
    apply_styles(attribute_dropdown, label_type="normal")

    calculate_button = tk.Button(frame, text="Создать статистический отчет", command=calculateStatistics, bd=0, width=40, height=3)
    calculate_button.pack(pady=10)
    apply_styles(calculate_button, label_type="violet")

def create_frequency_report(apply_styles)->None:
    '''Создает отчет о частоте предметов и отображает его.
    
      Parameters
      ----------
      apply_styles : function
          Функция для применения стилей к виджетам.
    
      Returns
      -------
      None
      '''
    def generateSubjectHoursReport(df_predmety: pd.DataFrame, df_chasy: pd.DataFrame) -> pd.DataFrame:
        '''Создает отчет по часам предметов и проценту часов.
    
       Parameters
       ----------
       df_predmety : pd.DataFrame
           Данные о предметах.
       df_chasy : pd.DataFrame
           Данные о количестве часов.
    
       Returns
       -------
       pd.DataFrame
           Отчет по часам предметов и проценту часов.
       '''
        merged_df = df_predmety.merge(df_chasy.groupby('ID_ПРЕДМ').sum(), on='ID_ПРЕДМ')
        merged_df['ПРОЦ_ЧАС'] = (merged_df['ЧАСЫ_НЕД'] / merged_df['ЧАСЫ_НЕД'].sum()) * 100

        report = merged_df[['НАЗВ_ПРЕДМ', 'ЧАСЫ_НЕД', 'ПРОЦ_ЧАС']].copy()
        report.columns = ['Предметы', 'Количество учебных часов', 'Процент от общего количества часов']
        report['Процент от общего количества часов'] = report['Процент от общего количества часов'].map('{:.2f}%'.format)
        return report   

    def display_report()->None:
        '''Отображает отчет о часах предметов.

       Returns
       -------
       None
       '''
        global report
        report = generateSubjectHoursReport(df_predmety, df_chasy)
    
        # Форматирование данных в виде таблицы
        formatted_report = "{:<40}{:<30}{:<50}".format('Предметы', 'Количество учебных часов', 'Процент от общего количества часов') + "\n"
        for index, row in report.iterrows():
            formatted_report += "{:<40}{:<30}{:<50}".format(str(row['Предметы']), str(row['Количество учебных часов']), str(row['Процент от общего количества часов'])) + "\n"
    
        report_text.config(state="normal")
        report_text.delete("1.0", "end")
        report_text.insert("1.0", formatted_report)
        report_text.config(state="disabled")
        save_report_button.config(state="normal")

    def saveReport()->None:
        '''Сохраняет отчет о часах предметов в файл Excel.
    
       Returns
       -------
       None
       '''
        default_filename = "Отчет о частоте предметов.xlsx" 
        file_path = filedialog.asksaveasfilename(initialdir=text_report_dir, defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=default_filename)
        if file_path:
            report.to_excel(file_path, index=False)
            messagebox.showinfo(f"Отчет сохранен в файл '{file_path}'")
            
    # Загрузка данных
    df_chasy = pd.read_pickle(df_chasy_path)
    df_predmety = pd.read_pickle(df_predmety_path)

    # Графический интерфейс
    window = tk.Toplevel()
    window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(window)

    header_frame = tk.Frame(window)
    header_frame.place(relwidth=1, relheight=0.1)
    apply_styles(header_frame, label_type="dark")    

    header_label = tk.Label(header_frame, text="Отчет о частоте предметов", height=2)
    header_label.place(relx=0.5, rely=0.5, anchor='center')    
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, \
                            command=lambda: go_back(window))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")

    # Настройка шрифта для текста отчета
    text_font = font.Font(family="Courier", size=10)

    # Создание кнопки для генерации и отображения отчета
    generate_report_button = tk.Button(window, text="Создать отчёт о частоте предметов", command=display_report, bd=0, width=40, height=3)
    generate_report_button.pack(pady=(100, 10))
    apply_styles(generate_report_button, label_type="violet")

    # Настройка текстового виджета для отображения отчета
    report_text = scrolledtext.ScrolledText(window, height=20, width=80, wrap="none", font=text_font)
    report_text.pack(pady=20)

    # Создание кнопки для сохранения отчета, которая изначально неактивна
    save_report_button = tk.Button(window, text="Сохранить отчет", command=saveReport, bd=0, width=40, height=3)
    save_report_button.pack(pady=10)
    save_report_button.config(state="disabled")  # Делаем кнопку неактивной
    apply_styles(save_report_button, label_type="normal")

def create_simple_report(apply_styles)->None:
    '''Генерирует простой отчет на основе выбранных атрибутов и условий.

   Parameters
   ----------
   apply_styles : function
       Функция для применения стилей к виджетам.

   Returns
   -------
   None
   '''

    def generateSimpleReport(df_chasy: pd.DataFrame, df_prepodavateli: pd.DataFrame, df_predmety: pd.DataFrame, attributes: list, condition_column: str, condition_value: int):
        '''Генерирует простой отчет на основе выбранных атрибутов и условий.

       Parameters
       ----------
       df_chasy : pd.DataFrame
           Данные о часах.
       df_prepodavateli : pd.DataFrame
           Данные о преподавателях.
       df_predmety : pd.DataFrame
           Данные о предметах.
       attributes : list
           Список выбранных атрибутов для отчета.
       condition_column : str
           Название колонки для условия.
       condition_value : int
           Значение условия.
    
       Returns
       -------
       pd.DataFrame
           Результирующий отчет.
       '''

        global result_df
        df_all = df_chasy.merge(df_prepodavateli, on='ID_ПРЕП')
        df_all = df_all.merge(df_kursy_napravleniya, on='ID_КУРСА')
        df_all = df_all.merge(df_predmety, on='ID_ПРЕДМ')
        
        result_df = df_all[df_all[condition_column] == condition_value][attributes]
        result_df.drop_duplicates(keep='first', inplace=True)
        save_to_file_button.config(state="active")
        return result_df
        
    def toggle_attributes_menu()->None:
        '''Переключает видимость меню выбора атрибутов.
    
       Returns
       -------
       None
       '''

        if attributes_menu.winfo_ismapped():
            attributes_menu.pack_forget()
            label_condition.pack_forget()
            attribute_dropdown.pack_forget()
            label_value.pack_forget()
            condition_dropdown.pack_forget()

        else:
            attributes_menu.pack()
            label_condition.pack()
            attribute_dropdown.pack()
            label_value.pack()
            condition_dropdown.pack()
            # save_button.config(state="active")
            plot_frame.pack_forget()
            save_to_file_button.config(state="disabled")

    def save_selection()->None:
        '''Сохраняет выбор атрибутов и генерирует отчет.
    
       Returns
       -------
       None
       '''
        selected_attrs = [attr.cget("text") for attr in attributes_checkboxes if attr.var.get() == 1]
        if selected_attrs:
            selected_option = attribute_dropdown_var.get()
            selected_condition = int(condition_dropdown_var.get())

            result_df = generateSimpleReport(df_chasy, df_prepodavateli, df_predmety, selected_attrs, selected_option, selected_condition)
            display_table(result_df)

            attributes_menu.pack_forget()
            label_condition.pack_forget()
            attribute_dropdown.pack_forget()
            label_value.pack_forget()
            condition_dropdown.pack_forget()
            plot_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    def display_table(dataframe)->None:
        '''Отображает таблицу с данными.
    
       Parameters
       ----------
       dataframe : pd.DataFrame
           Данные для отображения.
    
       Returns
       -------
       None
       '''
        for widget in plot_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(facecolor='#BFDCFF')
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')
        table.scale(1.2, 2)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for (i, label) in enumerate(dataframe.columns):
            cell = table[0, i]  # Получение конкретной ячейки заголовка
            cell.set_facecolor('#0D99FF')  # Установка синего цвета фона для заголовка
            cell.set_text_props(color='white')  # Установка белого цвета текста
            cell.set_fontsize(14)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_to_file():
        '''Сохраняет отчет в файл Excel.
    
      Returns
      -------
      None
      '''
        global result_df 
        default_filename = "Простой текстовый отчет.xlsx" 
        file_path = filedialog.asksaveasfilename(initialdir=text_report_dir, defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=default_filename)
        if file_path:
            result_df.to_excel(file_path, index=False)
            print("Файл успешно сохранен:", file_path)
            
    def on_condition_select(*args)->None:
        '''Обрабатывает событие выбора значения условия.
    
      Returns
      -------
      None
      '''
        selected_condition = condition_dropdown_var.get()
        if selected_condition:  # Проверка выбора значения, активация кнопки "Готово" если выбрано значение
            save_button.config(state="active")

    def update_condition_values(*args)->None:
        '''Обновляет выпадающий список значений условия.
    
       Returns
       -------
       None
       '''
        selected_option = attribute_dropdown_var.get()
        condition_dropdown['menu'].delete(0, 'end')
        if selected_option in condition_options:
            for option in condition_options[selected_option]:
                condition_dropdown['menu'].add_command(label=option, command=lambda value=option: condition_dropdown_var.set(value))

    df_chasy = pd.read_pickle(df_chasy_path)
    df_prepodavateli = pd.read_pickle(df_prepodavateli_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    df_kursy_napravleniya = pd.read_pickle((df_kursy_napravleniya_path))
    result_df = None
    window = tk.Toplevel()
    window.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(window)

    header_frame = tk.Frame(window)
    header_frame.place(relwidth=1, relheight=0.1)
    apply_styles(header_frame, label_type="dark")    

    header_label = tk.Label(header_frame, text="Простой текстовый отчет", height=2)
    header_label.place(relx=0.5, rely=0.5, anchor='center')    
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0,\
                                command=lambda: go_back(window))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")

    frame = tk.Frame(window)
    frame.pack(pady=(100,10))
    apply_styles(frame, label_type="light")
    plot_frame = tk.Frame(window)
    apply_styles(plot_frame, label_type="light")

    attributes_menu = tk.Frame(window)
    apply_styles(attributes_menu, label_type="light")
    attributes_list = ["ID_ПРЕП", "ФАМ_ПРЕП", "ПОЧТА_ПРЕП", "ID_ПРЕДМ", "НАЗВ_ПРЕДМ", "ID_КУРСА", "НАПРАВ", "КУРС", "ЧАСЫ_НЕД"]
    integer_attributes_list = ["ID_ПРЕП", "ID_ПРЕДМ", "ID_КУРСА","КУРС", "ЧАСЫ_НЕД"]
    attributes_checkboxes = []
    for attr in attributes_list:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(attributes_menu, text=attr, variable=var)
        checkbox.var = var
        attributes_checkboxes.append(checkbox)
        checkbox.pack(anchor="w")
        # apply_styles(checkbox)

    choose_attributes_button = tk.Button(frame, text="Выбрать атрибуты", bd=0, command=toggle_attributes_menu)
    choose_attributes_button.pack(side=tk.LEFT, padx=40, pady=(20, 0))
    apply_styles(choose_attributes_button, label_type="normal")

    save_button = tk.Button(frame, text="Готово", state='disabled', bd=0, command=save_selection)
    save_button.pack(side=tk.LEFT, padx=40, pady=(20, 0))
    apply_styles(save_button, label_type="violet")

    save_to_file_button = tk.Button(frame, text="Сохранить в файл", bd=0, state="disabled", command=save_to_file)
    save_to_file_button.pack(side=tk.LEFT, padx=40, pady=(20, 0))
    apply_styles(save_to_file_button, label_type="violet")

    condition_options = {
        "ID_ПРЕП": [*set(df_chasy['ID_ПРЕП'])],
        "ID_ПРЕДМ": [*set(df_chasy['ID_ПРЕДМ'])],
        "ID_КУРСА": [*set(df_chasy['ID_КУРСА'])],
        "КУРС": [*set(df_kursy_napravleniya['КУРС'])],
        "ЧАСЫ_НЕД": [*set(df_chasy['ЧАСЫ_НЕД'])]
    }

    attribute_dropdown_var = tk.StringVar()
    label_condition = tk.Label(attributes_menu, text="Добавить условие:")
    label_condition.pack()
    apply_styles(label_condition, label_type="type1")
    attribute_dropdown = tk.OptionMenu(attributes_menu, attribute_dropdown_var, *integer_attributes_list)
    attribute_dropdown.pack()
    apply_styles(attribute_dropdown, label_type="normal")

    condition_dropdown_var = tk.StringVar()
    label_value = tk.Label(attributes_menu, text="Значение условия:")
    label_value.pack()
    apply_styles(label_value, label_type="type1")
    condition_dropdown = tk.OptionMenu(attributes_menu, condition_dropdown_var, ())
    apply_styles(condition_dropdown, label_type="normal")
    attribute_dropdown_var.trace_add('write', update_condition_values)
    condition_dropdown_var.trace_add('write', on_condition_select)

# Графические отчеты
def create_boxwhisker_diagram(apply_styles)->None:
    '''Создает диаграмму box-whisker и отображает ее в графическом интерфейсе.
    
      Parameters
      ----------
      apply_styles : function
          Функция для применения стилей к виджетам.
    
      Returns
      -------
      None
    '''
    df_chasy = pd.read_pickle(df_chasy_path)
    df_predmety = pd.read_pickle(df_predmety_path)

    fig = diag_box_whisker(df_chasy, df_predmety)

    root = tk.Toplevel() 
    root.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))

    apply_styles(root)
    header_frame = tk.Frame(root)
    header_frame.place(relwidth=1, relheight=0.1)
    apply_styles(header_frame, label_type="dark")
    
    header_label = tk.Label(header_frame,\
                            text="Статистика часов преподавания по предметам")
    header_label.place(relx=0.5, rely=0.5, anchor='center')    
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0,\
                                command=lambda: go_back(root))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")
    
    button_save = tk.Button(header_frame, text="Сохранить", command=lambda: save_plot(fig), bd=0, width=10, height=2)
    button_save.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, ipadx=100, ipady=10) 
    apply_styles(button_save, label_type="violet")
    
    canvas_width = root.winfo_screenwidth()
    canvas_height = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (canvas_width, canvas_height))
    
    figure_frame = tk.Frame(root)
    figure_frame.pack(pady=(100,10))
    apply_styles(figure_frame, label_type="light")

    plot_canvas = FigureCanvasTkAgg(fig, master=figure_frame)
    plot_canvas.get_tk_widget().pack(expand=True, fill='both')

    
def create_scatter_plot(apply_styles)->None:
    '''Создает график рассеивания для часов в неделю в зависимости от курса.

      Parameters
      ----------
      apply_styles : function
          Функция для применения стилей к виджетам.
    
      Returns
      -------
      None
      '''
    df_chasy = pd.read_pickle(df_chasy_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    
    fig = create_scatter_plot_backend(df_chasy, df_predmety)
    
    root = tk.Toplevel()
    root.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(root)
    
    header_frame = tk.Frame(root)
    header_frame.place(relwidth=1, relheight=0.1)  # Покрывает всю ширину окна
    apply_styles(header_frame, label_type="dark")

    header_label = tk.Label(header_frame, text="Распределение часов в неделю в зависимости от курса")
    header_label.place(relx=0.5, rely=0.5, anchor='center')
    apply_styles(header_label, label_type="type2")
    
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, command=lambda: go_back(root))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")
    
    button_save = tk.Button(header_frame, text="Сохранить", command=lambda: save_plot(fig), bd=0, width=10, height=2)
    button_save.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, ipadx=100, ipady=10) 
    apply_styles(button_save, label_type="violet")

    canvas_width = root.winfo_screenwidth()
    canvas_height = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (canvas_width, canvas_height))

    figure_frame = tk.Frame(root)
    figure_frame.pack(pady=(100,10))
    apply_styles(figure_frame, label_type="light")

    canvas = FigureCanvasTkAgg(fig, master=figure_frame)
    canvas.get_tk_widget().pack(expand=True, fill='both')

    
def create_bar_chart(apply_styles)->None:
    '''Создает столбчатую диаграмму для часов в неделю по предметам для каждого преподавателя.

   Parameters
   ----------
   apply_styles : function
       Функция для применения стилей к виджетам.

   Returns
   -------
   None
   '''
    df_chasy = pd.read_pickle(df_chasy_path)
    df_prepodavateli = pd.read_pickle(df_prepodavateli_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    
    fig = create_сlustered_bar_chart(df_prepodavateli, df_predmety, df_chasy)
    
    root = tk.Toplevel()
    root.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(root)
    
    header_frame = tk.Frame(root)
    header_frame.place(relwidth=1, relheight=0.1)  # Покрывает всю ширину окна
    apply_styles(header_frame, label_type="dark")

    header_label = tk.Label(header_frame, text="Распределение часов в неделю по предметам для каждого преподавателя")
    header_label.place(relx=0.5, rely=0.5, anchor='center')
    apply_styles(header_label, label_type="type2")
    
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, command=lambda: go_back(root))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")
    
    button_save = tk.Button(header_frame, text="Сохранить", command=lambda: save_plot(fig), bd=0, width=10, height=2)
    button_save.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, ipadx=100, ipady=10) 
    apply_styles(button_save, label_type="violet")

    canvas_width = root.winfo_screenwidth()
    canvas_height = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (canvas_width, canvas_height))

    figure_frame = tk.Frame(root)
    figure_frame.pack(pady=(100,10))
    apply_styles(figure_frame, label_type="light")

    canvas = FigureCanvasTkAgg(fig, master=figure_frame)
    canvas.get_tk_widget().pack(expand=True, fill='both')
 
    
def create_categorize_gist(apply_styles)->None:
    '''Создает категоризированную гистограмму для распределения часов по предметам.

   Parameters
   ----------
   apply_styles : function
       Функция для применения стилей к виджетам.

   Returns
   -------
   None
   '''
    df_chasy = pd.read_pickle(df_chasy_path)
    df_prepodavateli = pd.read_pickle(df_prepodavateli_path)
    df_predmety = pd.read_pickle(df_predmety_path)
    fig = categorize_gist(df_chasy, df_prepodavateli, df_predmety)

    root = tk.Toplevel()
    root.minsize(width=int(config.get('Settings', 'window_width')), height=int(config.get('Settings', 'window_height')))
    apply_styles(root)
    
    header_frame = tk.Frame(root)
    header_frame.place(relwidth=1, relheight=0.1)  # Покрывает всю ширину окна
    apply_styles(header_frame, label_type="dark")

    header_label = tk.Label(header_frame, text="Распределение количества отработанных часов по предметам")
    header_label.place(relx=0.5, rely=0.5, anchor='center')
    apply_styles(header_label, label_type="type2")
    
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, command=lambda: go_back(root))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type="normal")
    
    button_save = tk.Button(header_frame, text="Сохранить", command=lambda: save_plot(fig), bd=0, width=5, height=2)
    button_save.pack(side=tk.RIGHT, anchor='ne', padx=20, pady=10, ipadx=100, ipady=10) 
    apply_styles(button_save, label_type="violet")

    figure_frame = tk.Frame(root)
    figure_frame.pack(pady=(100,10))
    apply_styles(figure_frame, label_type="light")

    canvas = FigureCanvasTkAgg(fig, master=figure_frame)
    canvas.get_tk_widget().pack(expand=True, fill='both')


# Создание текстовых отчетов
def pivotTable(df_chasy: pd.DataFrame, df_prepodavateli: pd.DataFrame, df_predmety: pd.DataFrame)->pd.DataFrame:
    """
    Составляет сводную таблицу, отображающую преподавателей, предметы и сумму 
    часов каждого преподавателя по каждому преподаваемому им предмету;
    сохраняет её в файл pivot_table.xlsx

    Parameters
    ----------
    df_chasy : pd.DataFrame
       Таблица, содержащая соотношения часов, отведенных каждый преподавателем
       для каждой группы.
    df_prepodavateli : pd.DataFrame
        Таблица, содержащая соотношения информации о преподавателях.
    df_predmety : pd.DataFrame
        Таблица, содержащая информацию о предметах.
        
    Returns
    -------
    None

    """
    merged_data = pd.merge(df_chasy, df_prepodavateli, on='ID_ПРЕП')
    merged_data = pd.merge(merged_data, df_predmety, on='ID_ПРЕДМ')
    pivot_table = merged_data.pivot_table(index=['ID_ПРЕП', 'ФАМ_ПРЕП'],
                                          columns='НАЗВ_ПРЕДМ',
                                          values='ЧАСЫ_НЕД',
                                          aggfunc='sum',
                                          fill_value=0)

    filtered_pivot_table = pivot_table.stack().reset_index(name='ЧАСЫ_НЕД')
    filtered_df = filtered_pivot_table [filtered_pivot_table ['ЧАСЫ_НЕД'] != 0]
    return filtered_df

# Создание графических отчетов

def diag_box_whisker(df_chasy: pd.DataFrame, df_predmety: pd.DataFrame) -> plt.Figure:
    """
    Создает категоризированную диаграмму Бокса-Вискера для 
    статистики часов преподавания по предметам и загружает ее в файл 
    boxwhisker_diagram.jpg
    
    Parameters
    ----------
    df_chasy : pd.DataFrame
        Таблица, содержащая соотношения часов, отведенных каждый преподавателем
        для каждой группы.
    df_predmety : pd.DataFrame
        Таблица, содержащая информацию о предметах.

    Returns
    -------
    fig : plt.Figure
        Объект графика.
    """
    df_merged = pd.merge(df_chasy, df_predmety, on='ID_ПРЕДМ').loc[:, ['ЧАСЫ_НЕД', 'НАЗВ_ПРЕДМ']]
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111)
    df_merged.boxplot(column='ЧАСЫ_НЕД', by='НАЗВ_ПРЕДМ', patch_artist=True, ax=ax)
    fig.suptitle('')
    plt.title('Категоризированная диаграмма Бокса-Вискера для статистики часов преподавания по предметам')
    plt.ylabel('Часы преподавания')
    plt.xlabel('Предметы')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Изменение названий предметов
    labels = []
    for tick in ax.get_xticklabels():
        words = tick.get_text().split()  # Разделение на слова
        modified_label = '\n'.join(words)  # Объединение слов с использованием символа новой строки
        labels.append(modified_label)

    # Устанавливаем новые значения название предметов
    ax.set_xticklabels(labels)

    return fig

def create_scatter_plot_backend(df_chasy: pd.DataFrame, df_predmety: pd.DataFrame)->plt.Figure:
    """
    Создает категоризованную диаграмму рассеивания, которая показывает предмет в зависимости от
    курса+направления (например, ИВТ 1 курс или ИБ 2 курс и количества часов 
    (нагрузки) и загружает ее в файл scatter_plot_with_legend.jpg.

    Parameters
    ----------
    df_chasy : pd.DataFrame
        Таблица, содержащая соотношения часов, отведенных каждый преподавателем
        для каждой группы.
    df_predmety : pd.DataFrame
        Таблица, содержащая информацию о предметах.
        
    Returns
    -------
    fig : plt.Figure
        Объект графика. 
    """

    df_chasy_selected = df_chasy[['ID_КУРСА', 'ЧАСЫ_НЕД', 'ID_ПРЕДМ']]
    df_predmety_selected = df_predmety[['ID_ПРЕДМ', 'НАЗВ_ПРЕДМ']]

    merged_table = pd.merge(df_chasy_selected, df_predmety_selected, on='ID_ПРЕДМ')

    fig, ax = plt.subplots(figsize=(18, 8))  # Увеличение ширины графика
    plt.subplots_adjust(right=0.8)

    for subject in merged_table['НАЗВ_ПРЕДМ'].unique():
        data = merged_table[merged_table['НАЗВ_ПРЕДМ'] == subject]
        ax.scatter(data['ЧАСЫ_НЕД'], data['ID_КУРСА'], label=subject)

    ax.set_xlabel('Количество часов')
    ax.set_ylabel('ID_КУРСА')
    ax.set_title('Распределение часов в неделю по предмету в зависимости от курса')
    ax.legend(title='Название предмета', loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True)

    return fig

def create_сlustered_bar_chart(df_prepodavateli: pd.DataFrame, df_predmety: pd.DataFrame, df_chasy: pd.DataFrame)->plt.Figure:
    """
    Создает кластеризованную столбчатую диаграмму, отображающую распределение 
    часов в неделю по предметам для каждого преподавателя и загружает ее в файл
    clustered_bar_chart.jpg
    
    Parameters
    ----------
    df_prepodavateli : pd.DataFrame
        Таблица, содержащая соотношения информации о преподавателях.
    df_predmety : pd.DataFrame
        Таблица, содержащая информацию о предметах.
    df_chasy : pd.DataFrame
        Таблица, содержащая соотношения часов, отведенных каждый преподавателем
        для каждой группы.

    Returns
    -------
    fig : plt.Figure
       Объект графика.

    """
    merged_data = pd.merge(df_prepodavateli, pd.merge(df_predmety,df_chasy, on='ID_ПРЕДМ'), on='ID_ПРЕП')
    teacher_subject_hours = merged_data.groupby(['ФАМ_ПРЕП', 'НАЗВ_ПРЕДМ'])['ЧАСЫ_НЕД'].sum().unstack()

    fig, ax_1 = plt.subplots(figsize=(16, 8))
    teacher_subject_hours.plot(kind='bar', stacked=False, width=0.8, ax=ax_1)
    
    ax_1.set_xlabel('Преподаватель', fontsize=20) 
    ax_1.set_ylabel('Часы в неделю', fontsize=20) 
    ax_1.set_title('Распределение часов в неделю по предметам для каждого преподавателя', fontsize=20) 
    ax_1.legend(title='Предмет', title_fontsize=16, fontsize=14, bbox_to_anchor=(1, 1))

    plt.xticks(rotation=90, fontsize=16)
    plt.tight_layout()
    
    return fig

def categorize_gist(df_chasy: pd.DataFrame, df_prepodavateli: pd.DataFrame, df_predmety: pd.DataFrame)->plt.Figure:
    """
    Создает категоризованную гистограмму, отображающую распределение количества 
    отработанных часов по разным предметам и возвращает ее.

    Parameters
    ----------
    df_chasy : pd.DataFrame
       Таблица, содержащая соотношения часов, отведенных каждый преподавателем
       для каждой группы.
    df_prepodavateli : pd.DataFrame
        Таблица, содержащая соотношения информации о преподавателях.
    df_predmety : pd.DataFrame
        Таблица, содержащая информацию о предметах.

    Returns
    -------
    fig : plt.Figure
        Объект графика.

    """
    merged_data = pd.merge(df_chasy, df_prepodavateli, on='ID_ПРЕП')
    merged_data = pd.merge(merged_data, df_predmety, on='ID_ПРЕДМ')

    quantitative_attr = 'ЧАСЫ_НЕД'
    qualitative_attr = 'НАЗВ_ПРЕДМ'

    fig, ax_1 = plt.subplots(figsize=(18, 8))
    for category in merged_data[qualitative_attr].unique():
        ax_1.hist(merged_data.loc[merged_data[qualitative_attr] == category, quantitative_attr], label=category, alpha=0.5)

    ax_1.set_xlabel('Количество часов')
    ax_1.set_ylabel('Частота')
    ax_1.set_title('Категоризированная гистограмма, показывающая распределение количества отработанных часов по разным предметам')
    ax_1.legend()
    ax_1.grid(True)

    return fig

