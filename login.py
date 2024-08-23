import streamlit as st
import bcrypt

# Function to hash passwords
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify passwords
def verify_password(stored_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_password)

# Define user credentials with hashed passwords
credentials = {
    "usernames": {
        "johndoe": {
            "name": "John Doe",
            "password": hash_password("password123")  # Hashed password
        },
        "janedoe": {
            "name": "Jane Doe",
            "password": hash_password("mypassword")  # Hashed password
        }
    }
}

def authenticate(username, password):
    if username in credentials["usernames"]:
        stored_password = credentials["usernames"][username]["password"]
        if verify_password(stored_password, password):
            return True
    return False

def show_login():
    st.sidebar.title("Login")
    
    # Make sure st.form_submit_button() is used inside an st.form()
    with st.sidebar.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
            else:
                st.sidebar.error("Username or password is incorrect")
