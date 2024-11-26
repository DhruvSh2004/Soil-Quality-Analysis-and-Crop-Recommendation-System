from flask import Flask, request, render_template, redirect, url_for, flash
import pickle
import numpy as np
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  
app.secret_key = 'supersecretkey'  

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

rf_model = pickle.load(open("rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

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
    return render_template('index1.html')

def generate_sustainability_recommendation(data):
    """Provide sustainability recommendations based on soil data."""
    recommendations = []
    if data[0] < 50:  
        recommendations.append("Consider adding nitrogen-rich fertilizers.")
    if data[1] < 30:  
        recommendations.append("Phosphate levels are low, consider phosphate supplementation.")
    if data[2] < 20:  
        recommendations.append("Potash levels are below optimal levels. Add potash-rich manure.")
    
    return " ".join(recommendations) if recommendations else "Soil is in good condition. No major interventions needed."


@app.route('/predict', methods=['POST'])
def predict():
    """Handle both form inputs and file uploads for prediction."""
    if 'cropFile' in request.files:

        file = request.files['cropFile']

        if file.filename == '':
            flash('No file selected. Please upload a file.')
            return redirect(request.url)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            data = pd.read_csv(filepath)

            scaled_data = scaler.transform(data)

            predictions = rf_model.predict_proba(scaled_data)

            result = ""
            for i, prediction in enumerate(predictions):
                # Get top 3 crops with highest probability
                top_crops_indices = prediction.argsort()[-3:][::-1]  # Get indices of top 3 crops
                top_crops = [rf_model.classes_[index] for index in top_crops_indices]

                # Generate recommendations for each crop
                for crop_type in top_crops:
                    fertilizer_recommendation = get_fertilizer_recommendation(crop_type)
                    sustainability_recommendation = generate_sustainability_recommendation(data.iloc[i].tolist())

                    result += f'Recommended Crop: {crop_type}<br>'
                    result += f'Fertilizer Recommendation: {fertilizer_recommendation}<br>'
                    result += f'Sustainability Recommendation: {sustainability_recommendation}<br><br>'  # Adds a line break between each crop

        except Exception as e:
            flash(f'Error processing the file: {str(e)}')
            return redirect(url_for('index1'))

        return render_template('index1.html', prediction_text=result)

    else:
        try:
            inputs = [float(x) for x in request.form.values()]

            if not inputs:
                flash('Please provide all input values.')
                return redirect(request.url)

            scaled_input = scaler.transform([inputs])

            # Predict the top 3 crops
            predictions = rf_model.predict(scaled_input)[:3]  # Get top 3 predictions

            # Generate fertilizer and sustainability recommendations
            result = ""
            for crop_type in predictions:
                fertilizer_recommendation = get_fertilizer_recommendation(crop_type)
                sustainability_recommendation = generate_sustainability_recommendation(inputs)

                result += f'Recommended Crop: {crop_type}<br>'
                result += f'Fertilizer Recommendation: {fertilizer_recommendation}<br>'
                result += f'Sustainability Recommendation: {sustainability_recommendation}<br><br>'  # Adds a line break between each crop

            return render_template('index1.html', prediction_text=result)

        except Exception as e:
            flash(f'Error processing the input: {str(e)}')
            return redirect(url_for('index1'))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
