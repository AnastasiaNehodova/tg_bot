from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from recipes import Recipe
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
recipe = Recipe(url="https://api.edamam.com/api/recipes/v2", app_id=config.APP_ID, 
	app_key=config.APP_KEY, food_app_id=config.FOOD_APP_ID, food_app_key=config.FOOD_APP_KEY)
dp = Dispatcher(bot, storage=storage)
#bot = Bot(token=os.getenv('TOKEN'))
#recipe = Recipe(url="https://api.edamam.com/api/recipes/v2", app_id=os.getenv('APP_ID'), app_key=os.getenv('APP_KEY'))
