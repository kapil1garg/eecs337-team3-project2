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
    transformation = None
    if transform_type == 'omnivore':
        transformation = transform_recipe(recipe, [PLANT_TEXTURES], OMNIVORE_DICT)
    elif transform_type == 'pescatarian':
        transformation = transform_recipe(recipe, [MEAT_TEXTURES], PESC_DICT)
    elif transform_type == 'vegetarian':
        transformation = transform_recipe(recipe, [MEAT_TEXTURES, FISH_TEXTURES], VEGETARIAN_DICT)
    elif transform_type == 'vegan':
        transformation = transform_recipe(recipe, [MEAT_TEXTURES, FISH_TEXTURES], VEGAN_DICT,
                                          vegan_case=True)

    return transformation

def transform_recipe(recipe, texture_dicts, transformation_dict, vegan_case=False):
    """
    Transforms input recipe from current state into desired transformation via transformation_dict
    """
    substitutes = {}

    for ingredient in recipe['ingredients']:
        texture_value = None

        # check if texture for ingredient exists
        for texture_dict in texture_dicts:
            for texture in texture_dict:
                if texture in ingredient['name']:
                    texture_value = texture_dict[texture]
                    break
            if texture_value is not None:
                break

        # if texture exists, change ingredient
        if texture_value is not None:
            viable_substitutions = transformation_dict[texture_value]
            substitutes[ingredient['name']] = viable_substitutions

        # check if vegan is requested, if so find substitutes
        if vegan_case:
            for food in VEGAN_ANIMAL_PRODUCTS_DICT:
                if food in ingredient['name']:
                    substitutes[ingredient['name']] = VEGAN_ANIMAL_PRODUCTS_DICT[food]
    return substitutes

def main():
    current_recipe = TEST_URLS[0]

    for current_recipe in TEST_URLS:
        print 'Parsing Recipe from ' + current_recipe
        recipe_from_url = get_recipetext_from_html(current_recipe)
        parsed_recipe = ParseRecipe.get_parsed_recipe(recipe_from_url)

        ingredient_list = []
        for i in parsed_recipe['ingredients']:
            ingredient_list.append(i['name'])
        print 'List of ingredients: ' + ', '.join(ingredient_list)

        pesc_subs = transformation_handler(recipe_from_url, 'pescatarian')
        vegetarian_subs = transformation_handler(recipe_from_url, 'vegetarian')
        vegan_subs = transformation_handler(recipe_from_url, 'vegan')

        print 'Pescatarian substitutes: ' + str(pesc_subs)
        print 'Vegetarian substitutes: ' + str(vegetarian_subs)
        print 'Vegan substitutes: ' + str(vegan_subs)
        print

if __name__ == '__main__':
    main()
