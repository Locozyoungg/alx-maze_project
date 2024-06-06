import streamlit as st
import requests

st.title("Music Recommender")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post("http://localhost:8000/token", data={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Login successful!")
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        recommendations = requests.get("http://localhost:8000/recommendations/1/", headers=headers)
        if recommendations.status_code == 200:
            for song in recommendations.json():
                st.write(song["title"])
        else:
            st.error("Failed to fetch recommendations.")
    else:
        st.error("Login failed.")

if st.button("Sign Up"):
    email = st.text_input("Email")
    response = requests.post("http://localhost:8000/users/", json={"username": username, "email": email, "password": password})
    if response.status_code == 200:
        st.success("User created successfully!")
    else:
        st.error("Failed to create user.")

