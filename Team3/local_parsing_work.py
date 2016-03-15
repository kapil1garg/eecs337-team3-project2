"""this file will transform the string dictionary from get_recipetext_from_html(url)"""
from __future__ import division
import json
import re
import os

import nltk
from get_recipetext_from_html import get_recipetext_from_html

NOUN_STOP_WORDS = ['strips', 'strip', 'can']
VERB_STOP_WORDS = ['taste']
MISC_STOP_WORDS = ['to', 'of', 'into', 'and', 'or']
ADJ_STOP_WORDS = ['small', 'big', 'boneless']
STOP_WORDS = set(NOUN_STOP_WORDS + MISC_STOP_WORDS + VERB_STOP_WORDS)
PREPARATION_LIST = set(['cut', 'slice', 'mix', 'chopped', 'minced'])

CURRENT_WORKING_PATH = os.path.dirname(os.path.abspath(__file__))

URL = [
    'http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/',
    'http://allrecipes.com/recipe/42964/awesome-korean-steak/?internalSource=recipe%%20hub&referringId=17833&referringContentType=recipe%%20hub',
    'http://allrecipes.com/recipe/7399/tres-leches-milk-cake/',
    'http://allrecipes.com/recipe/213742/meatball-nirvana/'
]

def get_primary_methods():
    with open(os.path.join(CURRENT_WORKING_PATH,'data/cooking-methods_db.json')) as filedata:
        data = json.load(filedata)
    data = data["cooking-methods"]
    return data

def get_cooking_tools():
    with open(os.path.join(CURRENT_WORKING_PATH,'data/cooking-tools_db.json')) as filedata:
        data = json.load(filedata)
    data = data["cooking-tools"]
    return data

def get_cooking_verbs():
    with open(os.path.join(CURRENT_WORKING_PATH,'data/cooking-verbs_db.json')) as filedata:
        data = json.load(filedata)
    data = data["cooking-verbs"]
    return data

def get_basic_ingredients():
    with open(os.path.join(CURRENT_WORKING_PATH,'data/ingredients.json')) as filedata:
        data = json.load(filedata)
    data = data.keys()
    basic_ingredients = [ingredient.lower() for ingredient in data]
    split_ingredients = []
    for ingredient in basic_ingredients:
        split_ingredients = split_ingredients + ingredient.split()
    return split_ingredients

INGREDIENTS = get_basic_ingredients()
COOKING_VERBS = get_cooking_verbs()
COOKING_TOOLS = get_cooking_tools()
PRIMARY_COOKING_METHODS = get_primary_methods()

def parse_quantity(raw_ingredient):
    # deal with fraction part
    fraction = re.findall(r'(\d+)/(\d+)', raw_ingredient)
    if fraction:
        fraction = int(fraction[0][0]) / int(fraction[0][1])
    else:
        fraction = 0.0

    # deal with int part
    integer = re.findall(r'^(\d+) ', raw_ingredient)
    if integer:
        integer = int(integer[0])
    else:
        integer = 0

    # output correct total based on quantity (numeric value or user defined)
    total_quantity = fraction + integer
    if total_quantity == 0:
        return 0
    else:
        return total_quantity

def parse_measurement(raw_ingredient, basic_ingredients):
    # the default measurement
    measurement = re.findall(r'\d (\w+) ', raw_ingredient)
    
    # for irregular measuremtn
    if measurement and len(measurement[0].split())>2:
        measurement = ""

    # remove plural
    if measurement:
        measurement = re.findall(r'(\w+?)s?$', measurement[0])
        if measurement == 'pound':
            measurement = 'pounds'
    if measurement and measurement[0] not in basic_ingredients and measurement[0] not in ADJ_STOP_WORDS:
        measurement = measurement[0]
    else:
        measurement = 'unit'
        if 'salt' in raw_ingredient or 'pepper' in raw_ingredient or 'parsley' in raw_ingredient:
            measurement = 'to taste'
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
            if word[0] in PREPARATION_LIST or ('VB' in word[1] and word[0] not in VERB_STOP_WORDS):
                preparation.append(word[0])
            elif 'RB' in word[1]:
                prep_description.append(word[0])
            elif word[0] not in STOP_WORDS:
                descriptor.append(word[0])

    return ' '.join(name), ' '.join(descriptor), ' '.join(preparation), ' '.join(prep_description)

