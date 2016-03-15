# Project 2: Recipe Analyzer
Recipe project for Team 3, built for Northwestern's EECS 337. 

# Using Project
## First Time Setup
Our project uses several third-party python dependencies. Below are instructions for setting up our project for use on your machine. 

1. Clone repository and navigate to directory using command line
2. Run the following to setup virtual environment and download dependencies:

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
