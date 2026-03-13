# ui/interface.py
"""
Модуль с настройками интерфейса
"""

# Цвета для приложения
COLORS = {
    'bg': '#f0f0f0',
    'button': '#4CAF50',
    'button_text': 'white',
    'entry_bg': 'white'
}

# Настройки окна
WINDOW = {
    'title': 'Генератор паролей',
    'width': 400,
    'height': 350
}

# Настройки пароля по умолчанию
DEFAULT = {
    'length': 12,
    'min_length': 4,
    'max_length': 32,
    'use_upper': True,
    'use_lower': True,
    'use_digits': True,
    'use_symbols': False
}

# Наборы символов
CHARS = {
    'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'lowercase': 'abcdefghijklmnopqrstuvwxyz',
    'digits': '0123456789',
    'symbols': '!@#$%^&*'
}
