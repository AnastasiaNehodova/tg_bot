from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/КБЖУ_витамины_микроэлементы_продукта')
b2 = KeyboardButton('/Рецепты_по_набору_продуктов')
b3 = KeyboardButton('/Похожий_продукт')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3)