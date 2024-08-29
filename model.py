import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

def get_clean_data():
    data = pd.read_csv("data/data.csv")
    data = data.drop(['Unnamed: 32', 'id'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data

def add_input_fields():
    data = get_clean_data()
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    with st.form(key='input_form'):
        for i, (label, key) in enumerate(slider_labels):
            col = st.columns(2)[i % 2]  # Create columns to arrange sliders
            with col:
                input_dict[key] = st.slider(
                    label,
                    min_value=float(0),
                    max_value=float(data[key].max()),
                    value=float(data[key].mean())
                )
        
        submit_button = st.form_submit_button(label='Update')
    
    return input_dict if submit_button else None

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(['diagnosis'], axis=1)
    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
    return scaled_dict

def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 
                  'Smoothness', 'Compactness', 
                  'Concavity', 'Concave Points',
                  'Symmetry', 'Fractal Dimension']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
            input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
            input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
            input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'], input_data['area_se'],
            input_data['smoothness_se'], input_data['compactness_se'], input_data['concavity_se'],
            input_data['concave points_se'], input_data['symmetry_se'], input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
            input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
            input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
            input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True
    )
    return fig

def save_predictions(input_data, probabilities, prediction ):
    # Ensure the directory exists
    os.makedirs('data', exist_ok=True)

    # Prepare data to be saved
    input_data['prediction'] = 'Benign' if prediction[0] == 0 else 'Malignant'
    input_data['probability_benign'] = probabilities[0]
    input_data['probability_malignant'] = probabilities[1]
    
    # Create a DataFrame
    df = pd.DataFrame([input_data])
    
    # Append data to a CSV file
    df.to_csv('data/prediction_history.csv', mode='a', header=not os.path.exists('data/prediction_history.csv'), index=False)

def add_predictions(input_data):
    model = pickle.load(open("model/model.pkl", "rb"))
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    prediction = model.predict(input_array_scaled)
    probabilities = model.predict_proba(input_array_scaled)[0]
     # Save predictions and all input values
    save_predictions(input_data, probabilities, prediction)

    st.subheader("Cell cluster prediction")
    st.write("The cell cluster is:")
    if prediction[0] == 0:
        st.write("<span class='diagnosis benign'>Benign</span>", unsafe_allow_html=True)
    else:
        st.write("<span class='diagnosis malicious'>Malicious</span>", unsafe_allow_html=True)
    st.write("Probability of being benign: ", model.predict_proba(input_array_scaled)[0][0])
    st.write("Probability of being malicious: ", model.predict_proba(input_array_scaled)[0][1])
    st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")

def process_file_upload(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("Uploaded Data:")
        st.write(data.head())

        # Load model and scaler
        model = pickle.load(open("model/model.pkl", "rb"))
        scaler = pickle.load(open("model/scaler.pkl", "rb"))

        # Scale the data
        scaled_data = scaler.transform(data)
        
        # Make predictions
        predictions = model.predict(scaled_data)
        probabilities = model.predict_proba(scaled_data)
        
        # Add predictions and probabilities to the DataFrame
        data['prediction'] = ['Benign' if p == 0 else 'Malignant' for p in predictions]
        data['probability_benign'] = probabilities[:, 0]
        data['probability_malignant'] = probabilities[:, 1]

        # Display updated DataFrame
        st.write("Predictions:")
        st.write(data)

        # Save results to a new CSV file
        data.to_csv('data/predictions_from_file.csv', index=False)
        st.success("Predictions saved to 'data/predictions_from_file.csv'")

def main():
    st.title("Breast Cancer Predictor")
    st.write("Please connect this app to your cytology lab to help diagnose breast cancer from your tissue sample. This app predicts using a machine learning model whether a breast mass is benign or malignant based on the measurements it receives from your cytology lab. You can also update the measurements by hand using the sliders below.")
    
    # File upload section
    st.subheader("Upload CSV or Excel File")
    uploaded_file = st.file_uploader("Upload your input file", type=['csv', 'xlsx'])
    process_file_upload(uploaded_file)
    
    input_data = add_input_fields()
    
    if input_data:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                radar_chart = get_radar_chart(input_data)
                st.plotly_chart(radar_chart)
            
            with col2:
                add_predictions(input_data)

if __name__ == "__main__":
    main()
