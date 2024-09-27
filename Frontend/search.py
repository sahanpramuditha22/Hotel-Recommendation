import streamlit as st
import pandas as pd

# Load the DataFrame (ensure this path is correct)
df = pd.read_pickle('/Users/sahanpramuditha/Documents/GitHub/Hotel-Recommendation/Backend/hotels.pkl')

# Recommendation function to filter hotels
def recommend(df, room_type, country, city, property_type):
    filtered_df = df[
        (df['roomtype'] == room_type) & 
        (df['country'] == country) & 
        (df['city'] == city) & 
        (df['propertytype'] == property_type)
    ]
    recommendations = filtered_df[['hotelname', 'roomtype']].head(5).values.tolist()
    return recommendations

# Define the search page function
def search_page():
    st.title("Hotel Search and Recommendations")
    
    room_type = st.selectbox("Select Room Type", df['roomtype'].unique())
    country = st.selectbox("Select Country", df['country'].unique())
    city = st.selectbox("Select City", df[df['country'] == country]['city'].unique())
    property_type = st.selectbox("Select Property Type", df['propertytype'].unique())
    
    if st.button('Recommend Hotels'):
        try:
            recommendations = recommend(df, room_type, country, city, property_type)
            if recommendations:
                st.write(f"Top hotel recommendations for {city}, {country}:")
                for hotel, room in recommendations:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #f9f9f9;">
                        <strong>Hotel:</strong> {hotel} <br>
                        <strong>Room Type:</strong> {room}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No recommendations found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
