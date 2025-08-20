import requests
from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'location_names':utils.get_location_names()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response






if __name__ == '__main__':
    print("Starting server...")
    app.run()