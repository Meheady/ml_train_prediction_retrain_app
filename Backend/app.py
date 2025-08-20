from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load('model.pkl')
except:
    model = LogisticRegression()

@app.route('/train', methods=['POST'])

def train_model():

    if 'file' not in request.files:
        return jsonify({
            'message': 'No file uploaded',
            'success': False
        })

    file = request.files['file']
    df = pd.read_csv(file)
    df.drop('customer_id', axis=1, inplace=True)
    X = df.drop('visited_website', axis=1)
    y = df['visited_website']
    model.fit(X, y)

    joblib.dump(model,'model.pkl')

    return jsonify({
        'message': 'Model trained successfully',
        'success': True
    });

@app.route('/predict', methods=['POST'])

def predict():
    data = request.json
    X_new = [[data["purchase_amount"], data["support_calls"]]]
    prediction = model.predict(X_new)[0]
    probability = model.predict_proba(X_new).tolist()

    return jsonify({
        'prediction': prediction.tolist(),
        'probability': probability,
        'success': True
    })

@app.route('/retrain', methods=["POST"])

def retrain():
    if 'file' not in request.files:
        return jsonify({
            'message': 'No file uploaded',
            'success': False
        })

    file = request.files['file']
    df = pd.read_csv(file)
    df.drop('customer_id', axis=1, inplace=True)
    X_new = df.drop('visited_website', axis=1)
    y_new = df['visited_website']

    global model

    model.fit(X_new, y_new)

    joblib.dump(model, 'model.pkl')
    return jsonify({
        'message': 'Model retrained successfully',
        'success': True
    });

if __name__ == '__main__':
    app.run(debug=True)
