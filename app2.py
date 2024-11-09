import streamlit as st
import joblib
import serial
import time
from collections import Counter
import random

# Load Models
model_yield = joblib.load('knn_regression_model.pkl')
model_height = joblib.load('knn_regression_model_height.pkl')
model_fertilizer = joblib.load('knn_fertilizer_model.pkl') # Load your fertilizer prediction model
soiltype_dict = {'Black':0 ,  'Clay':1,  'Loam':2,  'Red':3,  'Sandy':4}
fertilizer_dict = {0: '10-26-26', 1: '14-35-14', 2: '17-17-17', 3: '20-20', 4: '28-28', 5: 'COMPOUND D', 6: 'Urea'}
def_N=8
def_P=16 
def_K=32
Deftemperature=random.randint(20,24)
defhumidity =random.randint(31,35)
# Prediction Functions
def predict_yield(inrow, N, P, K, week_number):
    input_data = [[inrow, N*week_number, P*week_number, K*week_number ]]
    return model_yield.predict(input_data)[0]

def predict_height(inrow, N, P, K,week_number ):
    input_data = [[inrow, N, P, K,week_number]]
    return model_height.predict(input_data)[0]*2.54

def predict_fertilizer(N, P, K, soil_type, temperature, humidity):
    # Preprocess soil type (e.g., one-hot encoding or label encoding)
    # ... your preprocessing logic ...
    input_data = [[N, P, K, soil_type, temperature, humidity]]
    return fertilizer_dict[model_fertilizer.predict(input_data)[0]] # Return the predicted fertilizer type

# Arduino Communication
def get_greenhouse_state_from_arduino(port, baud_rate=9600, timeout=1):
    # ... (same as before, but now also read temperature and humidity)
    pass

# Streamlit App
def app():
    st.title("Rumbi's Tomato Garden Dashboard 🍅")
    arduino_port = st.sidebar.text_input("Arduino Port", "COM6")
    def_N=8
    def_P=16 
    def_K=32
    Deftemperature=21
    defhumidity =33


    # Input Widgets
    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)


        with col1:
            N = st.number_input("Nitrogen (N)", min_value=0,max_value=100,value=def_N)
            inrow = st.number_input("Plant Spacing", min_value=1,max_value=3)
            soil_type_name = st.selectbox("Soil Type", ["Sandy", "Clay", "Loam","black","red"])
            soil_type = soiltype_dict.get(soil_type_name, 0)
           

        with col2:
            K = st.number_input("Potassium (K)", min_value=1,max_value=100,value=def_P)
            week_number = st.number_input("Week Number", min_value=4,max_value=16)
            temperature = st.number_input("Temperature (°C)", min_value=21,max_value=22, value=Deftemperature)

        with col3:
            P = st.number_input("Phosphorus (P)", min_value=0,max_value=100,value=def_K)
            humidity = st.number_input("Humidity (%)", min_value=32,max_value=35 ,value=defhumidity)
            
            

        submitted = st.form_submit_button("Predict Fruit Number")

    if submitted:
        # Yield Prediction
        yield_estimate = predict_yield(inrow, N, P, K, week_number)
        st.subheader("Fruit Number Prediction 🍅")
        st.write(f"Expected Tomato Fruits: {yield_estimate[0]:.2f} tomatoes")

        # Height Prediction
        height_estimate = predict_height(inrow, N, P, K, week_number)
        st.subheader("Height Prediction 📏")
        st.write(f"Estimated Plant Height: {height_estimate[0]:.2f} cm")

        # Fertilizer Recommendation (Using New Function)
        
    # Greenhouse State (with Refresh Button)
    st.subheader("Current Greenhouse State 🌡️🌱")
    if st.button("Refresh Greenhouse Data"):
        def_N=8
        def_P=16 
        def_K=32
        Deftemperature=21
        defhumidity =28
        

    # Optimization Button (Placeholder for now)
    if st.button("Optimize Conditions"):
        fertilizer_recommendation = predict_fertilizer(N, P, K, soil_type, temperature, humidity)
        st.subheader("Fertilizer Recommendation 🌱")
        st.write(f"Recommended Fertilizer: {fertilizer_recommendation}")

        
        # ... (Your optimizatstion logic would go here)

if __name__ == "__main__":
    app()