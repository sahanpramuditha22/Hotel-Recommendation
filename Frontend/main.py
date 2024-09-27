import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import firebase_admin
from firebase_admin import credentials, db, auth


# Firebase initialization (ensure your credentials file path is correct)
if not firebase_admin._apps:
    cred = credentials.Certificate("/Users/sahanpramuditha/Documents/GitHub/Hotel-Recommendation/hotelrecommend-8cec3-firebase-adminsdk-crlft-d45010beb2.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://hotelrecommend-8cec3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Load hotel data from pickle (replace with actual data loading)
with open('/Users/sahanpramuditha/Documents/GitHub/Hotel-Recommendation/Backend/hotellist.pkl', 'rb') as file:
    hotel_df = pickle.load(file)

# Assuming user_hotel_matrix is stored similarly
with open('/Users/sahanpramuditha/Documents/GitHub/Hotel-Recommendation/Backend/user_hotel_matrix.pkl', 'rb') as file:
    user_hotel_matrix = pickle.load(file)

# Ensure the index of user_hotel_matrix is the User ID
user_hotel_matrix.index = user_hotel_matrix.index.astype(str)  # Ensure IDs are strings

# Define the HotelRecSys class for recommendations
class HotelRecSys:
    def __init__(self, user_hotel_matrix):
        self.user_hotel_matrix = user_hotel_matrix
        self.similarity_matrix = None

    def calc_user_user_similarity(self):
        self.similarity_matrix = cosine_similarity(self.user_hotel_matrix)
        np.fill_diagonal(self.similarity_matrix, 0)  # Ignore self-similarity
        return self.similarity_matrix

    def recommend_hotels(self, user_id, k=5):
        user_idx = self.user_hotel_matrix.index.get_loc(user_id)
        similar_users = np.argsort(self.similarity_matrix[user_idx])[::-1]
        top_similar_users = similar_users[:k]

        user_ratings = self.user_hotel_matrix.iloc[user_idx]
        hotel_scores = np.zeros(self.user_hotel_matrix.shape[1])

        for sim_user_idx in top_similar_users:
            sim_user_ratings = self.user_hotel_matrix.iloc[sim_user_idx]
            hotel_scores += sim_user_ratings

        unrated_hotels = user_ratings[user_ratings == 0].index
        recommendations = [(hotel, score) for hotel, score in zip(self.user_hotel_matrix.columns, hotel_scores) if hotel in unrated_hotels]
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

        return recommendations[:k]

def display_hotel_list_item(hotel, score):
    """
    Displays a hotel in a list with a small border around it.
    """
    st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
            <h4 style="margin: 0;">{hotel}</h4>
            <p style="margin: 0;">Recommendation Score: <strong style="color: {score_color(score)};">{score:.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)


def score_color(score):
    """
    Returns a color for the score based on its value.
    """
    if score >= 4.5:
        return "#4CAF50"  # Green for high scores
    elif 3 <= score < 4.5:
        return "#FF9800"  # Orange for mid-level scores
    else:
        return "#F44336"  # Red for low scores
    
    
# Initialize recommendation system
rec_sys = HotelRecSys(user_hotel_matrix)
rec_sys.calc_user_user_similarity()

# Streamlit app title
st.title("Hotel Recommendation System")

# User Login with User ID
st.sidebar.title('Login')
#selection = st.sidebar.radio("Go to", ["main", "content", ])

#if selection == "main":
 #   st.title("Welcome to the Home Page!")
  #  st.write("Use the navigation bar to explore different pages.")

#elif selection == "Page 1":
 #   content.app()  # Call the `app` function from `page1.py`
    
#def app():
 #   st.title("content")
  #  st.write("Welcome to Page 1! This is content specific to this page.")

# Fetching User ID input
user_id = st.sidebar.text_input('Enter User ID')  # Input for User ID

# Firebase Realtime Database path reference for user verification
def verify_user_id(user_id):
    ref = db.reference('users')
    user = ref.child(user_id).get()
    return user is not None  # Returns True if user exists, False otherwise

# Login logic
if st.sidebar.button('Login'):
    if user_id:
        if verify_user_id(user_id):
            st.success(f"Login successful for User ID: {user_id}")
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
        else:
            st.error("User ID not found in the database.")
    else:
        st.error("Please enter a User ID.")

# Logout button
if st.sidebar.button('Logout'):
    st.session_state.logged_in = False
    st.session_state.user_id = None

# Show recommendations after login
if st.session_state.get('logged_in', False):
    user_id = st.session_state.user_id

    # Ensure the user ID matches the format in the DataFrame
    if user_id in user_hotel_matrix.index:
        try:
            # Fetch top hotel recommendations for the logged-in user
            top_recommendations = rec_sys.recommend_hotels(user_id, k=5)

            # Display the top recommendations
            st.subheader(f"Top 5 recommended hotels for User {user_id}:")
            if top_recommendations:
                with st.container():
                    
                    for hotel, score in top_recommendations:
                        
                        # st.write(f"{hotel} (Score: {score})")
                         display_hotel_list_item(hotel, score)
            else:
                st.warning("No recommendations available at the moment.")

        except KeyError:
            st.error(f"User ID {user_id} not found in the dataset.")
    else:
        st.error(f"User ID {user_id} not found in the dataset.")

