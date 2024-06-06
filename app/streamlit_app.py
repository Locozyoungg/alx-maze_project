import streamlit as st
import requests

st.title("Music Recommender")

# Function to sign up a new user
def sign_up(username, email, password):
    url = "http://localhost:8000/users/"
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    return response

# Function to login an existing user
def login(username, password):
    url = "http://localhost:8000/token"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    return response

# Function to fetch recommendations
def fetch_recommendations(token):
    url = "http://localhost:8000/recommendations/1/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = login(username, password)
    if response.status_code == 200:
        st.success("Login successful!")
        token = response.json()["access_token"]
        recommendations_response = fetch_recommendations(token)
        if recommendations_response.status_code == 200:
            for song in recommendations_response.json():
                st.write(song["title"])
        else:
            st.error("Failed to fetch recommendations.")
    else:
        st.error(f"Login failed: {response.json().get('detail')}")

if st.button("Sign Up"):
    email = st.text_input("Email")
    response = sign_up(username, email, password)
    if response.status_code == 200:
        st.success("User created successfully!")
    else:
        st.error(f"Sign up failed: {response.json().get('detail')}")

