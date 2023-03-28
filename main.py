import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import math
import pandas as pd
import matplotlib.pyplot as plt


# import numpy as np
# import math as mt


class CreatePlot:
    def __init__(self):

        self.l_y_range = None
        self.l_x_range = None
        self.y_min = None
        self.y_max = None
        self.x_min = None
        self.x_max = None
        self.arr_y = None
        self.arr_x = None
        self.b_show_graph = None
        self.l_y_var = None
        self.l_x_var = None
        self.lb_x_var = None
        self.lb_y_var = None
        self.progress_max = None
        self.DELIMITER = None
        self.b_get_list_var = None
        self.b_select_source_file = None
        self.e_source_file = None
        self.SOURCE_FILE = None
        self.l_source_file = None
        self.MAIN_WIN_MENU = None
        self.GRAPH_MAIN_WIN = None
        self.HIGH_GRAPH_MAIN_WIN = 400
        self.WEIGHT_GRAPH_MAIN_WIN = 600
        self.LABEL_GRAPH_WIN = 'Print graph'
        self.create_graph_win()

    def create_graph_win(self):
        self.GRAPH_MAIN_WIN = tk.Tk()
        self.GRAPH_MAIN_WIN.geometry(
            f"{self.WEIGHT_GRAPH_MAIN_WIN}x{self.HIGH_GRAPH_MAIN_WIN}+"
            f"{int(1920 / 2 - (self.WEIGHT_GRAPH_MAIN_WIN / 2))}+{int((1080 / 2) - (self.HIGH_GRAPH_MAIN_WIN / 2))}")

        self.GRAPH_MAIN_WIN.title(self.LABEL_GRAPH_WIN)
        for i in range(self.HIGH_GRAPH_MAIN_WIN // 25):
            self.GRAPH_MAIN_WIN.grid_columnconfigure(i, minsize=25)

        for i in range(self.WEIGHT_GRAPH_MAIN_WIN // 25):
            self.GRAPH_MAIN_WIN.grid_rowconfigure(i, minsize=25)

        self.create_label()
        self.create_button()
        self.create_entry()
        self.create_listbox()

        self.create_menu_graph()

        self.GRAPH_MAIN_WIN.mainloop()

    def create_label(self):
        self.l_source_file = tk.Label(self.GRAPH_MAIN_WIN, text='Исходный файл', font="Arial 12")
        self.l_source_file.grid(column=0, row=0, sticky="w", padx=10, pady=10)

        self.l_x_var = tk.Label(self.GRAPH_MAIN_WIN, text='X:', font="Arial 12")
        self.l_x_var.place(x=5, y=90)

        self.l_y_var = tk.Label(self.GRAPH_MAIN_WIN, text='Y:', font="Arial 12")
        self.l_y_var.place(x=300, y=90)

        self.l_x_range = tk.Label(self.GRAPH_MAIN_WIN, text=f'X: {self.x_min} - {self.x_max}', font="Arial 12")
        self.l_x_range.place(x=5, y=170)

        self.l_y_range = tk.Label(self.GRAPH_MAIN_WIN, text=f'Y: {self.y_min} - {self.y_max}', font="Arial 12")
        self.l_y_range.place(x=300, y=170)

    def create_button(self):
        self.b_select_source_file = tk.Button(self.GRAPH_MAIN_WIN, text="Обзор",
                                              command=lambda: self.get_file(self.e_source_file))
        self.b_select_source_file.grid(column=16, row=0, sticky="we", padx=10)

        self.b_show_graph = tk.Button(self.GRAPH_MAIN_WIN, text="Построить график",
                                      command=lambda: self.show_plot())
        self.b_show_graph.place(x=240, y=300)

    def create_listbox(self):
        self.lb_x_var = tk.Listbox(self.GRAPH_MAIN_WIN, selectmode="single", width=40, height=5, exportselection=0)
        self.lb_x_var.place(x=30, y=60)

        self.lb_y_var = tk.Listbox(self.GRAPH_MAIN_WIN, selectmode="single", width=40, height=5, exportselection=0)
        self.lb_y_var.place(x=325, y=60)

    def create_entry(self):
        self.e_source_file = tk.Entry(self.GRAPH_MAIN_WIN, textvariable=self.SOURCE_FILE)
        self.e_source_file.grid(column=1, row=0, columnspan=15, sticky="we", padx=10)
        self.e_source_file.delete(0, tk.END)

    def show_plot(self):
        pos_x = 0
        pos_y = 0
        x_var = CreatePlot.get_list_of_choice_var(self.lb_x_var)
        y_var = CreatePlot.get_list_of_choice_var(self.lb_y_var)
        file = open(self.SOURCE_FILE, 'r')
        read_str = file.readline()
        read_str = str.split(read_str, self.DELIMITER)

        for el in range(len(read_str)):
            if str(read_str[el]) == str(x_var[0]):
                pos_x = el

        for el in range(len(read_str)):
            if str(read_str[el]) == str(y_var[0]):
                pos_y = el
        self.arr_x = []
        self.arr_y = []
        for el in file:
            el = str.split(el, self.DELIMITER)
            self.arr_x.append(float(el[pos_x]))
            self.arr_y.append(float(el[pos_y]))
        self.x_max = max(self.arr_x, default=None)
        self.x_min = min(self.arr_x, default=None)
        self.y_max = max(self.arr_y, default=None)
        self.y_min = min(self.arr_y, default=None)

        self.l_x_range.config(text=f'X: {self.x_min} - {self.x_max}')
        self.l_y_range.config(text=f'Y: {self.y_min} - {self.y_max}')
        plt.title(self.SOURCE_FILE)

        plt.xlabel(str(x_var[0]))
        plt.ylabel(str(y_var[0]))
        plt.grid(visible=True, axis='both')
        plt.plot(self.arr_x, self.arr_y, label=str(y_var[0]))
        plt.legend('labels')
        plt.show()

    def create_menu_graph(self):
        self.MAIN_WIN_MENU = tk.Menu(self.GRAPH_MAIN_WIN)
        self.GRAPH_MAIN_WIN.config(menu=self.MAIN_WIN_MENU)
        self.MAIN_WIN_MENU.add_command(label="Перезапустить", command=lambda: reboot_graph_win(self))
        self.MAIN_WIN_MENU.add_command(label="Конвертация файлов", command=lambda: create_conv_win(self))

    def get_file(self, entry: tk.Entry):
        filetypes = (("Таблица", "*.csv"),
                     ("Текстовый файл", "*.txt"),
                     ("Любой", "*"))

        filename = fd.askopenfilename(title="Выбрать файл", initialdir="C:/Users/Equint/Desktop/",
                                      filetypes=filetypes)
        if filename:
            self.SOURCE_FILE = filename
            self.get_list_of_var()

            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def get_list_of_var(self):
        count_str = 0
        tmp_list = []
        data1 = []
        self.get_delimiter()

        file = open(self.SOURCE_FILE, 'r')
        read_str = file.readline()
        count_str += 1
        spl_str = str.split(read_str, self.DELIMITER)
        for el in spl_str:
            tmp_list.append(el)

        for _ in file:
            count_str += 1

        list_of_variable = set(tmp_list)
        file.close()
        data1.extend(list_of_variable)
        data1.sort()

        self.progress_max = count_str
        if len(data1):
            for i in data1:
                self.lb_x_var.insert(0, i)
                self.lb_y_var.insert(0, i)
        else:
            return

    def get_delimiter(self):
        file = open(self.SOURCE_FILE, 'r')
        read_str = file.readline()
        file.close()
        num_pole1 = len(str.split(read_str, ';'))
        num_pole2 = len(str.split(read_str, ','))
        if num_pole1 > num_pole2:
            self.DELIMITER = ';'
        else:
            self.DELIMITER = ','

    @staticmethod
    def get_list_of_choice_var(list_box: tk.Listbox):
        choice_var = []
        choice_list = list_box.curselection()
        for i in choice_list:
            op = list_box.get(i)
            choice_var.append(op)
        return choice_var


class ConvertLogFile:

    def __init__(self):

        self.CONV_MAIN_WIN = tk.Tk()
        self.HIGH_CONV_MAIN_WIN = 350
        self.WEIGHT_CONV_MAIN_WIN = 700
        self.LABEL_CONV_WIN = 'Converting log files WinCC'

        self.setting_check_data_omissions = None
        self.cb_check_data_omissions = None
        self.v_check_data_omissions = tk.IntVar()
        self.MAIN_WIN_MENU = None
        self.end_file: str = ''
        self.l_progress = None
        self.v_add_counter = tk.IntVar()
        self.v_use_sys_time = tk.IntVar()
        self.setting_add_counter = False
        self.setting_use_sys_time = False
        self.cb_add_record_counter = None
        self.cb_sys_time = None
        self.l_settings = None
        self.progress_step = None
        self.progress_value = None
        self.progress_max = None
        self.pb_progress = None
        self.choice_delim = tk.IntVar()
        self.l_delimiter = None
        self.r_delimiter1 = None
        self.r_delimiter2 = None
        self.r_delimiter3 = None
        self.lb_var = None
        self.l_list_var = None
        self.TARGET_FILE = None
        self.SOURCE_FILE = None
        self.CHOICE_VAR = []
        self.e_target_file = None
        self.e_source_file = None
        self.b_get_list_var = None
        self.b_convert = None
        self.b_select_source_file = None
        self.b_select_target_file = None
        self.l_target_file = None
        self.l_source_file = None
        self.DELIMITER = None
        self.create_main_window()
        self.CONV_MAIN_WIN.mainloop()

    def cb1_changed(self):
        if self.v_use_sys_time.get == 0:
            self.setting_use_sys_time = False
        else:
            self.setting_use_sys_time = True

    def cb2_changed(self):
        if self.v_add_counter.get == 0:
            self.setting_add_counter = False
        else:
            self.setting_add_counter = True

    def cb3_changed(self):
        if self.v_check_data_omissions.get == 0:
            self.setting_check_data_omissions = False
        else:
            self.setting_check_data_omissions = True

    def get_delimiter(self):
        if self.choice_delim.get() == 0:
            self.DELIMITER = ';'
        elif self.choice_delim.get() == 1:
            self.DELIMITER = ','
        else:
            file = open(self.SOURCE_FILE, 'r')
            read_str = file.readline()
            file.close()
            num_pole1 = len(str.split(read_str, ';'))
            num_pole2 = len(str.split(read_str, ','))
            if num_pole1 > num_pole2:
                self.DELIMITER = ';'
            else:
                self.DELIMITER = ','
        return

    def get_file(self, file, entry: tk.Entry, button: tk.Button):
        filetypes = (("Таблица", "*.csv"),
                     ("Текстовый файл", "*.txt"),
                     ("Любой", "*"))

        filename = fd.askopenfilename(title="Выбрать файл", initialdir="C:/Users/Equint/Desktop/",
                                      filetypes=filetypes)
        if filename:
            if file == "source":
                self.SOURCE_FILE = filename
                self.auto_target_path()
                self.get_list_of_var()
            else:
                self.TARGET_FILE = filename
            entry.delete(0, tk.END)
            entry.insert(0, filename)
            button.config(state='normal')

    def get_list_of_var(self):
        count_str = 0
        tmp_list = []
        data1 = []
        self.get_delimiter()
        file = open(self.SOURCE_FILE, 'r')
        for i in file:
            count_str += 1
            spl_str = str.split(i, self.DELIMITER)
            tmp_list.append(spl_str[0])
        list_of_variable = set(tmp_list)
        file.close()
        data1.extend(list_of_variable)
        data1.sort()

        self.progress_max = count_str
        self.progress_step = self.progress_max // 100
        if len(data1):
            for i in data1:
                self.lb_var.insert(0, i)
        else:
            return

    def get_list_of_choice_var(self, list_box: tk.Listbox):
        choice_list = list_box.curselection()
        for i in choice_list:
            op = list_box.get(i)
            self.CHOICE_VAR.append(op)

    def file_transform(self, progress_bar: ttk.Progressbar):
        self.get_list_of_choice_var(self.lb_var)
        self.get_delimiter()

        self.l_progress.grid(column=0, row=3, sticky="w", padx=10, pady=10, columnspan=2)
        self.pb_progress.grid(column=0, row=4, columnspan=2, sticky="we", padx=10)

        buf_value_var = []
        list_of_search_flag = []
        time_ms = []
        count_record_num = 0
        count = 0
        buf_name_vars = []
        f_buff_full = False
        error_str = []

        source_file = open(self.SOURCE_FILE, 'r')
        target_file = open(self.TARGET_FILE, 'w')

        if self.setting_use_sys_time:
            target_file.write('Date' + ';')
            target_file.write('Time' + ';')

        if self.setting_add_counter:
            target_file.write('Counter' + ';')

        for el in self.CHOICE_VAR:
            target_file.write(el + ';')

        target_file.write("\n")

        for i in range(len(self.CHOICE_VAR)):
            buf_value_var.append(0)
            list_of_search_flag.append(False)
            time_ms.append(0.0)
            buf_name_vars.append('')
        self.progress_value: int = 0
        count_str = 0

        source_file.readline()
        for sourceStr in source_file:
            sources_str = sourceStr.split(self.DELIMITER)
            count_str += 1

            if self.setting_check_data_omissions:
                if count < len(self.CHOICE_VAR) and not f_buff_full:
                    buf_name_vars[count] = sources_str[0]

                if f_buff_full and buf_name_vars[count] == sources_str[0]:
                    pass
                elif f_buff_full:
                    error_str.append(count_str + self.progress_value * self.progress_step+1)
                    f_buff_full = False
                    count = -1

                count += 1

                if count == len(self.CHOICE_VAR) and not f_buff_full:
                    f_buff_full = True

                if count == len(self.CHOICE_VAR):
                    count = 0

            if count_str >= self.progress_step:
                count_str = 0
                self.progress_value += 1
                progress_bar.config(value=self.progress_value)
                self.l_progress.config(text=f'Выполнение: {self.progress_value} из 100%. {self.end_file}')
                self.CONV_MAIN_WIN.update()
            for i in range(len(self.CHOICE_VAR)):
                if sources_str[0] == self.CHOICE_VAR[i]:
                    buf_value_var[i] = float(sources_str[2])
                    list_of_search_flag[i] = True
                    time_ms[i] = float(sources_str[4])
            count_positive_flag = 0
            for j in range(len(self.CHOICE_VAR)):
                if list_of_search_flag[j]:
                    count_positive_flag += 1
            if count_positive_flag == len(self.CHOICE_VAR):

                if self.setting_use_sys_time:
                    sum_time_ms = 0
                    for el in range(len(self.CHOICE_VAR)):
                        sum_time_ms += time_ms[el]
                    average_time_ms = sum_time_ms // len(self.CHOICE_VAR)

                    count_day = int(average_time_ms // 1000000)
                    count_time = (average_time_ms / 1000000) % 1

                    start_date = "1899/12/30"
                    date_log = pd.to_datetime(start_date) + pd.DateOffset(days=count_day)

                    hour = math.trunc(count_time * 24)
                    minute = math.trunc(((count_time * 24) % 1) * 60)
                    second = math.trunc(((((count_time * 24) % 1) * 60) % 1) * 60)
                    time_log = f"{hour}:{minute}:{second + 1}"

                    target_file.write(str(date_log) + ";")
                    target_file.write(time_log + ";")

                if self.setting_add_counter:
                    count_record_num += 1
                    target_file.write(str(count_record_num) + ";")

                for i in range(len(self.CHOICE_VAR)):
                    target_file.write(str(buf_value_var[i]))
                    target_file.write(";")
                    buf_value_var[i] = 0
                    list_of_search_flag[i] = False

                target_file.write("\n")
        if not self.setting_check_data_omissions:
            self.end_file = 'Выполнено.'
        elif not len(error_str):
            self.end_file = 'Выполнено.'
        else:
            self.end_file = f'Пропуск данных в стр: {error_str}'

        self.l_progress.config(text=f'Выполнение: {self.progress_value} из 100%. {self.end_file}')
        self.CONV_MAIN_WIN.update()
        target_file.close()
        source_file.close()
        return None

    def auto_target_path(self):

        spl_str = self.SOURCE_FILE.split('/')
        file_name = spl_str[-1]
        file_name = file_name.split('.')
        new_name = str(file_name[0]) + '_conv.' + str(file_name[1])
        str_auto_target_file: str = ''
        for el in spl_str[0:-1]:
            str_auto_target_file += el + '/'
        str_auto_target_file += new_name
        self.TARGET_FILE = str_auto_target_file
        self.e_target_file.delete(0, tk.END)
        self.e_target_file.insert(0, self.TARGET_FILE)
        self.b_convert.config(state='normal')

    def create_main_window(self):

        self.CONV_MAIN_WIN.geometry(
            f"{self.WEIGHT_CONV_MAIN_WIN}x{self.HIGH_CONV_MAIN_WIN}+"
            f"{int(1920 / 2 - (self.WEIGHT_CONV_MAIN_WIN / 2))}+{int((1080 / 2) - (self.HIGH_CONV_MAIN_WIN / 2))}")

        self.CONV_MAIN_WIN.title(self.LABEL_CONV_WIN)

        self.CONV_MAIN_WIN.columnconfigure(1, minsize=400)

        self.create_label()
        self.create_buttons()
        self.create_entry()
        self.create_listbox()
        self.create_checkbutton()
        self.create_progressbar()
        self.create_radiobutton()
        self.create_menu_conv()

    def create_label(self):
        self.l_source_file = tk.Label(self.CONV_MAIN_WIN, text='Исходный файл', font="Arial 12")
        self.l_source_file.grid(column=0, row=0, sticky="w", padx=10, pady=10)

        self.l_target_file = tk.Label(self.CONV_MAIN_WIN, text='Файл назначения', font="Arial 12")
        self.l_target_file.grid(column=0, row=2, sticky="w", padx=10, pady=10)

        self.l_delimiter = tk.Label(self.CONV_MAIN_WIN, text='Разделитель', font="Arial 12")
        self.l_delimiter.place(x=10, y=310)

        self.l_list_var = tk.Label(self.CONV_MAIN_WIN, text='Переменные', font="Arial 12")
        self.l_list_var.grid(column=0, row=1, sticky="w", padx=10, pady=10)

        self.l_settings = tk.Label(self.CONV_MAIN_WIN, text='Настройки', font='Arial 12')
        self.l_settings.place(x=10, y=270)

    def create_buttons(self):
        self.b_select_source_file = tk.Button(self.CONV_MAIN_WIN, text="Обзор",
                                              command=lambda: self.get_file('source',
                                                                            self.e_source_file,
                                                                            self.b_get_list_var))
        self.b_select_source_file.grid(column=2, row=0, sticky="we", padx=10)

        self.b_select_target_file = tk.Button(self.CONV_MAIN_WIN, text="Обзор",
                                              command=lambda: self.get_file('target',
                                                                            self.e_target_file,
                                                                            self.b_convert))
        self.b_select_target_file.grid(column=2, row=2, sticky="we", padx=10)

        self.b_get_list_var = tk.Button(self.CONV_MAIN_WIN, text="Открыть", command=lambda: self.get_list_of_var(),
                                        state='disabled')
        self.b_get_list_var.grid(column=2, row=1, sticky="we", padx=10)

        self.b_convert = tk.Button(self.CONV_MAIN_WIN, text="Конвертировать",
                                   command=lambda: self.file_transform(self.pb_progress),
                                   state='disabled')
        self.b_convert.grid(column=2, row=3, sticky="we", padx=10)

    def create_entry(self):
        self.e_source_file = tk.Entry(self.CONV_MAIN_WIN, textvariable=self.SOURCE_FILE)
        self.e_source_file.grid(column=1, row=0, sticky="we", padx=10)
        self.e_source_file.delete(0, tk.END)

        self.e_target_file = tk.Entry(self.CONV_MAIN_WIN, textvariable=self.TARGET_FILE)
        self.e_target_file.grid(column=1, row=2, sticky="we", padx=10)
        self.e_target_file.delete(0, tk.END)

    def create_listbox(self):
        self.lb_var = tk.Listbox(self.CONV_MAIN_WIN, selectmode="multiple", height=5)
        self.lb_var.grid(column=1, row=1, sticky="we", padx=10)

        self.l_progress = tk.Label(self.CONV_MAIN_WIN,
                                   text=f'Выполнение: {self.progress_value} из 100%. {self.end_file}',
                                   textvariable=self.progress_value, font="Arial 12")

    def create_radiobutton(self):
        self.r_delimiter1 = tk.Radiobutton(self.CONV_MAIN_WIN, text=';', variable=self.choice_delim, value=0,
                                           font="Arial 12")
        self.r_delimiter1.place(x=120, y=310)

        self.r_delimiter2 = tk.Radiobutton(self.CONV_MAIN_WIN, text=',', variable=self.choice_delim, value=1,
                                           font="Arial 12")
        self.r_delimiter2.place(x=160, y=310)

        self.r_delimiter3 = tk.Radiobutton(self.CONV_MAIN_WIN, text='auto', variable=self.choice_delim, value=2,
                                           font="Arial 10")
        self.r_delimiter3.place(x=200, y=310)
        self.choice_delim.set(2)

    def create_progressbar(self):
        self.pb_progress = ttk.Progressbar(self.CONV_MAIN_WIN, orient='horizontal', maximum=100, mode='determinate',
                                           value=self.progress_value)

        self.progress_value: int = 0
        self.l_progress.config(text=f'Выполнение: {self.progress_value} из 100%. {self.end_file}')

    def create_checkbutton(self):
        self.cb_sys_time = tk.Checkbutton(self.CONV_MAIN_WIN, text='Использовать системное время')
        self.cb_sys_time.place(x=100, y=270)

        self.cb_sys_time = tk.Checkbutton(self.CONV_MAIN_WIN, text='Использовать системное время',
                                          variable=self.v_use_sys_time, command=self.cb1_changed)
        self.cb_sys_time.place(x=100, y=270)

        self.cb_add_record_counter = tk.Checkbutton(self.CONV_MAIN_WIN, text='Добавить счётчик записей',
                                                    variable=self.v_add_counter, command=self.cb2_changed)
        self.cb_add_record_counter.place(x=300, y=270)

        self.cb_check_data_omissions = tk.Checkbutton(self.CONV_MAIN_WIN, text='Регистрировать пропуски данных',
                                                      variable=self.setting_check_data_omissions,
                                                      command=self.cb3_changed)
        self.cb_check_data_omissions.place(x=470, y=270)

    def create_menu_conv(self):
        self.MAIN_WIN_MENU = tk.Menu(self.CONV_MAIN_WIN)
        self.CONV_MAIN_WIN.config(menu=self.MAIN_WIN_MENU)
        self.MAIN_WIN_MENU.add_command(label="Перезапустить", command=lambda: reboot_conv_win(self))
        self.MAIN_WIN_MENU.add_command(
            label="Построение графиков", command=lambda: create_graph_win(self))


def reboot_conv_win(obj: ConvertLogFile):
    obj.CONV_MAIN_WIN.destroy()
    obj.__init__()


def reboot_graph_win(obj: CreatePlot):
    obj.GRAPH_MAIN_WIN.destroy()
    obj.__init__()


def create_conv_win(obj: CreatePlot):
    obj.GRAPH_MAIN_WIN.destroy()
    obj = ConvertLogFile()
    return obj


def create_graph_win(obj: ConvertLogFile):
    obj.CONV_MAIN_WIN.destroy()
    obj = CreatePlot()
    return obj


program = ConvertLogFile()