def parse_ingredient(raw_ingredient, basic_ingredients):
    # firstly get the content in brackets
    brackets_content = re.findall(r'\((.*)\)', raw_ingredient)

    # quantity
    ingredient = {}
    quantity = parse_quantity(raw_ingredient)
    ingredient['quantity'] = quantity

    # check if the concrete answer is in the brackets
    special_quantity = 0
    if len(brackets_content) > 0:
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
    name, descriptor, preparation, prep_description = parse_ingredient_others(raw_ingredient,
                                                                              measurement,
                                                                              basic_ingredients)
    '''
    if not descriptor:
        descriptor = 'none'
    if not preparation:
        preparation = 'none'
    if not prep_description:
        prep_description = 'none'
    '''
    ingredient['name'] = name
    ingredient['descriptor'] = descriptor
    ingredient['preparation'] = preparation
    ingredient['prep-description'] = prep_description
    return ingredient

def get_parsed_methods(directions, cooking_verbs, primary_methods):
    methods = []
    words = []
    bigrams = []
    for direction in directions:
        words_per_sent = nltk.word_tokenize(direction)
        words_per_sent = [word.lower() for word in words_per_sent if word.isalpha()]
        bigrams_per_sent = list(nltk.bigrams(words_per_sent))
        words.append(words_per_sent)
        bigrams.append(bigrams_per_sent)

    for words_per_sent in words:
        for word in words_per_sent:
            if word in cooking_verbs:
                methods.append(word)

    for bigrams_per_sent in bigrams:
        for bigram in bigrams_per_sent:
            if ' '.join(bigram) in cooking_verbs:
                methods.append(' '.join(bigram))

    p_methods = []
    for method in methods:
        if method in primary_methods:
            p_methods.append(method)

    p_method = nltk.FreqDist(p_methods).most_common(1)
    if p_method:
        p_method = p_method[0][0]
    else:
        p_method = 'None'
    methods = list(set(methods))
    return methods, p_method

def get_parsed_tools(directions, cooking_tools):
    tools = []
    directions = ' '.join(directions)
    for tool in cooking_tools:
        for key in tool:
            if key in directions:
                tools.append(key)
                continue
            otherwords = tool[key]["verbs"] + tool[key]["alternatives"]
            for otherword in otherwords:
                if otherword in directions:
                    tools.append(key)
                    break
    return list(set(tools))

def get_parsed_recipe(recipe, basic_ingredients=None, cooking_verbs=None,
                      cooking_tools=None, primary_methods=None):
    # check if optional values are None
    if basic_ingredients is None:
        basic_ingredients = INGREDIENTS
    if cooking_verbs is None:
        cooking_verbs = COOKING_VERBS
    if cooking_tools is None:
        cooking_tools = COOKING_TOOLS
    if primary_methods is None:
        primary_methods = PRIMARY_COOKING_METHODS

    raw_ingredients = recipe['ingredients']

    # parse the ingredient
    ingredients = []
    for raw_ingredient in  raw_ingredients:
        ingredients.append(parse_ingredient(raw_ingredient, basic_ingredients))
    recipe['ingredients'] = ingredients

    directions = recipe['directions']

    # parse the method
    recipe['cooking methods'], recipe['primary cooking method'] = \
        get_parsed_methods(directions, cooking_verbs, primary_methods)

    # parse the tool
    recipe['cooking tools'] = get_parsed_tools(directions, cooking_tools)
    return recipe

def main():
    recipe_url = get_recipetext_from_html(URL[3])
    recipe = get_parsed_recipe(recipe_url)
    print json.dumps(recipe, indent=4)

if __name__ == "__main__":
    main()
