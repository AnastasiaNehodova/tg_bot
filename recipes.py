# data_image - список с url картинок
# data_label - список с названием рецептов
# data_ingridients - Список со списком ингредиентов
# data_cal - Список с калорийностью рецептов
# data_url - Список с url рецептов

import requests
from deep_translator import GoogleTranslator


class Recipe():
    def __init__(self, url, app_id, app_key, food_app_id, food_app_key):
        self.url, self.app_id, self.app_key, self.food_app_id, self.food_app_key = url, app_id, app_key, food_app_id, food_app_key

    def get_dict(self, ingridients):
        ingridients = GoogleTranslator('ru', 'en').translate(ingridients)
        params_dict = {
            "type": "public",
            "app_id": self.app_id,
            "app_key": self.app_key,
            "q": ingridients,
            "imageSize": "SMALL",
            "random": "false"}
        response = requests.get(self.url, params_dict)
        response = response.json()
        return response

    def get_lists(self, data_dict):
        hits = data_dict['hits']
        temp_label_str = ''
        temp_image_str = ''
        temp_cal_str = ''
        temp_url_str = ''
        data_ingridients = []
        for key in hits:
            temp_label = key['recipe']['label']
            temp_image = key['recipe']['image']
            temp_ingridients = key['recipe']['ingredientLines']
            temp_cal = key['recipe']['calories']
            temp_weight = key['recipe']['totalWeight']
            temp_cal = (temp_cal / temp_weight) * 100
            temp_url = key['recipe']['url']
            temp_label_str = temp_label_str + temp_label + '<<<<>>>>'
            temp_image_str = temp_image_str + temp_image + '<<<<>>>>'
            data_ingridients.append(temp_ingridients)
            temp_cal_str = temp_cal_str + str(temp_cal) + '<<<<>>>>'
            temp_url_str = temp_url_str + str(temp_url) + '<<<<>>>>'
        data_cal = temp_cal_str.split('<<<<>>>>')
        data_image = temp_image_str.split('<<<<>>>>')
        data_label = temp_label_str.split('<<<<>>>>')
        data_url = temp_url_str.split('<<<<>>>>')
        return data_image, data_label, data_ingridients, data_cal, data_url

    def get_error(self, data_dict):
        if data_dict['hits']:
            return True
        else:
            return False

    def get_image_dict(self, food):
        food = GoogleTranslator('ru','en').translate(food)
        params_dict = {
            "type":"public",
            "app_id":self.food_app_id,
            "app_key":self.food_app_key,
            "ingr":food}
        image_dict = requests.get('https://api.edamam.com/api/food-database/v2/parser',params_dict)
        image_dict = image_dict.json()
        return image_dict

    def food_image_parse(self,food):
        image_dict = self.get_image_dict(food)
        parsed = image_dict['parsed']
        for key in parsed:
            image = key['food']['image']
        return image

    def get_image_error(self, food):
        image_dict = self.get_image_dict(food)
        if image_dict['parsed']:
            return True
        else:
            return False

# data = Reciept(url, app_id, app_key)
# data_dict = data.get_dict(ingridients)
# data.get_error(data_dict) # -True значит рецепты нашлись)
# data_image,data_label,data_ingridients,data_cal,data_url = data.get_lists(data_dict)
# image = reciept.food_image_parse(ingridients) # - Получаем картинку
# data.get_image_error() # -True значит картинка нашлась)


