import tkinter as tk
from tkinter import filedialog
import os
import pickle
import configparser
from pandastable import Table
import pandas as pd

def go_back(report_window)->None:
    '''Закрывает окно отчетов.

   Parameters
   ----------
   report_window : tk.Toplevel
       Окно отчетов.

   Returns
   -------
   None
   '''
    report_window.destroy()  

def upload_files(apply_styles)->None:
    '''Открывает окно для загрузки файлов и сохранения их в формате pickle.
    
      Parameters
      ----------
      apply_styles : function
          Функция для применения стилей к виджетам.
    
      Returns
      -------
      None
      '''
    root = tk.Toplevel()
    root.title("Загрузка файлов")
    apply_styles(root)

    files = ["", "", "", ""]

    header_frame = tk.Frame(root)
    header_frame.place(relwidth=1, relheight=0.1)  # Покрывает всю ширину окна
    apply_styles(header_frame, label_type='dark')

    header_label = tk.Label(header_frame, text="Загрузка данных")
    header_label.place(relx=0.5, rely=0.5, anchor='center')
    apply_styles(header_label, label_type="type2")
    back_button = tk.Button(header_frame, text="НАЗАД", bd=0, \
                                command=lambda: go_back(root))
    back_button.place(relx=0.02, rely=0.5, anchor='w')
    apply_styles(back_button, label_type='normal')
    
    def choose_file(index)->None:
        '''Позволяет выбрать файл и обновляет соответствующие элементы интерфейса.
    
       Parameters
       ----------
       index : int
           Индекс файла в списке файлов.
    
       Returns
       -------
       None
       '''
        file_types = [("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("CSV files", "*.csv"), ("Pickle files", "*.pkl")]
        file = filedialog.askopenfilename(filetypes=file_types)
        if file:
            files[index] = file
            browse_buttons[index].config(state=tk.ACTIVE)
            file_labels[index].config(text=os.path.basename(file))

        # Проверяем, все ли файлы уже загружены
        if all(files):
            save_button.config(state=tk.NORMAL)
            
    def browse_file(index)->None:
        '''Открывает выбранный файл для просмотра и редактирования.
    
       Parameters
       ----------
       index : int
           Индекс файла в списке файлов.
    
       Returns
       -------
       None
       '''
        file = files[index]
        if file:
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file, encoding='utf-8')
                elif file.endswith('.xlsx') or file.endswith('.xls'):
                    df = pd.read_excel(file)
                elif file.endswith('.pkl'):
                    with open(file, 'rb') as f:
                        df = pickle.load(f)
                else:
                    print("Неподдерживаемый формат файла")
                    return


                table_viewer = tk.Toplevel(root)
                table_viewer.title("Просмотр")
                table_viewer.configure(bg="light blue")
                apply_styles(table_viewer)

                table_label = tk.Label(table_viewer, text="Редактирование", height=3)
                table_label.pack(fill="x", pady=(0, 50))
                apply_styles(table_label, label_type="type2")
                
                table_frame = tk.Frame(table_viewer)
                table_frame.pack(pady=50)
                apply_styles(table_frame)
                
                pt = Table(table_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
                pt.width = 1000  # Задаем ширину таблицы
                pt.height = 600  # Задаем высоту таблицы
                pt.show()

                def save_changes()->None:
                    '''Сохраняет внесенные изменения в файл.
                    
                      Returns
                      -------
                      None
                    '''
                    try:
                        data = pt.model.df  # Получаем данные из таблицы tkinter
                        df_updated = pd.DataFrame(data)  # Преобразуем данные в DataFrame

                        if file.endswith('.csv'):
                            df_updated.to_csv(file, index=False, encoding='utf-8')
                        elif file.endswith('.xlsx') or file.endswith('.xls'):
                            df_updated.to_excel(file, index=False, engine='openpyxl')
                        else:
                            print("Неподдерживаемый формат файла для сохранения изменений")
                            return

                        print("Изменения сохранены успешно")
                        table_viewer.destroy()
                    except Exception as exc:
                        print(f"Ошибка при сохранении изменений: {exc}")

                save_button = tk.Button(table_viewer, text="Сохранить", bg="violet", fg="#9747FF", command=save_changes)
                save_button.pack(side=tk.RIGHT, padx=10)
                apply_styles(save_button, label_type='violet')
                table_viewer.minsize(400, 300)

            except Exception as exc:
                print(f"Ошибка при чтении файла: {exc}")


    file_labels = []
    browse_buttons = []
    text_label = tk.Label(root, text="Загрузка файлов форматов .xls/.xlsx/.csv/.pkl", bg="light blue", fg="black", font=("Arial", 24))
    text_label.pack(pady=(100,10))
    apply_styles(text_label, label_type="type1")
    
    def save_files()->None: 
        '''Сохраняет загруженные файлы в формате pickle. 
 
        Returns 
        ------- 
        None
        '''
        config = configparser.ConfigParser() 
        config.read('config.ini') 
        folder_path = config['Settings']['data_folder'] 
        if not os.path.exists(folder_path): 
            os.makedirs(folder_path) 
 
        file_names = ["df_prepodavateli.pkl", "df_predmety.pkl", "df_kursy_napravleniya.pkl", "df_chasy.pkl"] 
 
        for i, file_path in enumerate(files): 
            if file_path: 
                if file_path.endswith('.csv'): 
                    d_f = pd.read_csv(file_path, encoding='utf-8') 
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'): 
                    d_f = pd.read_excel(file_path) 
                else: 
                    print("Неподдерживаемый формат файла") 
                    continue 
 
                destination = os.path.join(folder_path, file_names[i]) 
                with open(destination, 'wb') as file: 
                    pickle.dump(d_f, file) 
 
        print("Файлы сохранены в папке 'data' в формате pickle")
    
    
    for i, label_text in enumerate(["Преподаватели", "Предметы", "Курсы", "Часы"]):
        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, padx=100)
        apply_styles(frame, label_type='light')

        text_label = tk.Label(frame, text=label_text)
        text_label.pack(pady=5)
        apply_styles(text_label, label_type="type1")

        file_labels.append(tk.Label(frame, text="Файл не выбран"))
        file_labels[i].pack()
        apply_styles(file_labels[i], label_type='type1')

        upload_button = tk.Button(frame, text="Выбрать файл", command=lambda i=i: choose_file(i))
        upload_button.pack(pady=5)
        apply_styles(upload_button, label_type='violet')

        browse_button = tk.Button(frame, text="Посмотреть", state=tk.DISABLED, command=lambda i=i: browse_file(i))
        browse_buttons.append(browse_button)
        browse_button.pack(pady=5)
        apply_styles(browse_button, label_type='violet')

    button_frame = tk.Frame(root)
    button_frame.place(relx=0.5, rely=0.95, anchor='center')
    apply_styles(button_frame)
 
    save_button = tk.Button(button_frame, text="Готово", command=save_files, state=tk.DISABLED)
    save_button.pack()
    apply_styles(save_button, label_type='violet')
