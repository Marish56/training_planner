import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar


class DatePicker(tk.Toplevel):
    """Простой календарь для выбора даты на чистом tkinter"""
    
    def __init__(self, parent, entry_widget):
        super().__init__(parent)
        self.entry_widget = entry_widget
        self.title("Выберите дату")
        self.geometry("300x280")
        self.resizable(False, False)
        
        # Текущая отображаемая дата
        self.current_date = datetime.now()
        self.selected_date = None
        
        self.create_widgets()
        self.update_calendar()
        
        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Центрируем окно относительно родителя
        self.center_window(parent)
    
    def center_window(self, parent):
        """Центрирует окно относительно родительского"""
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Создает элементы календаря"""
        # Фрейм для навигации по месяцам
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)
        
        self.prev_button = tk.Button(nav_frame, text="◄", command=self.prev_month, width=3)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.month_label = tk.Label(nav_frame, text="", width=20, font=("Arial", 10, "bold"))
        self.month_label.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(nav_frame, text="►", command=self.next_month, width=3)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для дней недели
        days_frame = tk.Frame(self)
        days_frame.pack(pady=5)
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            label = tk.Label(days_frame, text=day, width=4, font=("Arial", 8, "bold"))
            label.grid(row=0, column=i)
        
        # Фрейм для чисел месяца
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(pady=5)
        
        # Кнопки ОК и Отмена
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=self.on_ok, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Отмена", command=self.on_cancel, width=10).pack(side=tk.LEFT, padx=5)
    
    def update_calendar(self):
        """Обновляет отображение календаря"""
        # Очищаем предыдущий календарь
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Обновляем заголовок
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        self.month_label.config(text=f"{months[self.current_date.month - 1]} {self.current_date.year}")
        
        # Получаем календарь на текущий месяц
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Отображаем дни
        today = datetime.now().date()
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    # Определяем цвет для сегодняшней даты
                    date = datetime(self.current_date.year, self.current_date.month, day).date()
                    
                    if date == today:
                        bg_color = "#0078D7"  # Синий для сегодня
                        fg_color = "white"
                    elif self.selected_date and date == self.selected_date:
                        bg_color = "#E5F3FF"  # Светло-синий для выбранной даты
                        fg_color = "black"
                    else:
                        bg_color = "white"
                        fg_color = "black"
                    
                    btn = tk.Button(
                        self.calendar_frame,
                        text=str(day),
                        width=4,
                        bg=bg_color,
                        fg=fg_color,
                        command=lambda d=day: self.select_date(d)
                    )
                    btn.grid(row=week_num, column=day_num, padx=1, pady=1)
    
    def select_date(self, day):
        """Выбирает дату"""
        self.selected_date = datetime(self.current_date.year, self.current_date.month, day).date()
        self.update_calendar()
    
    def prev_month(self):
        """Переключает на предыдущий месяц"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()
    
    def next_month(self):
        """Переключает на следующий месяц"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()
    
    def on_ok(self):
        """Подтверждает выбор даты"""
        if self.selected_date:
            self.entry_widget.delete(0, tk.END)
            self.entry_widget.insert(0, self.selected_date.strftime("%d.%m.%Y"))
        self.destroy()
    
    def on_cancel(self):
        """Отменяет выбор даты"""
        self.destroy()


class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("950x700")
        
        # Файл для хранения данных по умолчанию
        self.data_file = "trainings.json"
        self.trainings = []
        
        # Типы тренировок
        self.training_types = ["Бег", "Плавание", "Велосипед", "Силовая", "Йога", "Растяжка", "Другое"]
        
        self.create_widgets()
        self.load_data()  # Автоматическая загрузка при запуске
        
        # Привязываем сохранение при закрытии окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # Создаем меню
        self.create_menu()
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Дата с календарем
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", pady=5)
        
        # Фрейм для даты и кнопки календаря
        date_frame = tk.Frame(input_frame)
        date_frame.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        self.date_entry = ttk.Entry(date_frame, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Привязываем события для автоподстановки точек
        self.date_entry.bind('<KeyRelease>', self.format_date)
        self.date_entry.bind('<FocusOut>', self.validate_date_format)
        
        # Кнопка календаря
        calendar_button = ttk.Button(date_frame, text="📅", width=3, 
                                    command=lambda: DatePicker(self.root, self.date_entry))
        calendar_button.pack(side=tk.LEFT)
        
        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="w", pady=5)
        self.type_combobox = ttk.Combobox(input_frame, values=self.training_types, width=18)
        self.type_combobox.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.type_combobox.set(self.training_types[0])
        
        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w", pady=5)
        self.duration_entry = ttk.Entry(input_frame, width=20)
        self.duration_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        
        # Кнопка добавления
        add_button = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, sticky="w", pady=5)
        
        # Фрейм для даты фильтра и кнопки календаря
        filter_date_frame = tk.Frame(filter_frame)
        filter_date_frame.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        self.filter_date_entry = ttk.Entry(filter_date_frame, width=15)
        self.filter_date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Привязываем события для автоподстановки точек в фильтре
        self.filter_date_entry.bind('<KeyRelease>', self.format_date)
        
        # Кнопка календаря для фильтра
        filter_calendar_button = ttk.Button(filter_date_frame, text="📅", width=3,
                                          command=lambda: DatePicker(self.root, self.filter_date_entry))
        filter_calendar_button.pack(side=tk.LEFT)
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=1, column=0, sticky="w", pady=5)
        self.filter_type_combobox = ttk.Combobox(filter_frame, values=["Все"] + self.training_types, width=18)
        self.filter_type_combobox.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.filter_type_combobox.set("Все")
        
        # Кнопки фильтрации
        filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=2, column=0, padx=5, pady=5)
        
        clear_filter_button = ttk.Button(filter_frame, text="Очистить фильтр", command=self.clear_filter)
        clear_filter_button.grid(row=2, column=1, padx=5, pady=5)
        
        # Таблица для отображения тренировок
        table_frame = ttk.LabelFrame(self.root, text="Список тренировок", padding="10")
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Создаем таблицу
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        
        self.tree.column("date", width=150)
        self.tree.column("type", width=200)
        self.tree.column("duration", width=150)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Контекстное меню для удаления
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Удалить тренировку", command=self.delete_training)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Статус бар для отображения информации о файле
        self.status_bar = ttk.Label(self.root, text=f"Файл данных: {self.data_file}", relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        # Настройка весов для правильного масштабирования
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def create_menu(self):
        """Создает главное меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить (Ctrl+S)", command=self.save_data, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_data_as)
        file_menu.add_command(label="Открыть...", command=self.open_data)
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт в JSON...", command=self.export_to_json)
        file_menu.add_command(label="Импорт из JSON...", command=self.import_from_json)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)
        
        # Привязываем горячие клавиши
        self.root.bind('<Control-s>', lambda event: self.save_data())
        self.root.bind('<Control-S>', lambda event: self.save_data())
    
    def format_date(self, event):
        """Автоматически добавляет точки при вводе даты"""
        widget = event.widget
        text = widget.get()
        
        # Удаляем все нецифровые символы, кроме точек
        cleaned = ''.join(c for c in text if c.isdigit() or c == '.')
        
        # Если пользователь стер символы - пропускаем форматирование
        if event.keysym in ['BackSpace', 'Delete']:
            return
        
        # Удаляем все точки для переформатирования
        digits = ''.join(c for c in cleaned if c.isdigit())
        
        # Форматируем с точками
        formatted = ''
        if len(digits) > 0:
            formatted = digits[:2]
        if len(digits) > 2:
            formatted += '.' + digits[2:4]
        if len(digits) > 4:
            formatted += '.' + digits[4:8]
        
        # Обновляем текст только если он изменился
        if formatted != text:
            cursor_pos = widget.index(tk.INSERT)
            widget.delete(0, tk.END)
            widget.insert(0, formatted)
            # Устанавливаем курсор в конец
            widget.icursor(len(formatted))
    
    def validate_date_format(self, event=None):
        """Проверяет и исправляет формат даты при потере фокуса"""
        widget = event.widget if event else self.date_entry
        text = widget.get().strip()
        
        if text:
            # Пытаемся привести к правильному формату
            digits = ''.join(c for c in text if c.isdigit())
            
            if len(digits) == 8:
                formatted = f"{digits[:2]}.{digits[2:4]}.{digits[4:8]}"
                widget.delete(0, tk.END)
                widget.insert(0, formatted)
    
    def show_context_menu(self, event):
        """Показывает контекстное меню при правом клике"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def validate_input(self, date, duration):
        """Проверяет корректность ввода"""
        try:
            # Проверка даты
            datetime.strptime(date, "%d.%m.%Y")
            
            # Проверка длительности
            duration_int = int(duration)
            if duration_int <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
                
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return False
    
    def add_training(self):
        """Добавляет новую тренировку"""
        date = self.date_entry.get().strip()
        training_type = self.type_combobox.get()
        duration = self.duration_entry.get().strip()
        
        if self.validate_input(date, duration):
            training = {
                "date": date,
                "type": training_type,
                "duration": int(duration)
            }
            
            self.trainings.append(training)
            self.save_data()  # Автоматическое сохранение после добавления
            self.refresh_table()
            self.clear_input()
            messagebox.showinfo("Успех", "Тренировка добавлена! Данные сохранены в JSON.")
    
    def delete_training(self):
        """Удаляет выбранную тренировку"""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], "values")
            
            for training in self.trainings:
                if (training["date"] == item_values[0] and 
                    training["type"] == item_values[1] and 
                    training["duration"] == int(item_values[2])):
                    self.trainings.remove(training)
                    break
            
            self.save_data()  # Автоматическое сохранение после удаления
            self.refresh_table()
    
    def apply_filter(self):
        """Применяет фильтры к таблице"""
        filter_date = self.filter_date_entry.get().strip()
        filter_type = self.filter_type_combobox.get()
        
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Фильтруем данные
        filtered_trainings = self.trainings.copy()
        
        if filter_type != "Все":
            filtered_trainings = [t for t in filtered_trainings if t["type"] == filter_type]
        
        if filter_date:
            filtered_trainings = [t for t in filtered_trainings if t["date"] == filter_date]
        
        # Отображаем отфильтрованные данные
        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def clear_filter(self):
        """Очищает фильтры и показывает все данные"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_type_combobox.set("Все")
        self.refresh_table()
    
    def clear_input(self):
        """Очищает поля ввода"""
        self.date_entry.delete(0, tk.END)
        self.type_combobox.set(self.training_types[0])
        self.duration_entry.delete(0, tk.END)
    
    def refresh_table(self):
        """Обновляет таблицу"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for training in self.trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def save_data(self):
        """Сохраняет данные в текущий JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
            self.update_status_bar()
            return True
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные:\n{e}")
            return False
    
    def save_data_as(self):
        """Сохраняет данные в выбранный JSON файл"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить как..."
        )
        if filename:
            old_file = self.data_file
            self.data_file = filename
            if self.save_data():
                messagebox.showinfo("Успех", f"Данные сохранены в:\n{filename}")
            else:
                self.data_file = old_file
    
    def open_data(self):
        """Открывает и загружает данные из выбранного JSON файла"""
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Открыть файл данных"
        )
        if filename:
            self.data_file = filename
            self.load_data()
    
    def export_to_json(self):
        """Экспортирует данные в новый JSON файл с дополнительной информацией"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Экспорт данных"
        )
        if filename:
            try:
                # Создаем расширенную структуру для экспорта
                export_data = {
                    "export_date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    "total_trainings": len(self.trainings),
                    "training_types": list(set(t["type"] for t in self.trainings)),
                    "trainings": self.trainings
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=4)
                
                messagebox.showinfo("Экспорт", f"Данные экспортированы в:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{e}")
    
    def import_from_json(self):
        """Импортирует данные из JSON файла с проверкой структуры"""
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Импорт данных из JSON"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                
                # Проверяем структуру данных
                if isinstance(imported_data, dict) and "trainings" in imported_data:
                    # Если это экспортированный файл с дополнительной информацией
                    new_trainings = imported_data["trainings"]
                elif isinstance(imported_data, list):
                    # Если это простой список тренировок
                    new_trainings = imported_data
                else:
                    messagebox.showerror("Ошибка", "Неверный формат JSON файла")
                    return
                
                # Проверяем структуру каждой тренировки
                valid_trainings = []
                for t in new_trainings:
                    if all(key in t for key in ["date", "type", "duration"]):
                        valid_trainings.append(t)
                
                if not valid_trainings:
                    messagebox.showerror("Ошибка", "В файле нет корректных данных о тренировках")
                    return
                
                # Спрашиваем, заменить или добавить
                response = messagebox.askyesno(
                    "Импорт данных",
                    f"Найдено {len(valid_trainings)} тренировок.\n\n"
                    "Да - заменить текущие данные\n"
                    "Нет - добавить к текущим данным"
                )
                
                if response:
                    self.trainings = valid_trainings
                else:
                    self.trainings.extend(valid_trainings)
                
                self.save_data()
                self.refresh_table()
                
                messagebox.showinfo("Импорт", f"Импортировано {len(valid_trainings)} тренировок")
                
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Файл не является корректным JSON")
            except Exception as e:
                messagebox.showerror("Ошибка импорта", f"Не удалось импортировать данные:\n{e}")
    
    def load_data(self):
        """Загружает данные из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # Проверяем, не экспортированный ли это формат
                if isinstance(loaded_data, dict) and "trainings" in loaded_data:
                    self.trainings = loaded_data["trainings"]
                else:
                    self.trainings = loaded_data
                
                self.refresh_table()
                self.update_status_bar()
                
                # Показываем информацию о загрузке
                print(f"Загружено {len(self.trainings)} тренировок из {self.data_file}")
                
            except json.JSONDecodeError:
                messagebox.showwarning("Предупреждение", "Файл JSON поврежден. Создана новая база данных.")
                self.trainings = []
            except Exception as e:
                messagebox.showwarning("Предупреждение", f"Не удалось загрузить данные:\n{e}")
                self.trainings = []
        else:
            messagebox.showinfo("Новый файл", f"Файл {self.data_file} не найден.\nБудет создана новая база данных.")
            self.trainings = []
            self.update_status_bar()
    
    def update_status_bar(self):
        """Обновляет статус бар с информацией о файле"""
        file_size = os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0
        self.status_bar.config(
            text=f"Файл: {self.data_file} | Тренировок: {len(self.trainings)} | Размер: {file_size} байт"
        )
    
    def on_closing(self):
        """Действия при закрытии приложения"""
        # Сохраняем данные перед выходом
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()