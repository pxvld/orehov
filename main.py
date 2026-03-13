import tkinter as tk
import random
import string

def generate():
    chars = ""
    if upper.get(): chars += string.ascii_uppercase
    if lower.get(): chars += string.ascii_lowercase
    if digits.get(): chars += string.digits
    if symbols.get(): chars += "!@#$%^&*"
    
    if not chars:
        result.set("Ошибка: выберите символы")
        return
    
    password = ''.join(random.choice(chars) for _ in range(length.get()))
    result.set(password)

def copy_pass():
    root.clipboard_clear()
    root.clipboard_append(result.get())

# Окно
root = tk.Tk()
root.title("Генератор паролей")
root.geometry("350x250")

# Переменные
result = tk.StringVar()
length = tk.IntVar(value=12)
upper = tk.BooleanVar(value=True)
lower = tk.BooleanVar(value=True)
digits = tk.BooleanVar(value=True)
symbols = tk.BooleanVar(value=False)

# Интерфейс
tk.Entry(root, textvariable=result, font=("Arial", 12), width=30).pack(pady=10)
tk.Button(root, text="📋 Копировать", command=copy_pass).pack()

tk.Label(root, text="Длина:").pack()
tk.Scale(root, from_=4, to_=32, orient="horizontal", variable=length).pack()

tk.Checkbutton(root, text="A-Z", variable=upper).pack()
tk.Checkbutton(root, text="a-z", variable=lower).pack()
tk.Checkbutton(root, text="0-9", variable=digits).pack()
tk.Checkbutton(root, text="!@#$%", variable=symbols).pack()

tk.Button(root, text="Сгенерировать", command=generate, bg="green", fg="white").pack(pady=10)

generate()
root.mainloop()
