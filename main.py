import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import string
import datetime
import os

# Файл для логов
LOG_FILE = "password_generator.log"

# Функция для записи логов
def log(action, details=""):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{t}] {action}: {details}\n")
    except:
        pass

# ГЛАВНОЕ ОКНО
class PasswordApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Генератор паролей")
        self.root.geometry("450x450")
        
        # Переменные
        self.password = tk.StringVar()
        self.length = tk.IntVar(value=12)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        
        # История
        self.history = []
        self.saved = []
        
        self.setup_ui()
        self.generate()
        log("ЗАПУСК", "Программа запущена")
        
    def setup_ui(self):
        # Заголовок
        tk.Label(self.root, text="ГЕНЕРАТОР ПАРОЛЕЙ", 
                font=("Arial", 14, "bold")).pack(pady=5)
        
        # Поле пароля
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5)
        tk.Entry(frame1, textvariable=self.password, width=25, 
                font=("Arial", 12), state="readonly").pack(side="left", padx=5)
        tk.Button(frame1, text="Копировать", command=self.copy).pack(side="left")
        
        # Ручной ввод
        frame2 = tk.Frame(self.root)
        frame2.pack(pady=5)
        tk.Label(frame2, text="Свой пароль:").pack(side="left")
        self.manual = tk.Entry(frame2, width=15)
        self.manual.pack(side="left", padx=5)
        tk.Button(frame2, text="Проверить", command=self.check).pack(side="left")
        
        # Настройки
        f = tk.LabelFrame(self.root, text="Настройки")
        f.pack(pady=5, padx=10, fill="x")
        
        # Длина
        len_frame = tk.Frame(f)
        len_frame.pack(pady=5)
        tk.Label(len_frame, text="Длина:").pack(side="left")
        tk.Spinbox(len_frame, from_=4, to=32, textvariable=self.length, 
                  width=5, command=self.generate).pack(side="left", padx=10)
        
        # Чекбоксы
        cb_frame = tk.Frame(f)
        cb_frame.pack(pady=5)
        tk.Checkbutton(cb_frame, text="A-Z", variable=self.use_upper, 
                      command=self.generate).pack(side="left", padx=5)
        tk.Checkbutton(cb_frame, text="a-z", variable=self.use_lower, 
                      command=self.generate).pack(side="left", padx=5)
        tk.Checkbutton(cb_frame, text="0-9", variable=self.use_digits, 
                      command=self.generate).pack(side="left", padx=5)
        tk.Checkbutton(cb_frame, text="!@#$", variable=self.use_symbols, 
                      command=self.generate).pack(side="left", padx=5)
        
        # Сложность
        self.strength = tk.Label(self.root, text="", font=("Arial", 10))
        self.strength.pack(pady=5)
        
        # Кнопки действий
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Сгенерировать", command=self.generate,
                 bg="#4CAF50", fg="white", width=12).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Сохранить", command=self.save,
                 bg="#FF9800", fg="white", width=12).pack(side="left", padx=2)
        tk.Button(btn_frame, text="История", command=self.show_history,
                 bg="#2196F3", fg="white", width=12).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Логи", command=self.show_logs,
                 bg="#607D8B", fg="white", width=12).pack(side="left", padx=2)
        
        # Заметка
        note_frame = tk.LabelFrame(self.root, text="Заметка")
        note_frame.pack(pady=5, padx=10, fill="x")
        self.note = tk.Entry(note_frame, width=40)
        self.note.pack(pady=5)
        
        # Статус
        self.status = tk.Label(self.root, text="Готов", font=("Arial", 8), fg="gray")
        self.status.pack(pady=5)
    
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
        
        # Сохраняем в историю
        self.history.append(pwd)
        if len(self.history) > 10:
            self.history.pop(0)
        
        # Оценка сложности
        score = 0
        if len(pwd) >= 12: score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.islower() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in "!@#$%^&*" for c in pwd): score += 1
        
        levels = ["Слабый", "Средний", "Хороший", "Отличный"]
        level = levels[min(score, 4) - 1] if score > 0 else "Слабый"
        self.strength.config(text=f"Сложность: {level} ({score}/5)")
        
        self.status.config(text=f"Сгенерирован пароль")
        log("ГЕНЕРАЦИЯ", f"Длина: {len(pwd)}")
    
    def copy(self):
        pwd = self.password.get()
        if pwd and pwd != "Выберите символы!":
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            self.status.config(text="Скопировано!")
            log("КОПИРОВАНИЕ", "Пароль скопирован")
    
    def check(self):
        pwd = self.manual.get()
        if not pwd:
            messagebox.showwarning("", "Введите пароль!")
            return
        
        # Проверка
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_symbol = any(c in "!@#$%^&*" for c in pwd)
        
        msg = f"Длина: {len(pwd)}\n"
        msg += f"Заглавные: {'✓' if has_upper else '✗'}\n"
        msg += f"Строчные: {'✓' if has_lower else '✗'}\n"
        msg += f"Цифры: {'✓' if has_digit else '✗'}\n"
        msg += f"Спецсимволы: {'✓' if has_symbol else '✗'}"
        
        messagebox.showinfo("Результат", msg)
        log("ПРОВЕРКА", f"Проверен пароль длиной {len(pwd)}")
    
    def save(self):
        pwd = self.password.get()
        if not pwd or pwd == "Выберите символы!":
            messagebox.showerror("", "Нет пароля!")
            return
        
        note_text = self.note.get()
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.saved.append({"pwd": pwd, "note": note_text, "time": t})
        
        # Сохраняем в файл
        try:
            with open("saved_passwords.txt", "a", encoding="utf-8") as f:
                f.write(f"[{t}] {pwd} | {note_text}\n")
        except:
            pass
        
        self.status.config(text="Сохранено!")
        log("СОХРАНЕНИЕ", f"Сохранен пароль")
        messagebox.showinfo("", "Пароль сохранен!")
    
    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("История")
        win.geometry("400x300")
        
        tk.Label(win, text="Последние пароли", font=("Arial", 12, "bold")).pack(pady=5)
        
        if self.history:
            for i, pwd in enumerate(reversed(self.history[-10:]), 1):
                f = tk.Frame(win)
                f.pack(pady=2, padx=10, fill="x")
                tk.Label(f, text=f"{i}.", width=3).pack(side="left")
                tk.Label(f, text=pwd, font=("Courier", 10)).pack(side="left")
                tk.Button(f, text="Копировать", command=lambda p=pwd: self.copy_from_history(p),
                         width=8).pack(side="right")
        else:
            tk.Label(win, text="История пуста").pack(pady=20)
        
        tk.Button(win, text="Закрыть", command=win.destroy).pack(pady=10)
    
    def copy_from_history(self, pwd):
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        messagebox.showinfo("", "Скопировано!")
    
    def show_logs(self):
        win = tk.Toplevel(self.root)
        win.title("Логи")
        win.geometry("500x350")
        
        tk.Label(win, text="Логи работы", font=("Arial", 12, "bold")).pack(pady=5)
        
        text_area = scrolledtext.ScrolledText(win, width=60, height=18)
        text_area.pack(pady=10, padx=10, fill="both", expand=True)
        
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    text_area.insert("end", f.read())
            else:
                text_area.insert("end", "Логов пока нет")
            text_area.config(state="disabled")
        except:
            text_area.insert("end", "Ошибка чтения логов")
        
        tk.Button(win, text="Закрыть", command=win.destroy).pack(pady=10)
    
    def run(self):
        self.root.mainloop()
        log("ЗАВЕРШЕНИЕ", "Программа закрыта")


# ЗАПУСК
if __name__ == "__main__":
    app = PasswordApp()
    app.run()
