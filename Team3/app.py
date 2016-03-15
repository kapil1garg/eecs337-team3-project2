from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.session import Session
import os
import random

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

		#session['dietDirection'] = dietDirection
		session['dietType'] = dietType


		healthDirection = request.form.get('health-dir')
		healthType = request.form.get('health-opt')
		
		session['healthDirection'] = healthDirection
		session['healthType'] = healthType


		recipeText = get_recipetext_from_html(recipeURL)
		recipeDict = get_parsed_recipe(recipeText, BASIC_INGREDIENTS)

		session['recipeDict'] = recipeDict

		return redirect(url_for('view_recipe'))

	return render_template('parse_recipes.html')

@app.route('/view_recipe')
def view_recipe():

	recipeURL = session['recipeURL']

	recipeDict = session['recipeDict']

	#dietDirection = session['dietDirection']
	dietType = session['dietType']

	healthDirection = session['healthDirection']
	healthType = session['healthType']

	substitutes = {}
	if dietType != 'none':
		if dietType == 'omnivore':
			substitutes = Transformer.transformation_handler(recipeDict, 'omnivore')
		elif dietType == 'pescatarian':
			substitutes = Transformer.transformation_handler(recipeDict, 'pescatarian')
		elif dietType == 'vegetarian':
			substitutes = Transformer.transformation_handler(recipeDict, 'vegetarian')
		elif dietType == 'vegan':
			substitutes = Transformer.transformation_handler(recipeDict, 'vegan')

	if substitutes:
		
		recipeDict = clean_dict(recipeDict, substitutes)

	return render_template('view_recipe.html', recipeURL=recipeURL, recipeDict=recipeDict, dietType=dietType,
							substitutes=substitutes, healthDirection=healthDirection, healthType=healthType)

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

	# clean directions
	for i in range(len(recipeDict['directions'])):

		for key in substitutes.keys():

			if key in recipeDict['directions'][i]:
				print "[NOAH] Found key: " + key
				recipeDict['directions'][i] = substitutes[key].join(recipeDict['directions'][i].split(key))

	return recipeDict



if __name__ == '__main__':
	app.secret_key = 'tangerine prophet'
	app.config['SESSION_TYPE'] = 'filesystem'

	sess.init_app(app)
	app.debug = True
	app.run()

