''' this file will transform the string dictionary from get_recipetext_from_html(url) '''
from __future__ import division
from get_recipetext_from_html import get_recipetext_from_html
import re
import nltk
import json
from nltk.stem.porter import PorterStemmer

noun_stop_words = ['strips', 'strip', 'can']
verb_stop_words = ['taste']
other_stopwords = ['to', 'of', 'into', 'and', 'or']
stemmer = PorterStemmer()
stopwords = noun_stop_words+other_stopwords+verb_stop_words
preparation_list = ['cut', 'slice', 'mix', 'chopped']


URL = ["http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/",
"http://allrecipes.com/recipe/42964/awesome-korean-steak/?internalSource=recipe%%20hub&referringId=17833&referringContentType=recipe%%20hub",
"http://allrecipes.com/recipe/7399/tres-leches-milk-cake/"
]


def get_basic_ingredients():
	with open('ingredients.json') as filedata:
		data = json.load(filedata)
	data = data.keys()
	basic_ingredients = [ingredient.lower() for ingredient in data]
	split_ingredients = []
	for ingredient in basic_ingredients:
		split_ingredients = split_ingredients + ingredient.split()
	return split_ingredients

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

def parse_measurement(raw_ingredient, basic_ingredients):
	# the default measurement
	measurement = re.findall(r'\d (\w+) ', raw_ingredient)
	# remove plural
	if measurement:
		measurement = re.findall(r'(\w+?)s?$', measurement[0])
	if measurement and measurement[0] not in basic_ingredients:
		measurement = measurement[0]
	else:
		measurement = 'unit'
	return measurement

def remove_quantity_measurement_bracket(words, current_measurement):
	new_words = []
	bracket_tag = False
	for sent in words:
		sent_words = []
		for word in sent:
			if word == '(':
				bracket_tag = True
			if word == ')':
				bracket_tag = False
			if word.isalpha() and current_measurement not in word and not bracket_tag:
				sent_words.append(word.lower())
		new_words.append(sent_words)
	return new_words

def parse_ingredient_others(raw_ingredient, current_measurement, basic_ingredients):
	sents = raw_ingredient.split(',')
	words = [nltk.word_tokenize(sent) for sent in sents]
	words = remove_quantity_measurement_bracket(words, current_measurement)
	# get the name of ingredient here
	# since there are word and in basic_ingredients, we don't need to deal with this case
	name = []
	rests = []
	has_name = True
	for sent in words:
		rest = []
		contain_name = False
		for word in sent:
			if has_name and word in basic_ingredients:
				name.append(word)
				contain_name = True
			elif has_name and word[:-1] in basic_ingredients:
				name.append(word[:-1])
				contain_name = True
			elif word:
				rest.append(word)
		if contain_name:
			has_name = False
		if rest:
			rests.append(rest)
	descriptor = []
	preparation = []
	prep_description = []
	for sent in rests:
		tagged_sent = nltk.pos_tag(sent)
		for word in tagged_sent:
			if word[0] in preparation_list or 'VB' in word[1] and word[0] not in verb_stop_words:
				preparation.append(word[0])
			elif 'RB' in word[1]:
				prep_description.append(word[0])
			elif word[0] not in stopwords:
				descriptor.append(word[0])

	return ' '.join(name), ' '.join(descriptor), ' '.join(preparation), ' '.join(prep_description)

def parse_ingredient(raw_ingredient, basic_ingredients):
	# fisrtly get the content in brackets
	brackets_content = re.findall(r'\((.*)\)', raw_ingredient)
	# quantity
	ingredient = {}
	quantity = parse_quantity(raw_ingredient)
	ingredient['quantity'] = quantity
	# if the concrete anster is in the brackets
	special_quantity = 0
	if len(brackets_content)>0:
		brackets_content = brackets_content[0]
		special_quantity = parse_quantity(brackets_content)
	if special_quantity != 0:
		ingredient['quantity'] = special_quantity


	# measurement
	measurement = parse_measurement(raw_ingredient, basic_ingredients)
	ingredient['measurement'] = measurement
	# measurement in brackets
	if special_quantity != 0:
		ingredient['measurement'] = ' '.join(re.findall(r'[a-z]+', brackets_content))




	# name, descriptor, preparation
	name, descriptor, preparation, prep_description = parse_ingredient_others(raw_ingredient, measurement, basic_ingredients)
	if not descriptor:
		descriptor = 'none'
	if not preparation:
		preparation = 'none'
	if not prep_description:
		prep_description = 'none'
	ingredient['name'] = name
	ingredient['descriptor'] = descriptor
	ingredient['preparation'] = preparation
	ingredient['prep_description'] = prep_description
	print "In Progress - Finish One Piece of Ingredient"
	return ingredient


def get_parsed_recipe(recipe, basic_ingredients):
	raw_ingredients = recipe['ingredients']
	# parse the ingredient
	ingredients = []
	for raw_ingredient in  raw_ingredients:
		ingredients.append(parse_ingredient(raw_ingredient, basic_ingredients))
	recipe['ingredients'] = ingredients
	# parse the tool

	return recipe

def main():
	#basic_ingredients = get_basic_ingredients()
	#recipe = get_recipetext_from_html(URL[2])
	#print json.dumps(recipe, indent = 4)
	#recipe = get_parsed_recipe(recipe, basic_ingredients)
	#print json.dumps(recipe, indent = 4)

	return

if __name__ == "__main__":
	main() 