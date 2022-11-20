# import os
# import random
# import urllib.request
# import cv2
# import numpy as np
import streamlit as st
# import graphviz as graphviz
# import matplotlib.pyplot as plt
# import tensorflow as tf
# from appwrite.client import Client
# from appwrite.input_file import InputFile
# from appwrite.services.storage import Storage
# from PIL import Image
import tensorflow as tf
import urllib
import pickle
import tarfile
import pathlib
import streamlit.components.v1 as components

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
with open("pages/dtech_doctor.html", 'r') as f:
    html_data = f.read()

# Show in webpage
components.html(html_data, width=2000, height=1000)

#u = "https://media-exp1.licdn.com/dms/image/C5603AQFRUUXJfYlB2A/profile-displayphoto-shrink_400_400/0/1649999815837?e=1674086400&v=beta&t=fZVmr6XYrVzxxl0x4mWh24ztwhvwWUgQpd_8Sod6-k4"
#st.image(u, width=150)

# st.markdown(
#     f'<h1 style="color:#000000;font-size:24px;">{"Witness the magic by simply uploading an image below and let our model do the talking."}</h1>',
#     unsafe_allow_html=True,
# )

st.markdown(
    f'<h1 style="color:#000000;font-size:24px;">{"Patients medical history:"}</h1>',
    unsafe_allow_html=True,
)
st.text_area(label='', value='Sleep disorder, consumed paracetamol')

st.markdown(
    f'<h1 style="color:#000000;font-size:18px;">{"Prescribed drug:"}</h1>',
    unsafe_allow_html=True,
)


drug = st.text_input('')

class PostProcess():
    def __init__(self) -> None:
        self.dn = self.load_dn()
        self.se = self.load_se()

    def load_dn(self):
        text = pathlib.Path("drug_name_labelmap.csv").read_text()
        lines = text.split('\n')[1:-1]
        return tf.io.decode_csv(lines, [str(), str()])

    def load_se(self):
        text = pathlib.Path("se_labelmap.csv").read_text()
        lines = text.split('\n')[1:-1]
        return tf.io.decode_csv(lines, [str(), str(), str()])

    def predict(self, x):
        x = x[0]
        x = str(x)
        x = "'" + x + "'"
        i = 0
        flag = False
        for name in self.dn[1].numpy():
            if name.decode('UTF-8') == x:
                flag = True
                id = self.dn[0][i].numpy().decode('UTF-8')
            i += 1
        if not flag:
            return 'OOD'
        i = 0
        out = []
        id = id[:-1]
        id = id[1:]
        for ses in self.se[0].numpy():
            if ses.decode('UTF-8') == id:
                out.append(self.se[2][i].numpy().decode('UTF-8'))
            i += 1
        if out:
            return out[:5]
        else:
            return 'OOD'

with open("pages/serialized", "rb") as f:
    model = pickle.load(f)

def display_se():
    for x in model.predict([drug]):
        st.markdown(
            f'<h1 style="color:#000000;font-size:18px;">{x}</h1>',
            unsafe_allow_html=True,
        )

st.button('Confirm', on_click=display_se)

# file = st.file_uploader("", type=["jpg", "png"])


# def load_to_appwrite():
#     if file is None:
#         st.write("Please upload an image.")
#     else:
#         client = Client()
#         (
#             client.set_endpoint("http://34.139.148.58/v1")
#             .set_project("637009ba1cc4e478f2ac")
#             .set_key(
#                 "f3c9e9b0ed0b3fb2b6029687884b332f7df170546104aff0f9ef0cb10829de1235e2bde03a7b2f1f97e0efa78426fa444da66fa8e750caa9a81a5dc107b68ed785bb7ef3d2149e5f162621a75d1a83749657ddfad7336f2b4aaed96d25ad2b59694d898b0ed9773f7ea1a7237cccc5d4916f4ae96c2fd730b16cc8fd69758a4b"
#             )
#         )
#         storage = Storage(client)
#         result = storage.create_file(
#             "637009d1ea462ff0d224", "unique()", InputFile.from_path("img.jpg")
#         )
#         st.markdown(
#             f'<h1 style="color:#000000;font-size:15px;">{"Thank you for participating in improving and personalizing Weed Detech. The data you put in is anonymized before being used for training."}</h1>',
#             unsafe_allow_html=True,
#         )
#
#
# def load_model():
#     if "model" not in st.session_state:
#         urllib.request.urlretrieve(
#             "https://github.com/Shivesh777/weed-detech/releases/download/model-weights/model.h5",
#             "model.h5",
#         )
#         st.session_state["model"] = tf.keras.models.load_model("model.h5")
#     return st.session_state["model"]


# if file is None:
#     pass
# else:
#     img = Image.open(file)
#     img = img.save("img.jpg")
#
#     image = cv2.imread("img.jpg")
#     image = cv2.resize(image, (shape, shape))
#     image_1 = np.reshape(image, (1, shape, shape, 3))
#     pred = load_model().predict(image_1)
#     startX = int(pred[1][0][0] * 224)
#     startY = int(pred[1][0][1] * 224)
#     endX = int(pred[1][0][2] * 224)
#     endY = int(pred[1][0][3] * 224)
#     cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
#     Image.fromarray(image).save("img.jpg")
#     st.image("img.jpg", use_column_width=True)
#     st.button(label="Opt into testing", on_click=load_to_appwrite)
