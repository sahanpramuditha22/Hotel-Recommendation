import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your-firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://hotelrecommend-8cec3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Function to generate a new user ID starting from 2001
def generate_user_id():
    users_ref = db.reference('users')
    users_data = users_ref.get()

    # Get all user IDs as integers
    existing_ids = [int(user_id) for user_id in users_data.keys() if user_id.isdigit() and 1000 <= int(user_id) <= 2000]

    # If there are no users, start with 2001
    if not existing_ids:
        return 2001

    # Otherwise, find the maximum existing ID and generate the next one
    max_existing_id = max(existing_ids)
    return max_existing_id + 1

# Function to register a user in Firebase Realtime Database
def register_user(user_id, username, email, preferences):
    user_ref = db.reference(f'users/{user_id}')
    user_data = {
        'registered': True,
        'username': username,
        'email': email,
        'preferences': preferences
    }
    user_ref.set(user_data)
    st.success(f"User {username} has been registered successfully with ID {user_id}!")

# Streamlit frontend for User Registration
def user_registration_page():
    st.title("User Registration")
    
    # Automatically generate user ID
    user_id = generate_user_id()
    st.text(f"Generated User ID: {user_id}")
    
    # Input fields for registration
    username = st.text_input("Username", placeholder="Enter your username")
    email = st.text_input("Email", placeholder="Enter your email")
    room_type = st.selectbox("Preferred Room Type", ["deluxe", "standard", "suite"])
    city = st.text_input("Preferred City", placeholder="Enter your preferred city")
    
    # Register button
    if st.button("Register"):
        if username and email and city:
            preferences = {
                "room_type": room_type,
                "city": city
            }
            register_user(user_id, username, email, preferences)
        else:
            st.error("Please fill in all fields!")

# Run the Streamlit app
if __name__ == '__main__':
    user_registration_page()
