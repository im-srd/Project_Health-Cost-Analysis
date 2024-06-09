import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3

# Set page configuration with icon
st.set_page_config(page_title="Medical Charges Prediction", page_icon=":hospital:")

# Load the model from the pickle file
filename = 'rf_reg.pkl'
with open(filename, 'rb') as file:
    model = pickle.load(file)

# Define the function to predict charges
def predict_charges(features):
    features = np.array(features).reshape(1, -1)
    charges = model.predict(features)
    return charges[0]

# Database setup
conn = sqlite3.connect('patients.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS patients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, 
              name TEXT, hospital_tier INTEGER, city_tier INTEGER, bmi REAL, 
              hba1c REAL, heart_issues INTEGER, transplants INTEGER, 
              cancer_history INTEGER, major_surgeries INTEGER, 
              smoker INTEGER, age INTEGER, charges REAL)''')
conn.commit()

# User authentication
def signup():
    st.title('Signup')
    full_name = st.text_input('Full Name')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Signup'):
        c.execute('INSERT INTO patients (name, username, password) VALUES (?, ?, ?)', (full_name, username, password))
        conn.commit()
        st.success('You have successfully signed up!')

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        c.execute('SELECT * FROM patients WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.full_name = user[3]  # Store the user's full name in session state
            st.success(f'You have successfully logged in, {st.session_state.full_name}!')
        else:
            st.error('Invalid username or password')

# Define the homepage layout
def homepage():
    if st.button('Back'):
        st.session_state.logged_in = False
        st.experimental_rerun()

    st.title('Medical Charges Prediction')
    st.markdown(f'<div style="display: flex; align-items: center;"><h3>Welcome,</h3><h2 style="color:red; margin-left: 10px;">{st.session_state.full_name}!</h2></div>', unsafe_allow_html=True)
    st.write('Enter your details to predict medical charges:')
    
    # Input fields
    hospital_tier = st.selectbox('Hospital Tier', ['Tier 1', 'Tier 2', 'Tier 3'], key='hospital_tier')
    city_tier = st.selectbox('City Tier', ['Tier 1', 'Tier 2', 'Tier 3'], key='city_tier')
    bmi = st.number_input('BMI', min_value=0.0, step=0.1, key='bmi')
    hba1c = st.number_input('HBA1C', min_value=0.0, step=0.1, key='hba1c')
    heart_issues = st.checkbox('Heart Issues', key='heart_issues')
    transplants = st.checkbox('Any Transplants', key='transplants')
    cancer_history = st.checkbox('Cancer History', key='cancer_history')
    major_surgeries = st.number_input('Number of Major Surgeries', min_value=0, step=1, key='major_surgeries')
    smoker = st.checkbox('Smoker', key='smoker')
    age = st.number_input('Age', min_value=0, step=1, key='age')

    if st.button('Predict Charges'):
        hospital_tier = 1 if hospital_tier == 'Tier 1' else (2 if hospital_tier == 'Tier 2' else 3)
        city_tier = 1 if city_tier == 'Tier 1' else (2 if city_tier == 'Tier 2' else 3)
        heart_issues = 1 if heart_issues else 0
        transplants = 1 if transplants else 0
        cancer_history = 1 if cancer_history else 0
        smoker = 1 if smoker else 0

        features = [hospital_tier, city_tier, bmi, hba1c, heart_issues, transplants, cancer_history, major_surgeries, smoker, age]
        charges = predict_charges(features)
        st.write('Predicted Charges:', charges)

        c.execute('''INSERT INTO patients (name, hospital_tier, city_tier, bmi, hba1c, heart_issues, 
                    transplants, cancer_history, major_surgeries, smoker, age, charges) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (st.session_state.full_name, hospital_tier, city_tier, bmi, hba1c, heart_issues, 
                   transplants, cancer_history, major_surgeries, smoker, age, charges))
        conn.commit()

# Footer information
footer_info = """
<div style="border-radius: 25px; background-color: black; padding: 2px; position: fixed; bottom: 2px; height:15%; width: 50%; text-align: center;">
    <p style="color: white; font-size: 15px;">Shyam Ranjan Dubey------<a href="mailto:shyamrdubey@gmail.com">E-Mail</a>------ <a href="https://github.com/im-srd">GitHub</a></p>
    <h3>HEALTHCARE COST ANALYSIS</h3>
</div>
"""

# Run the app
if __name__ == '__main__':
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        homepage()
    else:
        choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Signup'], key='login_signup')
        if choice == 'Login':
            login()
        else:
            signup()

# Display footer
st.markdown(footer_info, unsafe_allow_html=True)
