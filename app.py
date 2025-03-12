from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the saved ML pipeline model (ensure pipeline_xgb.pkl is in the same directory)
with open('pipeline_xgb.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    age = float(request.form.get('age'))
    gender = request.form.get('gender')
    scheduledday = request.form.get('scheduledday')
    appointmentday = request.form.get('appointmentday')
    
    # Create a DataFrame for the new data point
    data = {
        'age': [age],
        'gender': [gender],
        'scheduledday': [scheduledday],
        'appointmentday': [appointmentday]
        # Add other fields as needed for your model here.
    }
    new_data = pd.DataFrame(data)
    
    # Convert date columns to datetime objects
    new_data['scheduledday'] = pd.to_datetime(new_data['scheduledday'])
    new_data['appointmentday'] = pd.to_datetime(new_data['appointmentday'])
    
    # Get prediction and probability
    prediction = model.predict(new_data)[0]
    prediction_proba = model.predict_proba(new_data)[0, 1]
    
    result = "Patient No-Show" if prediction == 1 else "Patient Will Show"
    
    return render_template('index.html', prediction_text=f"Prediction: {result} (No-show probability: {prediction_proba:.2f})")

if __name__ == "__main__":
    # If running in Google Colab, use flask_ngrok to expose the app externally.
    try:
        from flask_ngrok import run_with_ngrok
        run_with_ngrok(app)
    except ImportError:
        pass
    app.run()
