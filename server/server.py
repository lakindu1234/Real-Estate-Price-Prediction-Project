from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    res




if __name__ == '__main__':
    print("Starting server...")
    app.run()