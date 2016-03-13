""" Script to pull data from JSON DBs into python objects """
import json
import io

def get_db_cooking_methods():

	with io.open("data/cooking-methods_db.json") as datafile:
		data = json.load(datafile)

	return [method for method in data["cooking-methods"]]

class CookingTool():

	def __init__(self, name="", alternatives=[], verbs=[]):
		self.name = name
		self.alternatives = alternatives
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

	transformDict = data["diet-transforms"]

	toOmnivore = transformDict["toOmnivore"]
	toPescatarian = transformDict["toPescatarian"]
	toVegetarian = transformDict["toVegetarian"]
	toVegan = transformDict["toVegan"]
	toVeganAnimalProducts = transformDict["toVeganAnimalProducts"]
	return (toOmnivore, toPescatarian, toVegetarian, toVegan, toVeganAnimalProducts)

def get_db_food_textures():

	with io.open("data/food-textures_db.json") as datafile:
		data = json.load(datafile)

	textureDict = data["food-textures"]

	fishTextures = textureDict["fish"]
	meatTextures = textureDict["meat"]
	plantTextures = textureDict["plantBased"]

	return (meatTextures, fishTextures, plantTextures)

def main():

	COOKING_METHODS = get_db_cooking_methods()

	COOKING_TOOLS = get_db_cooking_tools()

	COOKING_VERBS = get_db_cooking_verbs()

	TO_OMNIVORE, TO_PESCATARIAN, TO_VEGETARIAN, TO_VEGAN, TO_VEGAN_ANIMAL_PRODUCTS = get_db_transforms()

	MEAT_TEXTURES, FISH_TEXTURES, PLANT_TEXTURES = get_db_food_textures()

	return

if __name__ == '__main__':
    main()