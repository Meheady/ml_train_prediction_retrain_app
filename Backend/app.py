from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib

app = Flask(__name__)


try:
    model = joblib.load('model.pkl')
except:
    model = LogisticRegression()

@app.route('/train', methods=['POST'])

def train_model():
    data = request.get_json()
    X = pd.DataFrame(data['X'])
    y = pd.DataFrame(data['y'])
    model.fit(X, y)

    joblib.dump(model,'model.pkl')

    return jsonify({
        'message': 'Model trained successfully',
        'success': True
    });

@app.route('/predict', methods=['POST'])

def predict():
    new_data = request.get_json()
    new_data = pd.DataFrame(new_data)
    y_pred = model.predict(new_data).tolist()
    y_prob = model.predict_proba(new_data).tolist()

    return jsonify({
        'predictions': y_pred,
        'probabilities': y_prob,
        'success': True
    });

@app.route('/retrain', methods=["POST"])

def retrain():
    data = request.get_json()
    X_new = pd.DataFrame(data['X'])
    y_new = pd.Series(data['y'])

    global model

    model.fit(X_new, y_new)

    joblib.dump(model, 'model.pkl')
    return jsonify({
        'message': 'Model retrained successfully',
        'success': True
    });

if __name__ == '__main__':
    app.run(debug=True)
