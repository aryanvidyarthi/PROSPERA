# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS

def load_model():
    model_file = 'stock_recommendation_model.pkl'
    if not os.path.exists(model_file):
        print(f"Error: '{model_file}' not found. Please train the model first.")
        sys.exit(1)
    try:
        model = joblib.load(model_file)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

# Load the trained model
model = load_model()

# Mapping from numerical recommendation to suggestion
recommendation_mapping = {
    1: "Do Not Buy",
    2: "Do Not Buy",
    3: "Wait",
    4: "Buy",
    5: "Buy Strongly"
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract features from the request
    try:
        open_price = float(data['Open'])
        high = float(data['High'])
        low = float(data['Low'])
        close = float(data['Close'])
        volume = float(data['Volume'])
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input data. Please provide Open, High, Low, Close, and Volume as numerical values.'}), 400

    # Create a feature array
    features = np.array([[open_price, high, low, close, volume]])

    # Make prediction
    try:
        prediction = model.predict(features)[0]
        suggestion = recommendation_mapping.get(prediction, "Unknown")
    except Exception as e:
        return jsonify({'error': f"Error making prediction: {e}"}), 500

    # Return the result
    return jsonify({
        'Recommendation_Score': int(prediction),
        'Suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)
