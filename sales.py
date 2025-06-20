'''import streamlit as st
import pandas as pd
import pickle

# Page configuration
st.set_page_config(page_title="BigMart Sales Predictor", layout="wide")

# Load model
@st.cache_resource
def load_model():
    with open("C:/Users/Windows10/Desktop/first app/salesforcast/bigmart_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

# Load expected columns
@st.cache_data
def load_columns():
    with open("C:/Users/Windows10/Desktop/first app/salesforcast/expected_columns.pkl", "rb") as f:
        expected_columns = pickle.load(f)
    return expected_columns

model = load_model()
expected_columns = load_columns()

# UI layout
st.title("📊 BigMart Sales Prediction App")
st.markdown("Predict sales for BigMart products using store and product features.")

with st.form("prediction_form"):
    st.subheader("Enter Product & Outlet Details")

    col1, col2 = st.columns(2)

    with col1:
        item_mrp = st.number_input("Item MRP (₹)", min_value=0.0, value=100.0, step=1.0)
        outlet_age = st.slider("Outlet Age (in years)", min_value=0, max_value=50, value=10)

    with col2:
        outlet_identifier = st.selectbox("Outlet Identifier", [
            "OUT049", "OUT018", "OUT010", "OUT013", "OUT027",
            "OUT045", "OUT017", "OUT046", "OUT035", "OUT019"
        ])

        outlet_size = st.selectbox("Outlet Size", ["Small", "Medium", "High"])
        outlet_type = st.selectbox("Outlet Type", [
            "Grocery Store", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3"
        ])

    submitted = st.form_submit_button("Predict Sales")

if submitted:
    # Input preparation
    input_data = {
        "Item_MRP": item_mrp,
        "Outlet_age": outlet_age,
        "Outlet_Identifier": outlet_identifier,
        "Outlet_Size": outlet_size,
        "Outlet_Type": outlet_type
    }

    input_df = pd.DataFrame([input_data])

    # Encode categorical features
    categorical_cols = ["Outlet_Identifier", "Outlet_Size", "Outlet_Type"]
    input_encoded = pd.get_dummies(input_df, columns=categorical_cols)

    # Add missing columns and reorder
    for col in expected_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[expected_columns]

    # Prediction
    try:
        prediction = model.predict(input_encoded)[0]
        st.success(f"📈 **Predicted Sales: ₹{prediction:.2f}**")
        st.info(f"Estimated range: ₹{prediction - 714.42:.2f} to ₹{prediction + 714.42:.2f}")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")'''


import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="BigMart Sales Predictor", layout="wide")

@st.cache_resource
def load_model():
    with open("C:/Users/Windows10/Desktop/first app/salesforcast/bigmart_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("📊 BigMart Sales Prediction App")

with st.form("prediction_form"):
    st.subheader("Enter product & outlet details")

    col1, col2 = st.columns(2)
    with col1:
        item_mrp   = st.number_input("Item MRP (₹)", 0.0, value=100.0, step=1.0)
        outlet_age = st.slider("Outlet Age (years)", 0, 50, 10)

    with col2:
        outlet_identifier = st.selectbox("Outlet Identifier", [
            "OUT049","OUT018","OUT010","OUT013","OUT027",
            "OUT045","OUT017","OUT046","OUT035","OUT019"
        ])
        outlet_size = st.selectbox("Outlet Size", ["Small", "Medium", "High"])
        outlet_type = st.selectbox("Outlet Type", [
            "Grocery Store","Supermarket Type1",
            "Supermarket Type2","Supermarket Type3"
        ])

    submitted = st.form_submit_button("Predict Sales")

if submitted:
    # 🔑  Build DataFrame **without** one‑hot encoding
    input_df = pd.DataFrame([{
        "Item_MRP":          item_mrp,
        "Outlet_Identifier": outlet_identifier,
        "Outlet_Size":       outlet_size,
        "Outlet_Type":       outlet_type,
        "Outlet_age":        outlet_age
    }])

    st.write("### Model Input (raw)", input_df)

 

# … previous code (unchanged) …

    input_df = pd.DataFrame([{
        "Item_MRP":          item_mrp,
        "Outlet_Identifier": outlet_identifier,
        "Outlet_Size":       outlet_size,
        "Outlet_Type":       outlet_type,
        "Outlet_age":        outlet_age
    }])

    # 👉 NEW: cast raw categoricals to pandas 'category' dtype
    cat_cols = ["Outlet_Identifier", "Outlet_Size", "Outlet_Type"]
    input_df[cat_cols] = input_df[cat_cols].astype("category")

    st.write("### Model Input (with category dtype)", input_df)

    try:
        pred = model.predict(input_df)[0]
        st.success(f"📈 Predicted Sales: ₹{pred:.2f}")
        st.info(f"Range: ₹{pred - 714.42:.2f} – ₹{pred + 714.42:.2f}")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")


