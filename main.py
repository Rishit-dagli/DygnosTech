import streamlit as st
import streamlit.components.v1 as components

u = "https://cdn.discordapp.com/attachments/1043363043947581533/1043716871876268132/DYGNOS__2_-removebg-preview.png"
page_title = "Welcome to DygnosTech"

# Set page title and favicon.
st.set_page_config(page_title=page_title, page_icon=u)


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.discordapp.com/attachments/1043363043947581533/1043480856150409257/marcel-strauss-iCR53oVMqcs-unsplash.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )


add_bg_from_url()

# Read file and keep in variable
with open("pages/dtech_main.html", "r") as f:
    html_data = f.read()

# Show in webpage
components.html(html_data, width=2000, height=1000)
