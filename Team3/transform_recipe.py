"""Transforms recipe along specified parameter"""
from __future__ import division

from get_recipetext_from_html import get_recipetext_from_html
import local_parsing_work as ParseRecipe
import get_db_data as DBImporter

TEST_URLS = [
    'http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/',
    'http://allrecipes.com/recipe/42964/awesome-korean-steak/?internalSource=recipe%%20hub&referringId=17833&referringContentType=recipe%%20hub',
    'http://allrecipes.com/recipe/7399/tres-leches-milk-cake/'
]

OMNIVORE_DICT, PESC_DICT, VEGETARIAN_DICT, VEGAN_DICT, VEGAN_ANIMAL_PRODUCTS_DICT, \
    LACTOSE_FREE_DICT, GLUTEN_FREE_DICT, LOW_CAL_DICT, LOW_FAT_DICT, LOW_SODIUM_DICT, \
    LOW_CARB_DICT, LOW_GI_DICT = DBImporter.get_db_transforms()

MEAT_TEXTURES, FISH_TEXTURES, PLANT_TEXTURES = DBImporter.get_db_food_textures()

def transformation_handler(recipe, transform_type):
    """
    Handler which calls transform_recipe with recipe and correct transformation dictionary
    """
    transformation = None
    if transform_type == 'omnivore':
        transformation = transform_recipe(recipe,
                                          texture_dicts=[PLANT_TEXTURES],
                                          texture_transform_dict=OMNIVORE_DICT)
    elif transform_type == 'pescatarian':
        transformation = transform_recipe(recipe,
                                          texture_dicts=[MEAT_TEXTURES],
                                          texture_transform_dict=PESC_DICT)
    elif transform_type == 'vegetarian':
        transformation = transform_recipe(recipe,
                                          texture_dicts=[MEAT_TEXTURES, FISH_TEXTURES],
                                          texture_transform_dict=VEGETARIAN_DICT)
    elif transform_type == 'vegan':
        transformation = transform_recipe(recipe,
                                          texture_dicts=[MEAT_TEXTURES, FISH_TEXTURES],
                                          texture_transform_dict=VEGAN_DICT,
                                          food_transform_dict=VEGAN_ANIMAL_PRODUCTS_DICT)
    elif transform_type == 'lactose free':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LACTOSE_FREE_DICT)
    elif transform_type == 'gluten free':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=GLUTEN_FREE_DICT)
    elif transform_type == 'low cal':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LOW_CAL_DICT)
    elif transform_type == 'low fat':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LOW_FAT_DICT)
    elif transform_type == 'low sodium':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LOW_SODIUM_DICT)
    elif transform_type == 'low carb':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LOW_CARB_DICT)
    elif transform_type == 'low gi':
        transformation = transform_recipe(recipe,
                                          food_transform_dict=LOW_GI_DICT)

    return transformation

def transform_recipe(recipe, texture_dicts=None, texture_transform_dict=None,
                     food_transform_dict=None):
    """
    Transforms recipe based on constraints given by texture and food dictionaries.
    If given a texture dictionary, first makes texture-based substitutions then food based subs.
    """
    substitutes = {}

    for ingredient in recipe['ingredients']:
        # convert ingredients by texture, if specified
        if texture_dicts is not None:
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
                viable_substitutions = texture_transform_dict[texture_value]
                substitutes[ingredient['name']] = viable_substitutions

        # convert ingredients by name, if specified
        if food_transform_dict is not None:
            for food in food_transform_dict:
                if food in ingredient['name']:
                    substitutes[ingredient['name']] = food_transform_dict[food]
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
        lactose_subs = transformation_handler(recipe_from_url, 'lactose free')
        gluten_subs = transformation_handler(recipe_from_url, 'gluten free')

        low_cal_subs = transformation_handler(recipe_from_url, 'low cal')
        low_fat_subs = transformation_handler(recipe_from_url, 'low fat')
        low_sodium_subs = transformation_handler(recipe_from_url, 'low sodium')
        low_carb_subs = transformation_handler(recipe_from_url, 'low carb')
        low_gi_subs = transformation_handler(recipe_from_url, 'low gi')

        print 'Pescatarian substitutes: ' + str(pesc_subs)
        print 'Vegetarian substitutes: ' + str(vegetarian_subs)
        print 'Vegan substitutes: ' + str(vegan_subs)
        print 'Lactose-free substitutes: ' + str(lactose_subs)
        print 'Gluten-free substitutes: ' + str(gluten_subs)
        print 'Low cal substitutes: ' + str(low_cal_subs)
        print 'Low fat substitutes: ' + str(low_fat_subs)
        print 'Low sodium substitutes: ' + str(low_sodium_subs)
        print 'Low carb substitutes: ' + str(low_carb_subs)
        print 'Low gi substitutes: ' + str(low_gi_subs)
        print

if __name__ == '__main__':
    main()
