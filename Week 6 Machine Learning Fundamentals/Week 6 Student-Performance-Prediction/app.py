import streamlit as st
import pandas as pd
import pickle

# Load Model
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
st.set_page_config(page_title="Student Performance Prediction")

st.title("🎓 Student Performance Prediction")

st.write("Fill the details below and click Predict.")

gender = st.selectbox("Gender", ["female", "male"])

race = st.selectbox(
    "Race/Ethnicity",
    ["group A", "group B", "group C", "group D", "group E"]
)

education = st.selectbox(
    "Parental Level of Education",
    [
        "associate's degree",
        "bachelor's degree",
        "high school",
        "master's degree",
        "some college",
        "some high school",
    ],
)

lunch = st.selectbox("Lunch", ["free/reduced", "standard"])

prep = st.selectbox(
    "Test Preparation Course",
    ["completed", "none"]
)

reading = st.slider("Reading Score", 0, 100, 50)

writing = st.slider("Writing Score", 0, 100, 50)

# Encoding (same as training)
gender = 1 if gender == "male" else 0

race_dict = {
    "group A": 0,
    "group B": 1,
    "group C": 2,
    "group D": 3,
    "group E": 4,
}

edu_dict = {
    "associate's degree": 0,
    "bachelor's degree": 1,
    "high school": 2,
    "master's degree": 3,
    "some college": 4,
    "some high school": 5,
}

lunch = 1 if lunch == "standard" else 0
prep = 0 if prep == "completed" else 1

if st.button("Predict"):

    data = pd.DataFrame([[
        gender,
        race_dict[race],
        edu_dict[education],
        lunch,
        prep,
        reading,
        writing
    ]])

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.success("✅ High Performance")
    else:
        st.error("❌ Low Performance")