# import os
# import random
# import urllib.request
# import cv2
# import numpy as np
import pathlib
import pickle
import tarfile
import urllib

import streamlit as st
import streamlit.components.v1 as components
import tensorflow as tf

u = "https://storage.googleapis.com/rishit-dagli.appspot.com/My_project-1_1.png"
page_title = "Weed Detech"

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
with open("pages/dtech_doctor.html", "r") as f:
    html_data = f.read()

# Show in webpage
components.html(html_data, width=2000, height=350)

st.markdown(
    f'<h1 style="color:#000000;font-size:24px;">{"Patients medical history:"}</h1>',
    unsafe_allow_html=True,
)
st.text_area(label="", value="Sleep disorder, consumed paracetamol")

st.markdown(
    f'<h1 style="color:#000000;font-size:18px;">{"Prescribed drug:"}</h1>',
    unsafe_allow_html=True,
)


drug = st.text_input("")


class PostProcess:
    def __init__(self) -> None:
        self.dn = self.load_dn()
        self.se = self.load_se()

    def load_dn(self):
        text = pathlib.Path("drug_name_labelmap.csv").read_text()
        lines = text.split("\n")[1:-1]
        return tf.io.decode_csv(lines, [str(), str()])

    def load_se(self):
        text = pathlib.Path("se_labelmap.csv").read_text()
        lines = text.split("\n")[1:-1]
        return tf.io.decode_csv(lines, [str(), str(), str()])

    def predict(self, x):
        x = x[0]
        x = str(x)
        x = "'" + x + "'"
        i = 0
        flag = False
        for name in self.dn[1].numpy():
            if name.decode("UTF-8") == x:
                flag = True
                id = self.dn[0][i].numpy().decode("UTF-8")
            i += 1
        if not flag:
            return "OOD"
        i = 0
        out = []
        id = id[:-1]
        id = id[1:]
        for ses in self.se[0].numpy():
            if ses.decode("UTF-8") == id:
                out.append(self.se[2][i].numpy().decode("UTF-8"))
            i += 1
        if out:
            return out[:5]
        else:
            return "OOD"


with open("pages/serialized", "rb") as f:
    model = pickle.load(f)


def display_se():
    st.markdown(
        f'<h4 style="color:#000000; font-family: Arial; font-size:15px; position: relative; top: 1050px">{"Here is a personalized list of possible side effects, based on the patient\'s medical history: "}</h4>',
        unsafe_allow_html=True,
    )

    for x in model.predict([drug]):
        st.markdown(
            f'<h6 style="color:#000000; font-family: Arial; font-size:15px; position: relative; top: 1050px">{x}</h6>',
            unsafe_allow_html=True,
        )


st.button("Confirm", on_click=display_se)

