import streamlit as st
import pandas as pd
import pickle

# Function to load the DataFrame (already stored as a pickle file)
df = pd.read_pickle('/Users/sahanpramuditha/Documents/GitHub/Hotel-Recommendation/Backend/hotels.pkl')

def recommend(df, room_type, country, city, property_type):
    # Your recommendation logic, filter based on the parameters
    filtered_df = df[
        (df['roomtype'] == room_type) & 
        (df['country'] == country) & 
        (df['city'] == city) & 
        (df['propertytype'] == property_type)
    ]
    
    # Get top recommendations (assumed to be 5, adjust as needed)
    recommendations = filtered_df[['hotelname', 'roomtype']].head(5).values.tolist()
    return recommendations

# Assuming the recommendation function is stored in another file
# import your recommendation function (ensure the function is correctly implemented in 'recommend_function.py')


# Function to load any model using pickle (if needed)
def load_model(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
    


# Streamlit app title
st.title("Hotel Recommendation System")

# Display the loaded DataFrame for confirmation
#st.write("Loaded Hotel Data:")
#st.write(df)

# Display columns to verify if 'hotel_name' exists
#st.write("Columns in the DataFrame:")
#stst.write(df.columns)


# User inputs for filtering
# Room type selection (unique room types from the DataFrame)
room_type = st.selectbox("Select Room Type", df['roomtype'].unique())

# Country selection
country = st.selectbox("Select Country", df['country'].unique())

# City selection (only cities from the selected country)
city = st.selectbox("Select City", df[df['country'] == country]['city'].unique())

# Property type selection
property_type = st.selectbox("Select Property Type", df['propertytype'].unique())

# When the user clicks the "Recommend Hotels" button
if st.button('Recommend Hotels'):
    try:
        # Call the recommendation function, passing the user inputs
        recommendations = recommend(df, room_type, country, city, property_type)

        # If there are recommendations, display them
        if len(recommendations) > 0:
            st.write(f"Top hotel recommendations for {city}, {country}:")
            for hotel, room in recommendations:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin: 10px 0; background-color: #f9f9f9;">
                    <strong>Hotel:</strong> {hotel} <br>
                    <strong>Room Type:</strong> {room}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found for the selected criteria.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
