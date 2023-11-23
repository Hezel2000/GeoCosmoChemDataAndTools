# requirements
import pandas as pd
import requests
import json
import os

base_url = 'https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/'

# Display the main database content
def display_databases():
    return pd.read_csv(base_url + 'GCCdata.csv')


# Get a specific database
def get_data(database, property=None, type=None):
    df_GCdata = pd.read_csv(base_url + 'GCCdata.csv')
    fil = (df_GCdata['available datasets'] == database) | (df_GCdata['abbreviated name'] == database)
    url = base_url + 'json/' + df_GCdata[fil]['available datasets'].values[0] + '.json'
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
def write_json_file(file_name, file_path=None, description=None, references=None, source=None, license=None):
    dataset = pd.read_csv(file_path + '/' + file_name + '.csv').to_dict()

    json_file = {
        "description": description,
        "references": references,
        "source": source,
        "license": license,
        "dataset": dataset
    }

    if file_path is not None:
        with open(file_path + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)
    else:
        with open(os.getcwd() + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)

