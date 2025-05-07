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
# Bore
col1, col2 = st.columns([3, 1])
with col1:
    bore = st.slider("Bore", 50.0, 300.0, 100.0, 1.0, key="bore_slider")
with col2:
    bore_input = st.number_input(" ", 50.0, 300.0, value=bore, step=1.0, key="bore_input")
    if bore_input != bore:
        bore = bore_input

# Stroke
col3, col4 = st.columns([3, 1])
with col3:
    stroke = st.slider("Stroke", 50.0, 2000.0, 300.0, 10.0, key="stroke_slider")
with col4:
    stroke_input = st.number_input("  ", 50.0, 2000.0, value=stroke, step=10.0, key="stroke_input")
    if stroke_input != stroke:
        stroke = stroke_input

# RPC
col5, col6 = st.columns([3, 1])
with col5:
    rpc = st.slider("RPC", 1.0, 10.0, 2.0, 0.1, key="rpc_slider")
with col6:
    rpc_input = st.number_input("   ", 1.0, 10.0, value=rpc, step=0.1, key="rpc_input")
    if rpc_input != rpc:
        rpc = rpc_input

# Rod
col7, col8 = st.columns([3, 1])
with col7:
    rod = st.slider("Rod", 20.0, 150.0, 50.0, 1.0, key="rod_slider")
with col8:
    rod_input = st.number_input("    ", 20.0, 150.0, value=rod, step=1.0, key="rod_input")
    if rod_input != rod:
        rod = rod_input


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
