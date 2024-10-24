# from flask import Flask, request, render_template, redirect, url_for, flash
# import pickle
# import numpy as np
# import os
# import pandas as pd

# # Initialize the Flask app
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder where files will be uploaded
# app.secret_key = 'supersecretkey'  # For flashing messages

# # Ensure the 'uploads' folder exists
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# # Load the model and scaler
# rf_model = pickle.load(open("rf_model.pkl", "rb"))
# scaler = pickle.load(open("scaler.pkl", "rb"))

# @app.route('/')
# def home():
#     """Render the home page."""
#     return render_template('home.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     """Handle both form inputs and file uploads for prediction."""
#     if 'cropFile' in request.files:
#         # Handle file upload
#         file = request.files['cropFile']

#         if file.filename == '':
#             flash('No file selected. Please upload a file.')
#             return redirect(request.url)

#         # Save the uploaded file
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)

#         try:
#             # Read the CSV file into a DataFrame
#             data = pd.read_csv(filepath)

#             # Assume the CSV contains the necessary features
#             scaled_data = scaler.transform(data)

#             # Predict using the model for all rows in the CSV
#             predictions = rf_model.predict(scaled_data)

#             # Prepare a result string with predictions
#             result = '<br>'.join([f'Recommended Crop: {pred}' for pred in predictions])

#         except Exception as e:
#             flash(f'Error processing the file: {str(e)}')
#             return redirect(url_for('home'))

#         return render_template('home.html', prediction_text=result)

#     else:
#         # Handle form input if no file is uploaded
#         try:
#             inputs = [float(x) for x in request.form.values()]

#             if not inputs:
#                 flash('Please provide all input values.')
#                 return redirect(request.url)

#             # Scale the input features
#             scaled_input = scaler.transform([inputs])

#             # Predict the crop
#             prediction = rf_model.predict(scaled_input)

#             return render_template('home.html', prediction_text=f'Recommended Crop: {prediction[0]}')

#         except Exception as e:
#             flash(f'Error processing the input: {str(e)}')
#             return redirect(url_for('home'))

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, render_template, redirect, url_for, flash
import pdfplumber  # Use PyMuPDF if preferred
import pandas as pd  # For CSV handling
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Make sure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle file upload and make predictions."""
    if 'cropFile' not in request.files:
        flash('No file part in the request')
        return redirect(url_for('index'))

    file = request.files['cropFile']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Extract data from PDF or CSV
    if file.filename.endswith('.pdf'):
        try:
            text = extract_text_from_pdf(filepath)
            data = extract_data_from_text(text)  # Convert text to usable data
        except Exception as e:
            flash(f"Error processing PDF: {str(e)}")
            return redirect(url_for('index'))

    elif file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(filepath)
            data = df.iloc[0].tolist()  # Extract the first row of data
        except Exception as e:
            flash(f"Error processing CSV: {str(e)}")
            return redirect(url_for('index'))
    else:
        flash('Invalid file format. Upload a PDF or CSV.')
        return redirect(url_for('index'))

    try:
        # Ensure data is numeric for the model
        scaled_input = scaler.transform([list(map(float, data))])
    except ValueError as e:
        flash(f"Error converting data to float: {str(e)}")
        return redirect(url_for('index'))

    try:
        prediction = rf_model.predict(scaled_input)
    except Exception as e:
        flash(f"Prediction failed: {str(e)}")
        return redirect(url_for('index'))

    # Display the prediction result
    return render_template('home.html', prediction_text=f'Recommended Crop: {prediction[0]}')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_data_from_text(text):
    """Convert extracted PDF text into a list of usable data."""
    try:
        # Assuming the text contains numeric data separated by spaces or commas
        return [float(value) for value in text.split() if value.strip()]
    except ValueError as e:
        raise ValueError(f"Could not convert text to numeric data: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)

