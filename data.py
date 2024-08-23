import streamlit as st
import pandas as pd


st.title("this is the Data page")

# Load data

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('data/data.csv')
    return data


st.dataframe(load_data())