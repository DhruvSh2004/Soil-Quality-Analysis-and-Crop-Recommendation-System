from flask import Flask, request, render_template, redirect, url_for, flash
import pickle
import numpy as np
import os
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder where files will be uploaded
app.secret_key = 'supersecretkey'  # For flashing messages

# Ensure the 'uploads' folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load the model and scaler
rf_model = pickle.load(open("rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Fertilizer recommendation based on crop type
def get_fertilizer_recommendation(crop_type):
    if crop_type == 'maize':
        return 'Urea'
    elif crop_type == 'sugarcane':
        return 'DAP'
    elif crop_type == 'cotton':
        return '14-35-14'
    elif crop_type == 'tobacco':
        return '28-28'
    elif crop_type == 'paddy':
        return 'Urea'
    elif crop_type == 'barley':
        return '17-17-17'
    elif crop_type == 'wheat':
        return 'Urea'
    elif crop_type == 'millets':
        return '28-28'
    elif crop_type == 'oil seeds':
        return '14-35-14'
    elif crop_type == 'pulses':
        return 'DAP'
    elif crop_type == 'ground Nuts':
        return 'DAP'
    elif crop_type == 'apple':
        return 'NPK balanced fertilizers'
    elif crop_type == 'banana':
        return 'Urea, Muriate of Potash (MOP), DAP'
    elif crop_type == 'blackgram':
        return 'Rhizobium inoculant, SSP (Single Super Phosphate)'
    elif crop_type == 'chickpea':
        return 'SSP (Single Super Phosphate)'
    elif crop_type == 'coconut':
        return 'NPK balanced, organic manure'
    elif crop_type == 'coffee':
        return 'NPK with higher potassium, compost'
    elif crop_type == 'grapes':
        return 'NPK mixture'
    elif crop_type == 'jute':
        return 'Urea, MOP (Muriate of Potash)'
    elif crop_type == 'kidney Beans':
        return 'Rhizobium inoculant, SSP'
    elif crop_type == 'lentil':
        return 'NPK mixture with moderate phosphorus'
    elif crop_type == 'mango':
        return 'NPK mixture, organic manure'
    elif crop_type == 'muskmelon':
        return 'NPK mixture with balanced nitrogen'
    elif crop_type == 'rice':
        return 'Urea'
    elif crop_type == 'watermelon':
        return 'NPK mixture with higher potassium'
    else:
        return 'No specific recommendation'


@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

def generate_sustainability_recommendation(data):
    """Provide sustainability recommendations based on soil data."""
    recommendations = []
    # Example logic based on nutrient levels in the data
    if data[0] < 50:  # Assume data[0] represents nitrogen levels
        recommendations.append("Consider adding nitrogen-rich fertilizers.")
    if data[1] < 30:  # Assume data[1] represents phosphate levels
        recommendations.append("Phosphate levels are low, consider phosphate supplementation.")
    if data[2] < 20:  # Assume data[2] represents potash levels
        recommendations.append("Potash levels are below optimal levels. Add potash-rich manure.")
    
    return " ".join(recommendations) if recommendations else "Soil is in good condition. No major interventions needed."

@app.route('/predict', methods=['POST'])
def predict():
    """Handle both form inputs and file uploads for prediction."""
    if 'cropFile' in request.files:
        # Handle file upload
        file = request.files['cropFile']

        if file.filename == '':
            flash('No file selected. Please upload a file.')
            return redirect(request.url)

        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            # Read the CSV file into a DataFrame
            data = pd.read_csv(filepath)

            # Assume the CSV contains the necessary features
            scaled_data = scaler.transform(data)

            # Predict using the model for all rows in the CSV
            predictions = rf_model.predict(scaled_data)

            # Prepare a result string with predictions and recommendations
            result = ""
            for i, pred in enumerate(predictions):
                crop_type = pred  # Assuming the model predicts a crop type
                fertilizer_recommendation = get_fertilizer_recommendation(crop_type)
                recommendation = generate_sustainability_recommendation(data.iloc[i].tolist())
                result += f'Recommended Crop: {pred} Fertilizer Recommendation: {fertilizer_recommendation} Sustainability Recommendation: {recommendation}'

        except Exception as e:
            flash(f'Error processing the file: {str(e)}')
            return redirect(url_for('home'))

        return render_template('home.html', prediction_text=result)

    else:
        # Handle form input if no file is uploaded
        try:
            inputs = [float(x) for x in request.form.values()]

            if not inputs:
                flash('Please provide all input values.')
                return redirect(request.url)

            # Scale the input features
            scaled_input = scaler.transform([inputs])

            # Predict the crop
            prediction = rf_model.predict(scaled_input)
            crop_type = prediction[0]

            # Generate fertilizer recommendation
            fertilizer_recommendation = get_fertilizer_recommendation(crop_type)

            # Generate sustainability recommendation based on inputs
            sustainability_recommendation = generate_sustainability_recommendation(inputs)

            return render_template('home.html', prediction_text=f'Recommended Crop: {crop_type}', prediction_text2=f'Fertilizer Recommendation: {fertilizer_recommendation}', prediction_text3= f'Sustainability Recommendation: {sustainability_recommendation}')

        except Exception as e:
            flash(f'Error processing the input: {str(e)}')
            return redirect(url_for('home'))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
