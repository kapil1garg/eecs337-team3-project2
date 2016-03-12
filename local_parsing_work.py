''' this file will transform the string dictionary from get_recipetext_from_html(url) '''
from __future__ import division
from get_recipetext_from_html import get_recipetext_from_html
import re
import nltk
import json
from nltk.stem.porter import PorterStemmer

ingredients_name_list = ["shallot"]
ingredients_stop_words = ['strip']
stemmer = PorterStemmer()

URL = ["http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/",
"http://allrecipes.com/recipe/42964/awesome-korean-steak/?internalSource=recipe%%20hub&referringId=17833&referringContentType=recipe%%20hub"
]


def get_basic_ingredients():
	basic_ingredients = []
	return basic_ingredients

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
		total = 'user-adjusted'
	return total

def parse_measurement(raw_ingredient):
	# the default measurement
	measurement = re.findall(r'\d (\w+) ', raw_ingredient)
	# remove plural
	if measurement:
		measurement = re.findall(r'(\w+?)s?$', measurement[0])
	if measurement and measurement[0] not in ingredients_name_list:
		measurement = measurement[0]
	else:
		measurement = 'unit'
	return measurement

def remove_quantity_measurement_bracket(words, current_measurement):
	new_words = []
	bracket_tag = False
	for word in words:
		if word == '(':
			bracket_tag = True
		if word == ')':
			bracket_tag = False
		if word.isalpha() and current_measurement not in word and not bracket_tag:
			new_words.append(word)
	return new_words

def parse_ingredient_others(raw_ingredient, current_measurement):
	words = nltk.word_tokenize(raw_ingredient)
	words = remove_quantity_measurement_bracket(words, current_measurement)
	words = nltk.pos_tag(words)
	print words
	name = []
	descriptor = []
	preparation = []
	name_tag = 0 # 0 stands for initial status, 1 for name, 2 for end name
	for word in words:
		if 'NN' in word[1] and name_tag != 2 or name_tag == 2 and 'JJ' in word[1]:
			name_tag = 1
			name.append(stemmer.stem(word[0])) # default method to stem the word, would be better to use dictionary
		else:	
			if word[1] == 'RB' or 'VB' in word[1]:
				preparation.append(word[0])
			elif 'JJ' in word[1] and name_tag != 2:
				descriptor.append(word[0])
			elif 'CC' in word[1]:
				name_tag = 0
			if name_tag == 1:
				name_tag == 2
	return ' '.join(name), ' '.join(descriptor), ' '.join(preparation)

def parse_ingredient(raw_ingredient):
	# quantity
	ingredient = {}
	quantity = parse_quantity(raw_ingredient)
	ingredient['quantity'] = quantity
	# measurement
	measurement = parse_measurement(raw_ingredient)
	ingredient['measurement'] = measurement
	# name, descriptor, preparation
	name, descriptor, preparation = parse_ingredient_others(raw_ingredient, measurement)
	ingredient['name'] = name
	ingredient['descriptor'] = descriptor
	ingredient['preparation'] = preparation
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
	recipe = get_recipetext_from_html(URL[0])
	print json.dumps(recipe, indent = 4)
	recipe = get_parsed_recipe(recipe)
	print json.dumps(recipe, indent = 4)
	return

if __name__ == "__main__":
	main() 