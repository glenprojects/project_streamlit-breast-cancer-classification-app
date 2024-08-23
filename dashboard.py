import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard():

    # Load the dataset
    data = pd.read_csv('data/data.csv')

    # Preprocess the data
    data = data.drop(['Unnamed: 32', 'id'], axis=1, errors='ignore')  # Drop irrelevant columns
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})  # Convert 'M' and 'B' to numeric values

    # Display the dataset
    st.title('Breast Cancer Diagnosis EDA')
    st.write('## Dataset')
    st.write(data.head())

    st.write('## Exploratory Data Analysis')

    # Dynamic Filter for Diagnosis
    diagnosis_filter = st.selectbox("Select Diagnosis Type", options=['All', 'Malignant', 'Benign'])
    if diagnosis_filter != 'All':
        data = data[data['diagnosis'] == (1 if diagnosis_filter == 'Malignant' else 0)]

    # Pair 1: Distribution of Diagnosis & Scatter Plot
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(data, x='diagnosis', title='Distribution of Diagnosis',
                            labels={'diagnosis': 'Diagnosis'}, 
                            category_orders={'diagnosis': [0, 1]})
        fig1.update_xaxes(tickvals=[0, 1], ticktext=['Benign', 'Malignant'])
        st.plotly_chart(fig1)

    with col2:
        scatter_x = st.selectbox("Select X-axis for Scatter Plot", options=data.columns[1:10], index=1)
        scatter_y = st.selectbox("Select Y-axis for Scatter Plot", options=data.columns[1:10], index=3)
        fig2 = px.scatter(data, x=scatter_x, y=scatter_y, color='diagnosis', title=f'{scatter_x} vs {scatter_y}')
        st.plotly_chart(fig2)

    # Pair 2: Box Plot for Perimeter Mean & Correlation Heatmap
    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.box(data, x='diagnosis', y='perimeter_mean', title='Perimeter Mean by Diagnosis')
        st.plotly_chart(fig3)

    with col4:
        corr = data.corr()
        fig4 = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='Viridis'))
        fig4.update_layout(title='Feature Correlation Heatmap', xaxis_nticks=36)
        st.plotly_chart(fig4)

    # Analysis Section
    if st.button('Show Analysis'):
        st.write('## Analysis')

        # Pair 3: Diagnosis Distribution (Pie Chart) & Radius vs Perimeter Mean
        col5, col6 = st.columns(2)

        with col5:
            fig5 = px.pie(data, names='diagnosis', title='Diagnosis Distribution',
                          labels={'diagnosis': 'Diagnosis'},
                          color_discrete_sequence=px.colors.sequential.RdBu)
            fig5.update_traces(textinfo='percent+label')
            st.plotly_chart(fig5)

        with col6:
            fig6 = px.scatter(data, x='radius_mean', y='perimeter_mean', color='diagnosis',
                              title='Radius Mean vs Perimeter Mean',
                              hover_data=['texture_mean', 'area_mean'])
            st.plotly_chart(fig6)

        # Pair 4: Box Plot for Area Mean & Violin Plot for Texture Mean
        col7, col8 = st.columns(2)

        with col7:
            fig7 = px.box(data, x='diagnosis', y='area_mean', title='Area Mean by Diagnosis',
                          points='all')
            st.plotly_chart(fig7)

        with col8:
            fig8 = px.violin(data, x='diagnosis', y='texture_mean', box=True, points="all",
                             title='Texture Mean by Diagnosis',
                             hover_data=['smoothness_mean', 'compactness_mean'])
            st.plotly_chart(fig8)

        # Analysis content
        st.write("""
        1. **Diagnosis Distribution**: The pie chart confirms the dataset is imbalanced, with more 'M' (Malignant) cases than 'B' (Benign).
        2. **Radius vs Perimeter**: Scatter plot shows that larger radii generally correspond to larger perimeters, particularly in malignant cases.
        3. **Area Mean Distribution**: Box plot highlights that malignant tumors have a larger area mean compared to benign tumors.
        4. **Texture Mean**: Violin plot shows the distribution of texture mean across both diagnoses, with malignant tumors showing a broader distribution.
        """)

if __name__ == "__main__":
    show_dashboard()

