from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.ext.session import Session
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def base():

	return render_template('index.html')

@app.route('/parse_recipes')
def parse_recipes():

	return render_template('parse_recipes.html')

if __name__ == '__main__':

	app.debug = True
	app.run()

