""" Script to pull data from JSON DBs into python objects"""
import json
import io

def get_db_cooking_methods():
    with io.open("data/cooking-methods_db.json") as datafile:
        data = json.load(datafile)

    return [method for method in data["cooking-methods"]]

class CookingTool(object):
    def __init__(self, name="", alternatives=None, verbs=None):
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

def get_db_cooking_tools():
    with io.open("data/cooking-tools_db.json") as datafile:
        data = json.load(datafile)

    json_list = data["cooking-tools"]
    cooking_tools = []
    for tool in json_list:
        name = tool.keys()[0]
        alternatives = tool[name]["alternatives"]
        verbs = tool[name]["verbs"]
        cooking_tools.append(CookingTool(name, alternatives, verbs))

    return cooking_tools

def get_db_cooking_verbs():
    with io.open("data/cooking-verbs_db.json") as datafile:
        data = json.load(datafile)

    return [verb for verb in data["cooking-verbs"]]

def get_db_transforms():
    with io.open("data/diet-transform_db.json") as datafile:
        data = json.load(datafile)

    transform_dict = data["diet-transforms"]

    to_omnivore = transform_dict["toOmnivore"]
    to_pescatarian = transform_dict["toPescatarian"]
    to_vegetarian = transform_dict["toVegetarian"]
    to_vegan = transform_dict["toVegan"]
    to_vegan_animal_products = transform_dict["toVeganAnimalProducts"]
    to_lactose_free = transform_dict["toLactoseFree"]
    to_gluten_free = transform_dict["toGlutenFree"]

    return (to_omnivore, to_pescatarian, to_vegetarian, to_vegan, to_vegan_animal_products, \
            to_lactose_free, to_gluten_free)

def get_db_food_textures():
    with io.open("data/food-textures_db.json") as datafile:
        data = json.load(datafile)

    texture_dict = data["food-textures"]

    fish_textures = texture_dict["fish"]
    meat_textures = texture_dict["meat"]
    plant_textures = texture_dict["plantBased"]

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
