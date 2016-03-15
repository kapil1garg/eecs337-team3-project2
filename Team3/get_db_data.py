"""Script to pull data from JSON DBs into python objects"""
import json
import io

class CookingTool(object):
    def __init__(self, name='', alternatives=None, verbs=None):
        # assign value to class variables
        self.name = name

        if alternatives is None:
            self.alternatives = []
        else:
            self.alternatives = alternatives

        if verbs is None:
            self.verbs = []
        else:
            self.verbs = verbs

    def get_name(self):
        return self.name

    def get_alternatives(self):
        return self.alternatives

    def get_verbs(self):
        return self.verbs

def get_db_cooking_methods():
    """Pulls cooking methods from externally defined dictionary"""
    with io.open('data/cooking-methods_db.json') as datafile:
        data = json.load(datafile)

    return [method for method in data['cooking-methods']]

def get_db_cooking_tools():
    """Pulls cooking tools from externally defined dictionary"""
    with io.open('data/cooking-tools_db.json') as datafile:
        data = json.load(datafile)

    json_list = data['cooking-tools']
    cooking_tools = []
    for tool in json_list:
        name = tool.keys()[0]
        alternatives = tool[name]['alternatives']
        verbs = tool[name]['verbs']
        cooking_tools.append(CookingTool(name, alternatives, verbs))

    return cooking_tools

def get_db_cooking_verbs():
    """Pulls cooking words from externally defined dictionary"""
    with io.open('data/cooking-verbs_db.json') as datafile:
        data = json.load(datafile)

    return [verb for verb in data['cooking-verbs']]

def get_db_transforms():
    """Pulls all diet and health transformations from externally defined dictionaries"""
    # get all diet dictionaries
    with io.open('data/diet-transform_db.json') as datafile:
        diet_data = json.load(datafile)

    diet_transform_dict = diet_data['diet-transforms']
    to_omnivore = diet_transform_dict['toOmnivore']
    to_pescatarian = diet_transform_dict['toPescatarian']
    to_vegetarian = diet_transform_dict['toVegetarian']
    to_vegan = diet_transform_dict['toVegan']
    to_vegan_animal_products = diet_transform_dict['toVeganAnimalProducts']
    to_lactose_free = diet_transform_dict['toLactoseFree']
    to_gluten_free = diet_transform_dict['toGlutenFree']

    # get all health dictionaries
    with io.open('data/health-transform_db.json') as datafile:
        health_data = json.load(datafile)

    health_transform_dict = health_data['health-transforms']
    to_low_calorie = health_transform_dict['toLowCalorie']
    to_low_fat = health_transform_dict['toLowFat']
    to_low_sodium = health_transform_dict['toLowSodium']
    to_low_carb = health_transform_dict['toLowCarb']
    to_low_gi = health_transform_dict['toLowGlycemicIndex']

    # get easy-to-diy dictionary
    with io.open('data/easy-to-diy_db.json') as datafile:
        easy_diy_data = json.load(datafile)

    easy_diy_dict = easy_diy_data['easy-to-diy']

    return (to_omnivore, to_pescatarian, to_vegetarian, to_vegan, to_vegan_animal_products, \
            to_lactose_free, to_gluten_free, \
            to_low_calorie, to_low_fat, to_low_sodium, to_low_carb, to_low_gi, easy_diy_dict)

def get_db_food_textures():
    with io.open('data/food-textures_db.json') as datafile:
        data = json.load(datafile)

    texture_dict = data['food-textures']

    fish_textures = texture_dict['fish']
    meat_textures = texture_dict['meat']
    plant_textures = texture_dict['plantBased']

    return (meat_textures, fish_textures, plant_textures)

def main():
    # cooking_methods = get_db_cooking_methods()
    # cooking_tools = get_db_cooking_tools()
    # cooking_verbs = get_db_cooking_verbs()

    # to_omnivore, to_pescatarian, to_vegetarian, to_vegan, to_vegan_animal_products, \
    # to_lactose_free, to_gluten_free = get_db_transforms()

    # meat_textures, fish_textures, plant_textures = get_db_food_textures()
    return

if __name__ == '__main__':
    main()
