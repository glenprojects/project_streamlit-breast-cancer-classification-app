import streamlit as st
import login  # Import the login module
import dashboard, model, predicthistory  # Import other pages as needed


# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Define a function to handle the login state
def check_authentication():
    return st.session_state.get('authenticated', False)

# Define a function to handle logout
def logout():
    st.session_state['authenticated'] = False
    st.session_state.pop('username', None)
    st.session_state['page'] = 'Login'  # Set the page to Login

def main():
    if check_authentication():
        if 'page' not in st.session_state:
            st.session_state['page'] = 'Home'
        
        # Sidebar with logout option
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()
        
        # Navigation menu
        st.sidebar.title("Navigation")
        st.session_state['page'] = st.sidebar.selectbox("Select Page", ["Home", "Dashboard","Model","Classification History"])
        
        # Render the selected page
        if st.session_state['page'] == "Home":
            show_home_page()
        elif st.session_state['page'] == "Dashboard":
            dashboard.show_dashboard()
        elif st.session_state['page'] == "Model":
            model.main()
        elif st.session_state['page'] == "Classification History":
            predicthistory.main()
    else:
        # Show the login form in the sidebar if not authenticated
        login.show_login()
        
        page_bg_img = '''
    
        <style>
        .stApp {

        background-image: url("https://wallpapercave.com/wp/wp7736559.jpg");
        background-size: contain;
        background-position: center;

        }
        </style>
        '''

        st.markdown(page_bg_img, unsafe_allow_html=True)


def show_home_page():
    st.title("Breast Cancer Classification App")
    st.markdown("""
    This app uses machine learning to classify whether a patient has breast cancer or not based on their medical data.
    """)

    st.subheader("Key Features")
    st.markdown(""" 
    - Upload your CSV file containing patient data
    - Select the desired features for classification
    - Choose a machine learning model from the dropdown menu
    - Click 'Classify' to get the predicted result
    - The app also provides a detailed report on the performance of the model
    - The report includes metrics like accuracy, precision, recall, and F1 score
    """)

    st.subheader("App Features")
    st.markdown("""
    - **View Data**: Access proprietary data
    - **Dashboard**: Explore interactive data visualizations for insights.
    """)

    st.subheader("User Benefits")
    st.markdown("""
    - **Data-driven Decisions**: Make informed decisions backed by data analytics.
    - **Easy Machine Learning**: Utilize powerful machine learning algorithms effortlessly.
    - **Live Demo**: Watch a demo video to see the app in action.
    """)
    st.markdown("[Watch Demo Video](#)")

    st.subheader("How to Run Application")
    st.code("""
    # activate virtual environment
    env/scripts/activate
    streamlit run 1_🏠_Home.py
    """, language='bash')

    st.subheader("Machine Learning Integration")
    st.markdown("""
    - **Model Selection**: Choose between two advanced models for accurate predictions.
    - **Seamless Integration**: Integrate predictions into your workflow with a user-friendly interface.
    - **Probability Estimates**: Gain insights into the likelihood of predicted outcomes.
    """)

    st.subheader("Need Help?")
    st.markdown("For collaborations contact me at [hello@azubi.com](mailto:hello@azubi.com).")
    st.button("Repository on GitHub", help="Visit the GitHub repository")

if __name__ == "__main__":
    main()
