"""Script to pull all necessary data and create necessary databases"""
import json
import requests
import io
import os
import Queue as Q
from difflib import SequenceMatcher

def load_from_config():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    return config_data

CONFIG_SETTINGS = load_from_config()

def merge_two_dict(x, y):
    """Combines two dictionaries into one an returns"""
    z = x.copy()
    z.update(y)
    return z

def load_food_ingredients():
    url = 'http://api.nal.usda.gov/ndb/nutrients?format=json&lt=f&sort=f&api_key='
    url += CONFIG_SETTINGS['ndb_api_key']
    parameters = '&max-150&nutrients=204&nutrients=208&nutrients=269'

    # pull all data from API
    start = 0
    food_items = []
    still_items = True
    while(still_items):
        r = requests.get(url + parameters + '&offset=' + str(start))
        r = r.json()

        new_start = r['report']['end']
        print "Finished query at offset " + str(start) + \
            "...Beginning query at offset " + str(new_start)

        if len(r['report']['foods']) > 0:
            food_items.extend(r['report']['foods'])
            start = new_start
        else:
            still_items = False

    # convert array of dictionaries to singular dictionary and export as json
    food_dict = parse_array_into_dict(food_items, 'name')
    with io.open('food_db.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(food_dict, sort_keys=True, indent=4, ensure_ascii=False))

def parse_array_into_dict(array, key_string):
    """
    Parses an array of dictionaries into a single dictionary with key_string values
    used as key values)
    """
    new_dict = {}
    for entry in array:
        new_key = entry[key_string]
        del entry[key_string]

        new_dict[new_key] = entry
    return new_dict

def find_similar_strings():
    """
    Finds all strings that are similar over a certain threshold.
    """
    # check if database esists, otherwise create database
    if not os.path.isfile('food_db.json'):
        load_food_ingredients()
    
    with open('food_db.json') as data:
        data = json.load(data)
    
    # create dictionary to hold most similar strings
    similarity_dict = dict.fromkeys(data.keys())
    for i in data.keys():
        print i
        similarity_queue = Q.PriorityQueue()
        for j in data.keys():
            current_ratio = SequenceMatcher(None, i, j).ratio()
            if not current_ratio == 1.0 and current_ratio > 0.8:
                similarity_queue.put((current_ratio, j))
        similarity_dict[i] = []
        while not similarity_queue.empty():
            similarity_dict[i].append(similarity_queue.get())
    print similarity_dict
 
def main():
    # load_food_ingredients()
    find_similar_strings()

if __name__ == '__main__':
    main()

