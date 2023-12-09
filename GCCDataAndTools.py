# requirements
import pandas as pd
import requests
import json

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

