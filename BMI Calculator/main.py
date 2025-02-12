import streamlit as st

st.title("BMI Calculator")

# Get user inputs
height = st.slider("Enter your height in cm: ", 50, 250)
weight = st.slider("Enter your weight in kg: ", 10, 250)

# Calculate BMI
bmi = weight / ((height / 100) ** 2)

# Display BMI result
st.write(f"Your BMI is {bmi:.2f}")

# Display BMI categories
st.write('--- BMI Categories ---')
st.write("Underweight: BMI less than 18.5")
st.write("Normal Weight: BMI between 18.5 and 24.9")
st.write("Overweight: BMI between 25 and 29.9")
st.write("Obesity: BMI 30 or greater")