import streamlit as st
import numpy as np
import pandas as pd
import pickle
import datetime
from sklearn.preprocessing import LabelEncoder
import time

# Load the trained model
regressor = pickle.load(open('forest.pkl', 'rb'))

def show_predict_page():
    # Title
    st.title('Healthcare Insurance Price Prediction')

    # Date of birth input
    dob = st.date_input('Date of birth', value=datetime.date(2000,1,1), min_value=datetime.date(1900,1,1))
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    year = today.year
    month = today.month
    date = today.day

    # Input fields
    children = st.slider('How many children do you have?', min_value=0, max_value=10)
    hospital_tier = st.selectbox('Hospital tier (quality of hospital)', ['tier 1', 'tier 2', 'tier 3'])
    city_tier = st.selectbox('City tier (quality of city)', ['tier 1', 'tier 2', 'tier 3'])
    bmi = st.number_input('BMI', min_value=10.0, max_value=100.0, step=0.1)
    gender = st.selectbox("Gender", ['Male', 'Female'])

    # Display BMI category
    if bmi < 18.5:
        st.markdown('Underweight')
    elif 18.5 <= bmi < 25:
        st.markdown('Healthy weight')
    elif 25 <= bmi < 30:
        st.markdown('Overweight')
    elif 30 <= bmi < 40:
        st.markdown('Obese')
    else:
        st.markdown('Severely obese')

    hba1c = st.number_input("HbA1c Level (1 to 10)", min_value=1.0, max_value=10.0, value=6.5, step=0.5)
    heart_issues = st.selectbox("Heart Issues", ['Yes', 'No'])
    any_transplants = st.selectbox("Any Transplants", ['Yes', 'No'])
    cancer_history = st.selectbox("Cancer History", ['Yes', 'No'])
    number_of_majorsurgeries = st.slider("Number of Major Surgeries", min_value=0, max_value=5, value=0)
    smoker = st.selectbox("Smoker", ['Yes', 'No'])
    

    # Button to submit
    ok = st.button('Submit')
    if ok:
        # Create the input DataFrame
        x = pd.DataFrame([[year, month, date, children,
                           hospital_tier, city_tier, bmi, hba1c,
                           heart_issues, any_transplants, cancer_history, number_of_majorsurgeries,
                           smoker, age, gender]],
                         columns=['year', 'month', 'date', 'children',
                                  'hospital tier', 'city tier', 'bmi', 'hba1c',
                                  'heart issues', 'any transplants', 'cancer history', 
                                  'numberofmajorsurgeries', 'smoker', 'age', 'beneficiary_gender'])

        # Label Encoding
        def labelencoding(df, cols):
            le = LabelEncoder()
            for col in cols:
                df[col] = le.fit_transform(df[col])
            return df

        categorical_columns = ['hospital tier', 'city tier', 'heart issues', 
                               'any transplants', 'cancer history', 'smoker', 'beneficiary_gender']
        x = labelencoding(x, categorical_columns)

        # Predict using the loaded model
        with st.spinner('Wait for it...'):
            time.sleep(3)
        st.success("Done!")



        try:
            patient = regressor.predict(x)
            st.subheader(f"Predicted Insurance Price: {patient[0]:.2f}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

