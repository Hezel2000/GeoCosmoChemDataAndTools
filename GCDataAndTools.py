#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# CGDataAndTools Commands

# requirements
import pandas as pd
import requests
import json
import os


# Display the main database content
def display_cgdatabases():
    return pd.read_csv('https://raw.githubusercontent.com/Hezel2000/GeoCosmoChemDataAndTools/master/CGdata.csv')


# Get a specific database
def get_data(database, property=None, type=None):
    df_GCdata = pd.read_csv('https://raw.githubusercontent.com/Hezel2000/GeoCosmoChemDataAndTools/master/CGdata.csv')
    fil = (df_GCdata['name'] == database) | (df_GCdata['abbreviated name'] == database)
    url = df_GCdata[fil]['github link'].values[0]
    resp = requests.get(url)
    full_data = json.loads(resp.text)

    if property is None:
        if type is None or type == 'dataframe':
            return pd.DataFrame(full_data['dataset'])
        elif type == 'json':
            return full_data['dataset']
    elif property == 'properties':
        return list(full_data.keys())[:-1]
    else:
        return full_data[property]


# Convert a csv into a json file with metadata
def write_json_file(file_name, file_path=None, description=None, references=None, license=None):
    dataset = pd.read_csv(file_path + '/' + file_name + '.csv').to_dict()

    json_file = {
        "description": description,
        "references": references,
        "license": license,
        "dataset": dataset
    }

    if file_path is not None:
        with open(file_path + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)
    else:
        with open(os.getcwd() + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)

