from aiogram import types, Dispatcher
from create_bot import dp, bot, recipe
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from requests import get
import os
from deep_translator import GoogleTranslator
import pandas as pd

class FSMClient(StatesGroup):
	product_for_nutrition = State()
	number_recipes = State()
	products_for_recipe = State() 
	product_for_similar_products = State()
	product_from_list_for_similar_products = State()

async def command_start(message : types.Message):
	try:
		await bot.send_message(message.from_user.id, 'Приветствую тебя, {first_name} {last_name}! Смотри, что я могу тебе показать.'
			.format(first_name=message.from_user.first_name, last_name=message.from_user.last_name),
			reply_markup=kb_client)
		await message.delete()
	except:
		await message.reply('Общение с ботом через ЛС, напиши ему:\nhttps://t.me/FoodNutritionAndRecipesBot')

async def command_nutrition(message : types.Message):
	await FSMClient.product_for_nutrition.set()
	await message.reply('Введи продукт')

async def command_number_recipes(message : types.Message):
	await FSMClient.number_recipes.set()
	await bot.send_message(message.from_user.id, 'Введи количество рецептов')

async def command_similar_products(message : types.Message):
	await FSMClient.product_for_similar_products.set()
	await bot.send_message(message.from_user.id, 'Введи продукт')

async def print_nutrition(message: types.Message, state: FSMContext):
	df = pd.read_csv('data/data_new.csv')
	item = message.text.lower().strip()

	try:
		res = df.loc[df['Desk3'] == item]
		cc = res.iloc[0]
		try:
			await bot.send_photo(message.from_user.id, get(recipe.food_image_parse(item)).content)
		except: 
			await bot.send_photo(message.from_user.id, photo=open('images/no_photo.jpg', 'rb'))
		await bot.send_message(message.from_user.id, 
			'ПРОДУКТ:\t{}\n\nКалорийность продукта:\t{}\nБелки:\t{}\nУглеводы:\t{}\nЖиры:\t{}\n\nСОДЕРЖАНИЕ ВИТАМИНОВ:\n\nВитамин A:\t{}\nВитамин B6:\t{}\nВитамин B12:\t{}\nВитамин C:\t{}\nВитамин D:\t{}\nВитамин E:\t{}\nВитамин K:\t{}\nЖелезо:\t{}\nКальций:\t{}\nМагний:\t{}\nФолиевая кислота:\t{}'.format(item, 
				cc['Energy_In_Kilogram_Calorie'], 
				cc['Protein_In_Grams'], 
				cc['Carbohydrate_In_Grams'],
				round((cc['Energy_In_Kilogram_Calorie'] - cc['Protein_In_Grams']*4 - cc['Carbohydrate_In_Grams']*4)/9, 2),
				cc['Vit_A_In_International_Unit'], 
				cc['Vit_B6_In_Miligrams'], 
				cc['Vit_B12_In_Micrograms'], 
				cc['Vit_C_In_Miligrams'], 
				cc['Vit_D_In_International_Unit'], 
				cc['Vit_E_In_Miligrams'],
				cc['Vit_K_In_Micrograms'], 
				cc['Iron_In_Miligrams'], 
				cc['Calcium_In_Miligrams'], 
				cc['Magnesium_In_Miligrams'], 
				cc['Folic_Acid_In_Micrograms']))
	except IndexError:
		try:
			res = df.loc[df['Desk3'].str.contains(item)]
			cc = res.iloc[0]
			try:
				await bot.send_photo(message.from_user.id, get(recipe.food_image_parse(cc['Desk3'])).content)
			except: 
				await bot.send_photo(message.from_user.id, photo=open('no_photo.jpg', 'rb'))

			await bot.send_message(message.from_user.id,
				'ПРОДУКТ:\t{}\n\nКалорийность продукта:\t{}\nБелки:\t{}\nУглеводы:\t{}\nЖиры:\t{}\n\nСОДЕРЖАНИЕ ВИТАМИНОВ:\n\nВитамин A:\t{}\nВитамин B6:\t{}\nВитамин B12:\t{}\nВитамин C:\t{}\nВитамин D:\t{}\nВитамин E:\t{}\nВитамин K:\t{}\nЖелезо:\t{}\nКальций:\t{}\nМагний:\t{}\nФолиевая кислота:\t{}'.format(cc['Desk3'], 
				cc['Energy_In_Kilogram_Calorie'], 
				cc['Protein_In_Grams'], 
				cc['Carbohydrate_In_Grams'],
				round((cc['Energy_In_Kilogram_Calorie'] - cc['Protein_In_Grams']*4 - cc['Carbohydrate_In_Grams']*4)/9, 2),
				cc['Vit_A_In_International_Unit'], 
				cc['Vit_B6_In_Miligrams'], 
				cc['Vit_B12_In_Micrograms'], 
				cc['Vit_C_In_Miligrams'], 
				cc['Vit_D_In_International_Unit'], 
				cc['Vit_E_In_Miligrams'],
				cc['Vit_K_In_Micrograms'], 
				cc['Iron_In_Miligrams'], 
				cc['Calcium_In_Miligrams'], 
				cc['Magnesium_In_Miligrams'], 
				cc['Folic_Acid_In_Micrograms']))
		except IndexError:
			await bot.send_photo(message.from_user.id, photo=open('images/lebedev.jpg', 'rb'))
			await bot.send_message(message.from_user.id, "Пока не знаю характеристики этого продукта :( ")
	await state.finish()


