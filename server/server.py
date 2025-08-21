from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        # Safely get JSON data without raising errors
        json_data = None
        try:
            if request.is_json:
                json_data = request.get_json()
        except:
            json_data = None

        # Debug: Print request method and data
        print(f"Request method: {request.method}")
        print(f"Request args: {request.args}")
        print(f"Request form: {request.form}")
        print(f"Request json: {json_data}")
        print(f"Content-Type: {request.content_type}")

        # Initialize variables
        total_sqft = None
        location = None
        bhk = None
        bath = None

        # GET: query parameters
        if request.method == 'GET':
            try:
                total_sqft = float(request.args.get('total_sqft')) if request.args.get('total_sqft') else None
                location = request.args.get('location')
                bhk = int(request.args.get('bhk')) if request.args.get('bhk') else None
                bath = int(request.args.get('bath')) if request.args.get('bath') else None
            except (ValueError, TypeError) as e:
                return jsonify({'error': f'Invalid parameter type: {str(e)}'}), 400

        # POST: try different data sources
        elif request.method == 'POST':
            # Try JSON data first
            if json_data:
                try:
                    total_sqft = float(json_data.get('total_sqft')) if json_data.get('total_sqft') else None
                    location = json_data.get('location')
                    bhk = int(json_data.get('bhk')) if json_data.get('bhk') else None
                    bath = int(json_data.get('bath')) if json_data.get('bath') else None
                except (ValueError, TypeError) as e:
                    return jsonify({'error': f'Invalid JSON parameter type: {str(e)}'}), 400
            else:
                # Try form data
                try:
                    total_sqft = float(request.form.get('total_sqft')) if request.form.get('total_sqft') else None
                    location = request.form.get('location')
                    bhk = int(request.form.get('bhk')) if request.form.get('bhk') else None
                    bath = int(request.form.get('bath')) if request.form.get('bath') else None
                except (ValueError, TypeError) as e:
                    return jsonify({'error': f'Invalid form parameter type: {str(e)}'}), 400

        # Debug: Print extracted values
        print(f"Extracted values - total_sqft: {total_sqft}, location: {location}, bhk: {bhk}, bath: {bath}")

        # Check if any value is missing
        missing_params = []
        if total_sqft is None:
            missing_params.append('total_sqft')
        if location is None:
            missing_params.append('location')
        if bhk is None:
            missing_params.append('bhk')
        if bath is None:
            missing_params.append('bath')

        if missing_params:
            return jsonify({
                'error': f'Missing parameters: {", ".join(missing_params)}',
                'required_params': ['total_sqft', 'location', 'bhk', 'bath'],
                'received_args': dict(request.args),
                'received_form': dict(request.form),
                'received_json': json_data,
                'content_type': request.content_type
            }), 400

        # Validate parameter ranges
        if total_sqft <= 0:
            return jsonify({'error': 'total_sqft must be greater than 0'}), 400
        if bhk <= 0:
            return jsonify({'error': 'bhk must be greater than 0'}), 400
        if bath <= 0:
            return jsonify({'error': 'bath must be greater than 0'}), 400

        # Call the utility function
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print(f"Error in predict_home_price: {str(e)}")
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'debug_info': {
                'method': request.method,
                'args': dict(request.args),
                'form': dict(request.form),
                'json': json_data,
                'content_type': request.content_type
            }
        }), 500

# Add a test endpoint to check if server is working
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Home Price Prediction API is running'})

# Add an endpoint to test the predict function with sample data
@app.route('/test_predict', methods=['GET'])
def test_predict():
    try:
        # Test with sample data
        estimated_price = util.get_estimated_price('1st Phase JP Nagar', 1000, 2, 2)
        return jsonify({
            'message': 'Test successful',
            'sample_prediction': estimated_price,
            'test_params': {
                'location': '1st Phase JP Nagar',
                'total_sqft': 1000,
                'bhk': 2,
                'bath': 2
            }
        })
    except Exception as e:
        return jsonify({'error': f'Test failed: {str(e)}'}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        util.load_saved_artifacts()
        print("Artifacts loaded successfully")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

    app.run(debug=True)  # Enable debug mode for better error messages
