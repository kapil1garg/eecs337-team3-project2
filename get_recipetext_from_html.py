''' parsing the html by input an url and then output string 
	get_recipetext_from_html will reture a dict contains 4 attributes: name, ingredients, directions and footnotes
	the name is a string and the other three are string list
'''
import urllib3
from lxml import html

# this two url is for testing
URL = "http://allrecipes.com/recipe/240400/skillet-chicken-bulgogi/?internalSource=staff%%20pick&referringContentType=home%%20page/"
URL1 = "http://allrecipes.com/recipe/80776/lemon-herb-barbeque-sauce-for-chicken/?internalSource=rotd&referringId=1284&referringContentType=recipe%%20hub"

def get_webpage(url):
	http = urllib3.PoolManager()
	page = http.request('GET', url)
	return page

def get_parsed_content(raw_data):
	recipe_string = {}
	temp = []
	html_tree = html.fromstring(raw_data)
	# het the name of recipe
	recipe_name = html_tree.xpath("//meta[@property='og:title']")
	recipe_name = recipe_name[0].attrib.get('content')
	recipe_name = recipe_name.lower().replace("recipe", "", 1)
	recipe_string['name'] = recipe_name

	temp = []
	# get all the ingredients
	ingredients = html_tree.xpath("//li[@class='checkList__line']/label/span")
	for ingredient in ingredients:
		if ingredient.text and ingredient.text != 'Add all ingredients to list':
			temp.append(ingredient.text)
	recipe_string['ingredients'] = temp

	# get all directions
	temp = []
	directions = html_tree.xpath("//span[@class='recipe-directions__list--item']")
	for direction in directions:
		if direction.text:
			temp.append(direction.text)
	recipe_string['directions'] = temp

	# get footnotes
	temp = []
	footnotes = html_tree.xpath("//section[@class='recipe-footnotes']/ul/li")
	for footnote in footnotes[1:]:
		if footnote.text:
			temp.append(footnote.text)
	recipe_string['footnotes'] = temp

	return recipe_string

def get_recipetext_from_html(url):
	# get the string of the whole page
	raw_data = get_webpage(url).data
	recipe_string = get_parsed_content(raw_data)
	return recipe_string

def main():
	recipe = get_recipetext_from_html(URL)
	return

if __name__ == "__main__":
    main()