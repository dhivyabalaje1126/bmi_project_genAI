import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# Configure API key
key_variable = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key_variable)

# Set up a streamlit page
st.title('Health Assistant for Fitness')
st.header('This page will help you to get information for your fitness using your BMI value -- tailored for you!')
st.subheader('This is made using Streamlit.')

st.sidebar.subheader('Height')
height = st.sidebar.text_input('Enter your height (in meters)')

st.sidebar.subheader('Weight')
weight = st.sidebar.text_input('Enter your weight (in kg)')

# Remember, both height and weight inputs are in 'text' format when given by the user

# You can use Ctrll+C or Shift+C to stop the streamlit from running

# Calculating BMI
try:
    height = pd.to_numeric(height)
    weight = pd.to_numeric(weight)
    
    if height > 0 and weight > 0:
        bmi = round(weight / (height**2), 2)
        st.sidebar.success(f'BMI value is: {bmi}')
    else:
        st.sidebar.write('Please enter a positive value.')
except:
    st.sidebar.info('Please enter positive values')
    
# User-input
input = st.text_input('Ask your question:')
submit = st.button('Ask! 📄')

#Initializing genai model
model = genai.GenerativeModel('gemini-1.5-flash')
#For me, gemini-1.5-pro limit has exceeded. 
# You can go to Gemini models and select any model you want to use!

# Creating a def function for the genai model
def generate_result(bmi,input):
    if input is not None:
        prompt = f'''
        You are a health assistant who specializes in guiding individuals towards their best
        selves fitness and health-wise through the input you're given. 
        However, the first thing you must do is provide a disclaimer that the advice you're giving
        should not be considered that from a medical practicioner, and the user must always consult with their physician based on pre-existing medical conditions
        and medications. 
        First, tell the user how their BMI {bmi} is, and what state they are in -- obese, heading there, or non-obese. Be gentle and considerate.
        You can then suggest diet types they can follow. Always provide vegan, vegetarian and non-vegetarian diet options. 
        You can also suggest workouts. Provide beginner-friendly options, with variants that can be done in the gym or at home.
        Use the bmi value of the individual provided as {bmi} to generate suggestions.
        '''
        
        result = model.generate_content(input+prompt)
    return result.text

if submit:
    with st.spinner('Result is loading 🔁... '):
        response = generate_result(bmi, input)
        
    st.markdown(':green[Response]')
    st.write(response)
    