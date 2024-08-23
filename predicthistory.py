import streamlit as st
import pandas as pd
import os

def main():
    
    st.title("Prediction History")
    
    # Load the data
    file_path = 'data/prediction_history.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.write("Below is the history of predictions and inputs:")
        st.dataframe(df)
    else:
        st.write("No prediction history available yet.")

if __name__ == "__main__":
    main()
