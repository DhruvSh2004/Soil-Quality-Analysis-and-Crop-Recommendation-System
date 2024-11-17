import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import MinMaxScaler

crop_data = pd.read_csv('Crop_recommendation.csv')
crop_data.info()
print(crop_data.isnull().sum())

#Feature Scaling (Normalizing N, K, P, temp, humidity, PH, rainfall) so that all value lies between 0 and 1
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(crop_data.drop('label', axis = 1))

#Creating a new DataFrame to store this scaled data
scaled_data = pd.DataFrame(scaled_features, columns = crop_data.columns[:-1])
scaled_data['Label'] = crop_data['label']

#Splitting the Dataset into training and testing sets
X = scaled_data.drop('Label', axis = 1)
Y = scaled_data['Label']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size  = 0.7, random_state = 42)

#Building the Random Forest Model
RF_model = RandomForestClassifier(n_estimators = 100, random_state = 42)
RF_model.fit(X_train, Y_train)

#Predicting on the test Data
Y_pred = RF_model.predict(X_test)

#Evaluating the model
accuracy = accuracy_score(Y_test, Y_pred)
print(f'Accuracy : {accuracy * 100:.2f}%')

print("Confusion Matrix : ")
print(confusion_matrix(Y_test, Y_pred))

print("Classification Report : ")
print(classification_report(Y_test, Y_pred))

import pickle
# Save the trained model to a file
with open("rf_model.pkl", "wb") as model_file:
    pickle.dump(RF_model, model_file)

# Save the scaler to a file
with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print("Model and scaler saved successfully!")
