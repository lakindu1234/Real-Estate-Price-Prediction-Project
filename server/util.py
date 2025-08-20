import json
import pickle

__locations = None
__data_columns = None
__model = None

def get_location_names():
    global __locations
    return __locations  # Return the list of locations

def load_saved_artifacts():
    print("Loading saved artifacts...")
    global __data_columns
    global __locations
    global __model

    # Load columns.json
    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']  # extract the data_columns list
        __locations = __data_columns[3:]  # first 3 are sqft, bath, bhk → rest are locations

    # Load the trained model pickle
    with open("./artifacts/banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)

    print("Loaded saved artifacts...")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())  # This will now print location names
