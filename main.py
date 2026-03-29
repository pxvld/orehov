import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    filename='password_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ГЛАВНОЕ ОКНО
class PasswordApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Генератор паролей")
        self.root.geometry("450x400")

        # Переменные
        self.password = tk.StringVar()
        self.length = tk.IntVar(value=12)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.custom_chars_var = tk.StringVar()

        self.history = []

        self.setup_ui()
        self.generate()

    def setup_ui(self):
        tk.Label(self.root, text="🔐 ГЕНЕРАТОР ПАРОЛЕЙ", font=("Arial", 14, "bold")).pack(pady=5)

        # Поле с паролем и кнопка копирования
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.password, width=30, font=("Arial", 12),
                justify="center", state="readonly").pack(side="left")
        tk.Button(frame, text="📋", command=self.copy, width=3).pack(side="left")

        # Настройки длины пароля с полем ввода
        length_frame = tk.Frame(self.root)
        length_frame.pack(pady=5)
        tk.Label(length_frame, text="Длина пароля:").pack(side="left")
        self.length_entry = tk.Entry(length_frame, width=5, textvariable=self.length)
        self.length_entry.pack(side="left", padx=5)
        tk.Button(length_frame, text="Установить", command=self.update_length).pack(side="left")

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Сгенерировать", command=self.generate,
                 bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="⚙️ Доп. настройки", command=self.open_settings,
                 bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="📜 История", command=self.open_history,
                 bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Очистить историю", command=self.clear_history,
                 bg="#F44336", fg="white").pack(side="left", padx=5)

        # Статус-бар
        self.status_var = tk.StringVar(value="Готов к работе")
        tk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w").pack(fill="x", side="bottom")

    def update_length(self):
        try:
            length = int(self.length_entry.get())
            if 4 <= length <= 64:
                self.length.set(length)
                self.generate()
                self.log_action(f"Установлена длина пароля: {length}")
            else:
                messagebox.showerror("Ошибка", "Длина должна быть от 4 до 64 символов")
                self.log_action("Ошибка: длина вне допустимого диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовое значение")
            self.log_action("Ошибка: неверный формат длины пароля")

    def open_settings(self):
        SettingsWindow(self.root, self)

    def open_history(self):
        HistoryWindow(self.root, self)

    def clear_history(self):
        self.history.clear()
        self.log_action("История очищена")
        messagebox.showinfo("Успех", "История паролей очищена")

    def add_custom_chars(self, custom_chars):
        if custom_chars:
            # Добавляем пользовательские символы к существующим
            current_chars = self.get_character_set()
            new_chars = current_chars + custom_chars
            # Генерируем пароль с новыми символами
            pwd = ''.join(random.choice(new_chars) for _ in range(self.length.get()))
            self.password.set(pwd)
            # Сохраняем в историю
            self.history.append(pwd)
            if len(self.history) > 5:
                self.history.pop(0)
            self.log_action(f"Добавлены пользовательские символы: {custom_chars}")
        else:
            messagebox.showwarning("Предупреждение", "Поле пользовательских символов пустое")
            self.log_action("Предупреждение: попытка добавить пустые символы")

    def get_character_set(self):
        chars = ""
        if self.use_upper.get(): chars += string.ascii_uppercase
        if self.use_lower.get(): chars += string.ascii_lowercase
        if self.use_digits.get(): chars += string.digits
        if self.use_symbols.get(): chars += "!@#$%^&*"
        return chars

    def generate(self):
        chars = self.get_character_set()
        custom = self.custom_chars_var.get()
        if custom:
            chars += custom

        if not chars:
            self.password.set("Выберите символы!")
            self.log_action("Ошибка: не выбраны символы для генерации")
            return

        pwd = ''.join(random.choice(chars) for _ in range(self.length.get()))
        self.password.set(pwd)

        # Сохраняем в историю
        self.history.append(pwd)
        if len(self.history) > 5:
            self.history.pop(0)

        self.log_action(f"Сгенерирован новый пароль (длина: {self.length.get()})")

    def copy(self):
        if self.password.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password.get())
            messagebox.showinfo("", "Пароль скопирован!")
            self.log_action("Пароль скопирован в буфер обмена")
        else:
            messagebox.showerror("Ошибка", "Нет пароля для копирования")
            self.log_action("Ошибка: попытка скопировать пустой пароль")

    def log_action(self, message):
        logging.info(message)


# ОКНО НАСТРОЕК
class SettingsWindow:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.window.title("Дополнительные настройки")
        self.window.geometry("350x300")
        self.window.transient(parent)  # Делает окно зависимым от родительского
        self.window.grab_set()  # Блокирует взаимодействие с родительским окном

        self.app = app

        tk.Label(self.window, text="Настройки символов", font=("Arial", 12, "bold")).pack(pady=10)

        # Настройки символов
        f = tk.LabelFrame(self.window, text="Типы символов")
        f.pack(pady=5, padx=10, fill="x")

        tk.Checkbutton(f, text="A-Z (верхний регистр)", variable=self.app.use_upper, command=self.app.generate).pack(anchor="w")
        tk.Checkbutton(f, text="a-z (нижний регистр)", variable=self.app