async def input_number_of_recipes(message: types.Message, state: FSMContext):
	if message.text.strip().isdigit():
		counter = int(message.text)
	else:
		counter = 1
	async with state.proxy() as data:
		data['counter'] = max(1, counter)
	await FSMClient.next()
	await bot.send_message(message.from_user.id, 'Введи список из одного или более продуктов')

	
async def print_recipe(message: types.Message, state: FSMContext):
	recipe_dict = recipe.get_dict(message.text)   # Получаем словарь рецептов
	async with state.proxy() as data:
		counter = data['counter']
	if recipe.get_error(recipe_dict):
		recipe_image, recipe_label, recipe_ingridients, recipe_cal, recipe_url = recipe.get_lists(recipe_dict)  # Возвращаем списки из словаря
		for i in range(int(counter)):  # Вывод сообщений, описание того что хранится в списках есть в reciepts.py
			await bot.send_photo(message.from_user.id, get(recipe_image[i]).content)
			await bot.send_message(message.from_user.id, GoogleTranslator('en','ru').translate(recipe_label[i]))
			recipe_ingridients[i] = ",".join(recipe_ingridients[i])
			recipe_ingridients[i] = recipe_ingridients[i].replace('.','??')
			recipe_ingridients[i] = GoogleTranslator('en','ru').translate(recipe_ingridients[i])
			recipe_ingridients[i] = recipe_ingridients[i].replace('??', '.')
			recipe_ingridients[i] = recipe_ingridients[i].replace(', ', '\n')
			recipe_ingridients[i] = recipe_ingridients[i].replace(',', '\n')
			await bot.send_message(message.from_user.id, recipe_ingridients[i])
			button_url = types.InlineKeyboardMarkup(row_width=2)
			button_url.add(types.InlineKeyboardButton('Подробнее', url=recipe_url[i]))
			await bot.send_message(message.from_user.id, "Калорийность {} ккал на 100 грамм".format(int(float(recipe_cal[i]))), reply_markup=button_url)
	else:
		await bot.send_photo(message.from_user.id, photo=open('images/lebedev.jpg', 'rb'))
		await bot.send_message(message.from_user.id, "Ничего не могу найти с такими ингредиентами :(")
	await state.finish()

async def print_similar_products(message: types.Message, state: FSMContext):
	data = pd.read_csv('data/similar.csv')
	key = message.text.lower().strip()
	data2 = data.loc[data['product'] == key]
	if len(data2) > 0:
		sim = data2.iloc[0]['similar']
		await bot.send_message(message.from_user.id, 'Похожий продукт:')
		await bot.send_message(message.from_user.id, sim)
		await state.finish()
	elif len(data2) == 0:
		data3 = data.loc[data['product'].str.contains(key)]
		bn = data3['product']
		if len(bn) == 0:
			key = key[:3]
			data5 = data.loc[data['product'].str.contains(key)]
			bn5 = data5['product']
			if len(bn5) > 0:
				await bot.send_message(message.from_user.id, "Возможно ты имел ввиду:")
				for i in range(len(bn5)):
					await bot.send_message(message.from_user.id, bn5.iloc[i])
				await FSMClient.next()
				await bot.send_message(message.from_user.id, 'Введи продукт из списка')
			else:
				await bot.send_photo(message.from_user.id, photo=open('images/lebedev.jpg', 'rb'))
				await bot.send_message(message.from_user.id, "Не знаю такой продукт :(")
				await state.finish() 

		if len(bn) > 0:
			await bot.send_message(message.from_user.id, "Возможно ты имел ввиду:")
			for i in range(len(bn)):
				await bot.send_message(message.from_user.id, bn.iloc[i])
			await FSMClient.next()
			await bot.send_message(message.from_user.id, 'Введи продукт из списка')
	else:
		await bot.send_photo(message.from_user.id, photo=open('images/lebedev.jpg', 'rb'))
		await bot.send_message(message.from_user.id, "Не знаю такой продукт :(")
		await state.finish() 

async def print_similar_products_for_product_from_list(message: types.Message, state: FSMContext):
	data = pd.read_csv('data/similar.csv')
	key = message.text.lower().strip()
	data2 = data.loc[data['product'] == key]
	if len(data2) > 0:
		sim = data2.iloc[0]['similar']
		await bot.send_message(message.from_user.id, 'Похожий продукт:')
		await bot.send_message(message.from_user.id, sim)
	else:
		await bot.send_photo(message.from_user.id, photo=open('images/lebedev.jpg', 'rb'))
		await bot.send_message(message.from_user.id, "Не знаю такой продукт :(")
	await state.finish() 

def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(command_start, commands=['старт', 'помощь', 'start', 'help'], state=None)
	dp.register_message_handler(command_nutrition, commands=['КБЖУ_витамины_микроэлементы_продукта'], state=None)
	dp.register_message_handler(command_number_recipes, commands=['Рецепты_по_набору_продуктов'], state=None)
	dp.register_message_handler(command_similar_products, commands=['Похожий_продукт'], state=None)
	dp.register_message_handler(print_nutrition, state=FSMClient.product_for_nutrition)
	dp.register_message_handler(input_number_of_recipes, state=FSMClient.number_recipes)		
	dp.register_message_handler(print_recipe, state=FSMClient.products_for_recipe)
	dp.register_message_handler(print_similar_products, state=FSMClient.product_for_similar_products)
	dp.register_message_handler(print_similar_products_for_product_from_list, state=FSMClient.product_from_list_for_similar_products)
