import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'modelMD.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Streamlit UI
st.title("Cylinder Cost Prediction")

# Inputs
bore = st.number_input("Bore", value=100.0)
stroke = st.number_input("Stroke", value=100.0)
rpc = st.number_input("RPC", value=1.0)
rod = st.number_input("Rod", value=100.0)

# Yes/No Inputs (converted to 0/1)
rbearing = st.selectbox("R bearing", ["No", "Yes"])
bbearing = st.selectbox("B bearing", ["No", "Yes"])
block = st.selectbox("Block", ["No", "Yes"])
vala = st.selectbox("Val A", ["No", "Yes"])

# Convert to DataFrame for model
data = pd.DataFrame([{
    'Bore': bore,
    'Stroke': stroke,
    'RPC': rpc,
    'Rod': rod,
    'Bore2': bore ** 2,
    'Bore_RPC': bore * rpc,
    'Bore_Stroke': rpc * stroke,
    'Bore_Rod': bore * rod,
    'R bearing_Y': 1 if rbearing == 'Yes' else 0,
    'B bearing_Y': 1 if bbearing == 'Yes' else 0,
    'Block_Y': 1 if block == 'Yes' else 0,
    'Val A_Y': 1 if vala == 'Yes' else 0
}])

# Predict
pred_log = model.predict(data)[0]
pred_cost = np.expm1(pred_log)

st.subheader(f"Predicted Total Cost: ₹{pred_cost:.2f}")
