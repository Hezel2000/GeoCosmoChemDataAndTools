# requirements
import pandas as pd
import requests
import json
import os

base_url = 'https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/'

json_file_names = ['chondrite properties.json',
 'chemical element properties.json',
 'chondrite element abundances.json',
 'element electron binding energies.json',
 'oxide - element conversion factors.json',
 'West African Craton.json',
 'Tanzania Craton Archean.json',
 'Bastar Craton.json',
 'Easter Seamount Chain Salas Y Gomez Ridge.json',
 'Ninetyeast Ridge.json',
 'Baical Rift Zone.json',
 'Emeishan.json',
 'Galapagos Islands.json',
 'Banda Arc.json',
 'Karoo Province - Africa.json',
 'North American Cordillera - Paleozoic.json',
 'Hyblean or Iblean Plateau, Sicily.json',
 'McDonald Islands.json']

# # json file names from the json folder
# def get_json_file_names():
#     json_files = []
#     for file in os.listdir('json'):
#         if file.endswith('json'):
#             json_files.append(file[:-5])
#     return json_files

# Display the main database content
def display_databases():
    return pd.DataFrame(json_file_names).rename(columns = {0: 'available datasets'})
    #return pd.read_csv('https://raw.githubusercontent.com/Hezel2000/geocosmochemdataandtools/master/GCCdata.csv')


# Get a specific database
def get_data(database, property=None, type=None):
    #df_GCdata = pd.read_csv('https://raw.githubusercontent.com/Hezel2000/geocosmochemdataandtools/master/GCCdata.csv')
    #fil = (df_GCdata['available datasets'] == database) #| (df_GCdata['abbreviated name'] == database)
    #url = df_GCdata[fil]['github link'].values[0]
    url = base_url + 'json/'+ database +'.json'
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

