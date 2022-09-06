Телеграм-бота можно найти по ссылке: @FoodNutritionAndRecipesBot либо по имени: Food nutrition and recipes

Запустить меню бота можно с помощью команд /старт /помощь /help /start

Меню содержит 3 пункта выбора:

1. /КБЖУ_витамины_микроэлементы_продукта, ввод: продукт, вывод: картинка продукта (если нашлась), характеристики продукта.

2. /Рецепты_по_набору_продуктов, ввод: количество рецептов, ввод: продукты через пробелы, вывод: фото рецепта, ингредиенты рецепта, ссылка на рецепт в количестве, указанном пользователем.

3. /Похожий продукт, ввод: продукт, возможный ввод: уточненный продукт, вывод: похожий продукт.

data.csv - первоначальные датасет

data_new.csv - преобразованный датасет, используется для определения КБЖУ, витаминов и микроэлементов продукта.

similar.csv - датасет, сформированный для определения похожего продукта.

similar.ipynb - последовательность формирование data_new.csv, similar.csv.

Edamam - Recipe Search API - получение картинки рецепта, ингредиентов рецепта, ссылки на рецепт.

Edamam - Food and Grocery Database API - получение картинки продукта.
