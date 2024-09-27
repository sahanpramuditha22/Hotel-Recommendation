import streamlit as st 
from streamlit_option_menu import option_menu
import search  # Ensure this is the correct import for your search page
import login
import register
# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Login", "Search", "Signup"],
    )

# Show the page based on the selected option
if selected == "Login":
    login.login_page()  # Ensure this is correctly implemented in `login.py`
elif selected == "Search":
    search.search_page()  # Make sure this function exists in `search.py`
elif selected == "Signup":
    register.user_registration_page()
