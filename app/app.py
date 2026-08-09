# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib
# Load the Model
model = joblib.load("../models/best_rent_prediction_model.pkl")
feature_names = joblib.load("../models/feature_names.pkl")
location_columns = [
    col for col in feature_names
    if col.startswith("Location_")
]

locations = [
    col.replace("Location_", "")
    for col in location_columns
]
# Create a Page Title
st.title("🏠 Lagos & Abuja Rent Prediction")
st.write("Enter house details below to estimate the annual rent.")
# Create Input Fields
# Bedrooms
bedrooms = st.number_input(
    "Bedrooms",
    min_value=0,
    max_value=10,
    value=2,
    key="bedrooms"
)

# Bathrooms
bathrooms = st.number_input(
    "Bathrooms",
    min_value=0,
    max_value=10,
    value=2,
    key="bathrooms"
)

# Toilets
toilets = st.number_input(
    "Toilets",
    min_value=0,
    max_value=10,
    value=2,
    key="toilets"
)

# Serviced
serviced = st.selectbox(
    "Serviced?",
    ["No", "Yes"],
    key="serviced"
)

# Newly Built
newly_built = st.selectbox(
    "Newly Built?",
    ["No", "Yes"],
    key="newly_built"
)

# Furnished
furnished = st.selectbox(
    "Furnished?",
    ["No", "Yes"],
    key="furnished"
)

# Location
location = st.selectbox(
    "Location",
    sorted(locations),
    key="location"
)
# Create the Predict Button
if st.button("Predict Rent"):

    new_house = pd.DataFrame(
        np.zeros((1, len(feature_names))),
        columns=feature_names
    )

    new_house["Bedrooms"] = bedrooms
    new_house["Bathrooms"] = bathrooms
    new_house["Toilets"] = toilets

    new_house["Serviced"] = 1 if serviced == "Yes" else 0
    new_house["Newly Built"] = 1 if newly_built == "Yes" else 0
    new_house["Furnished"] = 1 if furnished == "Yes" else 0

    location_column = f"Location_{location}"

    if location_column in new_house.columns:
        new_house[location_column] = 1

    prediction = model.predict(new_house)

    st.success(
        f"Estimated Annual Rent: ₦{prediction[0]:,.0f}"
    )