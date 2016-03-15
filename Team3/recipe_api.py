'''Version 0.1'''
from get_recipetext_from_html import get_recipetext_from_html
from local_parsing_work import get_parsed_recipe

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    # your code here
    recipe_string = get_recipetext_from_html(url)
    results = get_parsed_recipe(recipe_string)
    return results