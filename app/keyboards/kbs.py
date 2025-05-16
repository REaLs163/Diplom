from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Определяем reply клавиатуру
main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Анализ и обработка отзывов")],[KeyboardButton(text="Закончить работу")],],resize_keyboard=True)
analiz_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить работу")]], resize_keyboard=True)