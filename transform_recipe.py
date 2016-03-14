"""Transforms recipe along specified parameter"""
from __future__ import division
import json

from get_recipetext_from_html import get_recipetext_from_html
import local_parsing_work as ParseRecipe
import get_db_data as DBImporter

TEST_URLS = [
    'http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/',
    'http://allrecipes.com/recipe/42964/awesome-korean-steak/?internalSource=recipe%%20hub&referringId=17833&referringContentType=recipe%%20hub',
    'http://allrecipes.com/recipe/7399/tres-leches-milk-cake/'
]

OMNIVORE_DICT, PESC_DICT, VEGETARIAN_DICT, VEGAN_DICT, \
    VEGAN_ANIMAL_PRODUCTS_DICT = DBImporter.get_db_transforms()

MEAT_TEXTURES, FISH_TEXTURES, PLANT_TEXTURES = DBImporter.get_db_food_textures()

def transformation_handler(recipe, transform_type):
    """
    Handler which calls transform_recipe with recipe and correct transformation dictionary
    """
    pass

def transform_recipe(recipe, transformation_dict):
    """
    Transforms input recipe from current state into desired transformation via transformation_dict
    """
    pass

def main():
    print OMNIVORE_DICT
    print MEAT_TEXTURES
    for i in TEST_URLS:
        print 'Parsing Recipe from ' + i
        get_url_data = get_recipetext_from_html(i)
        print json.dumps(ParseRecipe.get_parsed_recipe(get_url_data), indent=4)

if __name__ == '__main__':
    main()
