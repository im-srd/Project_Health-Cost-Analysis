import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model from the pickle file
filename = 'rf_reg.pkl'
with open(filename, 'rb') as file:
    model = pickle.load(file)

# Define the function to predict charges
def predict_charges(features):
    # Reshape the features into a 2D array
    features = np.array(features).reshape(1, -1)
    # Make predictions
    charges = model.predict(features)
    return charges[0]

# Define the homepage layout
def homepage():
    st.title('Medical Charges Prediction')
    st.write('Enter the patient details to predict medical charges:')

    # Input fields
    hospital_tier = st.selectbox('Hospital Tier', ['Tier 1', 'Tier 2', 'Tier 3'])
    city_tier = st.selectbox('City Tier', ['Tier 1', 'Tier 2', 'Tier 3'])
    bmi = st.number_input('BMI', min_value=0.0, step=0.1)
    hba1c = st.number_input('HBA1C', min_value=0.0, step=0.1)
    heart_issues = st.checkbox('Heart Issues')
    transplants = st.checkbox('Any Transplants')
    cancer_history = st.checkbox('Cancer History')
    major_surgeries = st.number_input('Number of Major Surgeries', min_value=0, step=1)
    smoker = st.checkbox('Smoker')
    age = st.number_input('Age', min_value=0, step=1)

    # Button to predict charges
    if st.button('Predict Charges'):
        # Convert categorical inputs to numerical
        hospital_tier = 1 if hospital_tier == 'Tier 1' else (2 if hospital_tier == 'Tier 2' else 3)
        city_tier = 1 if city_tier == 'Tier 1' else (2 if city_tier == 'Tier 2' else 3)
        heart_issues = 1 if heart_issues else 0
        transplants = 1 if transplants else 0
        cancer_history = 1 if cancer_history else 0
        smoker = 1 if smoker else 0

        # Gather features
        features = [hospital_tier, city_tier, bmi, hba1c, heart_issues, transplants, cancer_history, major_surgeries, smoker, age]

        # Predict charges
        charges = predict_charges(features)

        # Display result
        st.write('Predicted Charges:', charges)


# Run the app
if __name__ == '__main__':
    homepage()
