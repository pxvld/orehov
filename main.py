import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import datetime
import os # Импорт для работы с файлами

# ГЛАВНОЕ ОКНО
class PasswordApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Генератор паролей")
        self.root.geometry("400x300")
        
        # Переменные
        self.password = tk.StringVar()
        self.length = tk.IntVar(value=12)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        
        self.history = []  # История последних 5 паролей
        
        self.setup_ui()
        self.generate()
        
    def setup_ui(self):
        tk.Label(self.root, text="🔐 ГЕНЕРАТОР ПАРОЛЕЙ", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Поле с паролем и кнопка копирования
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.password, width=25, font=("Arial", 12), 
                justify="center", state="readonly").pack(side="left")
        tk.Button(frame, text="📋", command=self.copy, width=3).pack(side="left")
        
        # Настройки
        f = tk.LabelFrame(self.root, text="Настройки")
        f.pack(pady=5, padx=10, fill="x")
        
        tk.Label(f, text="Длина:").pack()
        tk.Scale(f, from_=4, to=32, orient="h", variable=self.length, 
                command=lambda x: self.generate()).pack()
        
        tk.Checkbutton(f, text="A-Z", variable=self.use_upper, command=self.generate).pack()
        tk.Checkbutton(f, text="a-z", variable=self.use_lower, command=self.generate).pack()
        tk.Checkbutton(f, text="0-9", variable=self.use_digits, command=self.generate).pack()
        tk.Checkbutton(f, text="!@#$%", variable=self.use_symbols, command=self.generate).pack()
        
        # Кнопки для окон
        tk.Button(self.root, text="⚙️ Доп. настройки", command=self.open_settings, 
                 bg="#2196F3", fg="white").pack(pady=2)
        tk.Button(self.root, text="📜 История", command=self.open_history, 
                 bg="#FF9800", fg="white").pack(pady=2)
        
    def generate(self):
        chars = ""
        if self.use_upper.get(): chars += string.ascii_uppercase
        if self.use_lower.get(): chars += string.ascii_lowercase
        if self.use_digits.get(): chars += string.digits
        if self.use_symbols.get(): chars += "!@#$%^&*"
        
        if not chars:
            self.password.set("Выберите символы!")
            return
        
        pwd = ''.join(random.choice(chars) for _ in range(self.length.get()))
        self.password.set(pwd)
        
        # Сохраняем в историю (последние 5)
        self.history.append(pwd)
        if len(self.history) > 5:
            self.history.pop(0)
            
        # Логирование в файл
        self.log_password(pwd)
    
    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password.get())
        messagebox.showinfo("", "Пароль скопирован!")
    
    def open_settings(self):
        SettingsWindow(self)
    
    def open_history(self):
        HistoryWindow(self)
    
    def run(self):
        self.root.mainloop()
    
    def log_password(self, pwd):
        """Записывает пароль в файл лога с меткой времени."""
        try:
            with open('password_log.txt', 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {pwd}\n")
                # Добавим пустую строку для разделения записей (опционально)
                f.write("\n")
        except Exception as e:
            messagebox.showerror("Ошибка логирования", f"Не удалось записать пароль в лог:\n{e}")


# ОКНО НАСТРОЕК
class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Доп. настройки")
        self.win.geometry("300x200")
        
        self.extended = tk.BooleanVar(value=False)
        
        tk.Label(self.win, text="⚙️ Дополнительные опции", font=("Arial", 12, "bold")).pack(pady=5)
        
        tk.Checkbutton(self.win, text="Расширенные символы (_-+=[]{}|;:)", 
                      variable=self.extended).pack(pady=5)
        
        tk.Button(self.win, text="Применить", command=self.apply, 
                 bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.win, text="Закрыть", command=self.win.destroy).pack()
    
    def apply(self):
        if self.extended.get():
            self.app.use_symbols.set(True)
            messagebox.showinfo("", "Включены расширенные символы!")
            self.app.generate()
            self.win.destroy()


# ОКНО ИСТОРИИ
class HistoryWindow:
    def __init__(self, app):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("История")
        self.win.geometry("300x250")
        
        tk.Label(self.win, text="📜 Последние пароли", font=("Arial", 12, "bold")).pack(pady=5)
        
        if hasattr(app, 'history') and app.history:
            for pwd in reversed(app.history):
                f = tk.Frame(self.win)
                f.pack(pady=2, padx=10, fill="x")
                tk.Label(f, text=pwd, font=("Courier", 10)).pack(side="left")
                tk.Button(f, text="📋", command=lambda p=pwd: self.copy(p), 
                         width=2).pack(side="right")
                # Кнопка "Сохранить" (дополнительно)
                tk.Button(f, text="💾", command=lambda p=pwd: self.save_manually(p), 
                         width=2).pack(side="right")
                
                ttk.Separator(self.win).pack(fill='x', padx=10)
                
            # Кнопка очистить историю (в памяти)
            tk.Button(self.win, text="Очистить историю (в памяти)", 
                     command=self.clear_history).pack(pady=10)
            
            # Кнопка открыть лог-файл
            tk.Button(self.win, text="Открыть файл лога", 
                     command=self.open_log_file).pack(pady=5)
            
            # Кнопка очистить файл лога
            tk.Button(self.win, text="Очистить файл лога", 
                     command=self.clear_log_file).pack(pady=5)
            
            

    def copy(self, pwd):
        self.app.root.clipboard_clear()
        self.app.root.clipboard_append(pwd)
        messagebox.showinfo("", "Скопировано!")
    
    def save_manually(self, pwd):
         """Ручное сохранение пароля в лог (дублирует автоматическое)"""
         try:
             with open('password_log.txt', 'a', encoding='utf-8') as f:
                 timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 f.write(f"[{timestamp}] {pwd} (сохранено вручную)\n\n")
             messagebox.showinfo("", "Пароль сохранён в лог!")
         except Exception as e:
             messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить пароль:\n{e}")
    
    def clear_history(self):
         """Очищает историю только в памяти программы."""
         if messagebox.askyesno("Подтвердите", "Очистить историю последних паролей?"):
             self.app.history.clear()
             messagebox.showinfo("", "История очищена!")
             self.win.destroy()  # Перезапуск окна истории
             self.app.open_history()
    
    def open_log_file(self):
         """Пытается открыть файл лога в стандартном приложении."""
         try:
             os.startfile('password_log.txt')
         except Exception as e:
             messagebox.showerror("Ошибка открытия файла", f"Не удалось открыть файл лога:\n{e}")
    
    def clear_log_file(self):
         """Полностью очищает файл лога."""
         if messagebox.askyesno("Подтвердите", "Полностью очистить файл лога? Это действие нельзя отменить."):
             try:
                 open('password_log.txt', 'w').close()  # Очистка файла
                 messagebox.showinfo("", "Файл лога очищен!")
             except Exception as e:
                 messagebox.showerror("Ошибка очистки файла", f"Не удалось очистить файл лога:\n{e}")


# ЗАПУСК
if __name__ == "__main__":
    app = PasswordApp()
    app.run()
