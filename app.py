from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.session import Session
import os

from local_parsing_work import *

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

	return render_template('view_recipe.html', recipeURL=recipeURL, recipeDict=recipeDict, dietType=dietType, healthDirection=healthDirection, healthType=healthType)

if __name__ == '__main__':
	app.secret_key = 'tangerine prophet'
	app.config['SESSION_TYPE'] = 'filesystem'

	sess.init_app(app)
	app.debug = True
	app.run()

