import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load Dataset
df = pd.read_csv("data/StudentsPerformance.csv")

# Create Target
df["Performance"] = np.where(df["math score"] >= 60, 1, 0)

# Drop Target Column
df.drop("math score", axis=1, inplace=True)

# Encode Data
encoders = {}

for col in df.select_dtypes(include="object"):
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Train Model
X = df.drop("Performance", axis=1)
y = df["Performance"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

st.title("🎓 Student Performance Prediction")

gender = st.selectbox("Gender", ["female", "male"])

race = st.selectbox(
    "Race",
    ["group A", "group B", "group C", "group D", "group E"]
)

education = st.selectbox(
    "Parental Education",
    [
        "associate's degree",
        "bachelor's degree",
        "high school",
        "master's degree",
        "some college",
        "some high school",
    ],
)

lunch = st.selectbox(
    "Lunch",
    ["free/reduced", "standard"]
)

prep = st.selectbox(
    "Test Preparation",
    ["completed", "none"]
)

reading = st.slider("Reading Score", 0, 100, 50)

writing = st.slider("Writing Score", 0, 100, 50)

if st.button("Predict"):

    data = pd.DataFrame({
        "gender": [gender],
        "race/ethnicity": [race],
        "parental level of education": [education],
        "lunch": [lunch],
        "test preparation course": [prep],
        "reading score": [reading],
        "writing score": [writing],
    })

    for col in data.columns:
        if col in encoders:
            data[col] = encoders[col].transform(data[col])

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.success("✅ High Performance")
    else:
        st.error("❌ Low Performance")
