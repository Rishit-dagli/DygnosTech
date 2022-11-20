# import os
# import random
# import urllib.request
# import cv2
# import numpy as np
import pickle

import cv2
import graphviz as graphviz
import pytesseract
import streamlit as st
from twilio.rest import Client

# import matplotlib.pyplot as plt
# import tensorflow as tf
# from appwrite.client import Client
# from appwrite.input_file import InputFile
# from appwrite.services.storage import Storage
# from PIL import Image
import streamlit.components.v1 as components
from PIL import Image

u = "https://storage.googleapis.com/rishit-dagli.appspot.com/My_project-1_1.png"
page_title = "Patient Upload Screen"

# Set page title and favicon.
st.set_page_config(page_title=page_title, page_icon=u)

def send_message(number, content):
    account_sid = 'AC20aaa1377b72c680707b052d7659c45c' 
    auth_token = st.secrets["TWILI_AUTH"]
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG5457bf2f2adfefe7e211ff4440d90d42', 
                                body='Hello',
                                to='number' 
                            ) 

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
with open("pages/dtech_patient.html", "r") as f:
    html_data = f.read()

# Show in webpage
components.html(html_data, width=2000, height=200)

# Display markdown content
st.markdown(
    f'<h1 style="color:#000000;font-size:35px;">{"Prescription Upload Screen"}</h1>',
    unsafe_allow_html=True,
)
# st.markdown(
#     f'<h1 style="color:#000000;font-size:24px;">{"Witness the magic by simply uploading an image below and let our model do the talking."}</h1>',
#     unsafe_allow_html=True,
# )
st.markdown(
    f'<h1 style="color:#000000;font-size:18px;">{"Please upload your prescription below:"}</h1>',
    unsafe_allow_html=True,
)

file = st.file_uploader("", type=["jpg", "png"])


def ocr(file):
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img = Image.open(file)
    del file
    img = img.save("img.jpg")
    img = cv2.imread("img.jpg")
    custom_config = r"--oem 1 --psm 6"
    a = pytesseract.image_to_string(get_grayscale(img), config=custom_config).split(
        "\n"
    )
    for i in a:
        if i.startswith("Drugs"):
            drugs = i
    pos = 0
    for i in drugs:
        if i == "-":
            drugs = drugs[pos + 1 :]
        pos += 1
    drugs = drugs.lower().split(",")
    drugs_updated = []
    for i in drugs:
        drugs_updated.append(i.strip())
    return drugs_updated


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


if file is None:
    pass
else:
    drugs = ocr(file)
    dictionary = {}
    for i in drugs:
        dictionary[i] = model.predict([i])
    graph = graphviz.Digraph(format='dot')
    graph.graph_attr['rankdir'] = 'LR'
    graph.graph_attr["bgcolor"] = "#00000000"

    for k in dictionary:
        graph.edge("Alex", k)
        for i in dictionary[k]:
            graph.edge(k, i)

    st.graphviz_chart(graph)

    st.markdown(
        f'<h1 style="color:#000000;font-size:18px;">{"Mobile number, to receive a summary:"}</h1>',
        unsafe_allow_html=True,
    )
    txt = st.text_input("")
    st.button("Send Summary", on_click=send_message(txt, """Dear User,
        Here is a summary of your prescription:
        Having """ + drugs[0] + "can cause" + model.predict([drugs[0]])[0]))
