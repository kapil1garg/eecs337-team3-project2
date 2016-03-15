# Project 2: Recipe Analyzer
Recipe project for Team 3, built for Northwestern's EECS 337. 

# Using Project
## First Time Setup
Our project uses several third-party python dependencies. Below are instructions for setting up our project for use on your machine. 

1. Clone repository and navigate to directory using command line
2. Make sure you have virtual environment installed: http://docs.python-guide.org/en/latest/dev/virtualenvs/
3. Run the following to setup virtual environment and download dependencies:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Autograder
1. Navigate to directory in command line
2. Run `source venv/bin/activate`
3. Once in the virual environment, run `python autograder.py 3` to run the autograder script

## Running Web GUI
1. Navigate to directory in command line
2. Run `source venv/bin/activate`
3. Navgate to Team3 folder: `cd Team3/`
4. Run `python app.py`
5. In Chrome, navigate to `localhost:5000`

## External Python Libraries
These can also be found in the `requirements.txt` file used to install dependencies.
- Flask
- Flask-Session
- lxml
- nltk
- urllib3

## Resources for Databases
- Vegan substitutes:
  - http://veganoutreach.org/subs/
  - https://en.wikipedia.org/wiki/List_of_meat_substitutes
  - http://www.peta.org/living/beauty/animal-ingredients-list/
- Pescatarian substitute: https://en.wikipedia.org/wiki/Fish_as_food
- Omnivore substitute:
  - https://en.wikipedia.org/wiki/List_of_beef_dishes
  - http://www.hirschsmeats.com/cuts-of-meat.htm,
- Lactose-free substitutes: http://www.todaysdietitian.com/newarchives/080112p38.
- Gluten-free substitutes:
  - https://glutenfreeworks.com/diet-and-health/food-
  - http://www.dummies.com/how-to/content/glutenfree-grain
- Low-calorie, low-fat substitutes: https://www.nhlbi.nih.gov/health/educational/
- Low-sodium:
  - http://greatist.com/health/21-lower-sodium-solutions
  - http://www.goodhousekeeping.com/health/diet-nutrition/a18901/low-
- Low-carb: http://www.bodybuilding.com/fun/the-ultimate-list-of-40-low-carb-
- Creative low-calorie substitutes: http://greatist.com/health/83-healthy-recipe-
- Low glycemic index: http://www.livestrong.com/article/401811-sugar-substitutes-
- Food ingredients: http://www.food.com/about/
- Cooking tools: 
  - https://en.wikipedia.org/wiki/List_of_food_preparation_utensils
  - https://en.wikipedia.org/wiki/List_of_cooking_appliances
- DIY recipes: http://allrecipes.com/recipes/17622/everyday-cooking/more-meal-
- Cooking verbs: http://diannej.com/2013/100-verbs-for-recipes-from-julia-child/

## Documentation and Methodology
Please see the following files in the root of the repo for documentation:
- Workflow Flowchart: WorkFlow.pdf
- Recipe Representation Diagram: RecipeRepresentation.pdf
- Knowledge Base Diagram: KnowledgeBase.pdf
