import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    # Ensure model and columns are loaded
    if __data_columns is None or __model is None:
        raise Exception("Artifacts not loaded. Please call load_saved_artifacts() first.")

    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns, __locations, __model

    try:
        # Use absolute path for safety
        current_dir = os.path.dirname(__file__)
        columns_path = os.path.join(current_dir, "columns.json")
        model_path = os.path.join(current_dir, "banglore_home_prices_model.pickle")

        # Load columns.json
        with open(columns_path, "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

        # Load model pickle
        if __model is None:
            with open(model_path, 'rb') as f:
                __model = pickle.load(f)

        print("loading saved artifacts...done")
        return True

    except FileNotFoundError as fnf:
        print(f"File not found error: {fnf}")
        return False
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        return False


def get_location_names():
    return __locations


def get_data_columns():
    return __data_columns


if __name__ == '__main__':
    if load_saved_artifacts():
        print(get_location_names())
        print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
        print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
        print(get_estimated_price('Kalhalli', 1000, 2, 2))  # other location
        print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location
    else:
        print("Failed to load artifacts. Please check file paths.")
