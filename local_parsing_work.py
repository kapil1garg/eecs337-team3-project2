''' this file will transform the string dictionary from get_recipetext_from_html(url) '''
from __future__ import division
from get_recipetext_from_html import get_recipetext_from_html
import re
import json

URL = "http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/"

def parse_quantity(raw_ingredient):
	# deal with fraction part 
	fraction = re.findall('(\d+)/(\d+)', raw_ingredient)
	if fraction:
		fraction = int(fraction[0][0])/ int(fraction[0][1])
	else:
		fraction = 0.0
	# deal with int part
	integer = re.findall('^(\d+) ', raw_ingredient)
	if integer:
		integer = int(integer[0])
	else:
		integer = 0
	total = fraction+integer
	if total == 0:
		total = 'unspecified'
	return total

def parse_measurement(raw_ingredient):
	# the default measurement
	measurement = re.findall(r'\d (\w+) ', raw_ingredient)
	# remove plural
	if measurement:
		measurement = re.findall(r'(\w+?)s?$', measurement[0])
	if measurement:
		measurement = measurement[0]
	else:
		measurement = 'unit'
	return measurement

def parse_ingredient(raw_ingredient):
	# quantity
	ingredient = {}
	quantity = parse_quantity(raw_ingredient)
	ingredient['quantity'] = quantity
	# measurement
	measurement = parse_measurement(raw_ingredient)
	ingredient['measurement'] = measurement

	return ingredient


def get_parsed_recipe(recipe):
	raw_ingredients = recipe['ingredients']
	# parse the ingredient
	ingredients = []
	for raw_ingredient in  raw_ingredients:
		ingredients.append(parse_ingredient(raw_ingredient))
	recipe['ingredients'] = ingredients

	return recipe

def main():
	recipe = get_recipetext_from_html(URL)
	print json.dumps(recipe, indent = 4)
	recipe = get_parsed_recipe(recipe)
	print json.dumps(recipe, indent = 4)
	return

if __name__ == "__main__":
	main() 