from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.session import Session
import os
import random
import copy

from local_parsing_work import *
import transform_recipe as Transformer

app = Flask(__name__)
sess = Session()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

BASIC_INGREDIENTS = get_basic_ingredients()

@app.route('/')
def base():

	return render_template('index.html')

@app.route('/parse_recipes', methods=['GET', 'POST'])
def parse_recipes():

	if request.method == 'POST':

		# HERE is where we will do all of the parsing and transforming
		recipeURL = request.form.get('recipe-url')
		session['recipeURL'] = recipeURL

		#dietDirection = request.form.get('diet-dir')
		dietType = request.form.get('diet-opt')
		session['dietType'] = dietType

		healthType = request.form.get('health-opt')
		session['healthType'] = healthType

		easyDIY = request.form.get('easy-diy')
		session['easy diy'] = easyDIY is not None


		recipeText = get_recipetext_from_html(recipeURL)
		recipeDict = get_parsed_recipe(recipeText, BASIC_INGREDIENTS)

		session['recipeDict'] = recipeDict

		return redirect(url_for('view_recipe'))

	return render_template('parse_recipes.html')

@app.route('/view_recipe')
def view_recipe():

	recipeURL = session['recipeURL']

	recipeDict = session['recipeDict']

	origRecipeDict = copy.deepcopy(recipeDict)

	#dietDirection = session['dietDirection']
	dietType = session['dietType']

	#healthDirection = session['healthDirection']
	healthType = session['healthType']

	easyDIY = session['easy diy']

	dietSubstitutes = {}
	if dietType != 'none':
		if dietType == 'omnivore':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'omnivore')
		elif dietType == 'pescatarian':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'pescatarian')
		elif dietType == 'vegetarian':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'vegetarian')
		elif dietType == 'vegan':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'vegan')
		elif dietType == 'lactose free':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'lactose free')
		elif dietType == 'gluten free':
			dietSubstitutes = Transformer.transformation_handler(recipeDict, 'gluten free')

	if dietSubstitutes:

		recipeDict = clean_dict(recipeDict, dietSubstitutes)

	healthSubstitutes = {}
	if healthType != 'none':
		if healthType == 'low cal':
			healthSubstitutes = Transformer.transformation_handler(recipeDict, 'low cal')
		elif healthType == 'low fat':
			healthSubstitutes = Transformer.transformation_handler(recipeDict, 'low fat')
		elif healthType == 'low sodium':
			healthSubstitutes = Transformer.transformation_handler(recipeDict, 'low sodium')
		elif healthType == 'low carb':
			healthSubstitutes = Transformer.transformation_handler(recipeDict, 'low carb')
		elif healthType == 'low gi':
			healthSubstitutes = Transformer.transformation_handler(recipeDict, 'low gi')

	if healthSubstitutes:
		recipeDict = clean_dict(recipeDict, healthSubstitutes)


	easyDiySubstitutes = {}
	if easyDIY:
		easyDiySubstitutes = Transformer.transformation_handler(recipeDict, 'easy-to-diy')

	if easyDiySubstitutes:

		recipeDict = make_easy(recipeDict, easyDiySubstitutes)

	return render_template('view_recipe.html', recipeURL=recipeURL, origRecipeDict=origRecipeDict, recipeDict=recipeDict, dietType=dietType,
							dietSubstitutes=dietSubstitutes, healthSubstitutes=healthSubstitutes, healthType=healthType, easyDIY=easyDIY)

def clean_dict(recipeDict, substitutes):

	for substitute in substitutes:

		substitutes[substitute] = random.choice(substitutes[substitute])

	# clean name
	nameList = recipeDict['name'].split(" ")
	name = []
	for word in nameList:
		if word in substitutes.keys():
			name.append(substitutes[word])
		else:
			name.append(word)

	recipeDict['name'] = " ".join(name)

	# clean ingredients
	for ingredient in recipeDict['ingredients']:
		if ingredient['name'] in substitutes.keys():
			ingredient['name'] = substitutes[ingredient['name']]


	return recipeDict

def make_easy(recipeDict, substitutes):

	for ingredient in recipeDict['ingredients']:

		if ingredient['name'] in substitutes.keys():

			ingredient['name'] = '<a href=\"' + substitutes[ingredient['name']][0] + '\"" target=\"_blank\">' + 'DIY ' + ingredient['name'] + '</a>'

	return recipeDict



if __name__ == '__main__':
	app.secret_key = 'tangerine prophet'
	app.config['SESSION_TYPE'] = 'filesystem'

	sess.init_app(app)
	app.debug = True
	app.run()

