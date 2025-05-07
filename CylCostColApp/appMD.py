import streamlit as st
import pickle
import pandas as pd
import numpy as np

import os
#load the file
model_path = os.path.join(os.path.dirname(__file__), 'modelMD.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)


# Function to preprocess input
def preprocess_input(R_bearing, B_bearing, Block, Val_A, Bore, Stroke, RPC, Rod):
    data = pd.DataFrame({
        'Bore': [Bore],
        'Stroke': [Stroke],
        'RPC': [RPC],
        'Rod': [Rod],
        'R bearing_1': [int(R_bearing == 'Yes')],
        'B bearing_1': [int(B_bearing == 'Yes')],
        'Block_1': [int(Block == 'Yes')],
        'Val A_1': [int(Val_A == 'Yes')],
        'Bore2': [Bore ** 2],
        'Bore_RPC': [Bore * RPC],
        'Bore_Stroke': [RPC * Stroke],
        'Bore_Rod': [Bore * Rod]
    })
    return data

# Streamlit layout
st.title('Cylinder Cost Prediction')

st.sidebar.header("Input Parameters")

# Yes/No Inputs
R_bearing = st.sidebar.selectbox('R bearing', ['Yes', 'No'])
B_bearing = st.sidebar.selectbox('B bearing', ['Yes', 'No'])
Block = st.sidebar.selectbox('Block', ['Yes', 'No'])
Val_A = st.sidebar.selectbox('Val A', ['Yes', 'No'])

# Sliders and input boxes
Bore = st.sidebar.slider('Bore', min_value=50, max_value=300, step=1)
Stroke = st.sidebar.slider('Stroke', min_value=50, max_value=300, step=1)
RPC = st.sidebar.slider('RPC', min_value=5, max_value=50, step=1)
Rod = st.sidebar.slider('Rod', min_value=100, max_value=300, step=1)

# Preprocess the input
data = preprocess_input(R_bearing, B_bearing, Block, Val_A, Bore, Stroke, RPC, Rod)

# Prediction
prediction = model.predict(data)

st.write(f"Predicted Total Cost: {np.expm1(prediction)[0]:.2f}")  # Inverse the log transformation
