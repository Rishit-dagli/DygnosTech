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

shape = 224

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

u = "https://storage.googleapis.com/rishit-dagli.appspot.com/My_project-1_1.png"
st.image(u, width=150)

# Display markdown content
st.markdown(
    f'<h1 style="color:#000000;font-size:35px;">{"Doctor2"}</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<h1 style="color:#000000;font-size:24px;">{"Witness the magic by simply uploading an image below and let our model do the talking."}</h1>',
    unsafe_allow_html=True,
)
# st.markdown(
#     f'<h1 style="color:#000000;font-size:18px;">{"Please upload your file below:"}</h1>',
#     unsafe_allow_html=True,
# )

# file = st.file_uploader("", type=["jpg", "png"])

# plt.plot(np.array([0, 0.5, 1]), np.array([0, 0.5, 1]))
# plt.show()

# st.line_chart(np.array([0, 0.5, 1]))

# graph = graphviz.Digraph()
#
# graph.edge('Med', 'Dis')
#
# graph.edge('Med', 'S1')
#
# graph.edge('Med', 'S2')
#
# graph.edge('S1', 'Med for S1')
#
# graph.edge('S2', 'Med for S2')
#
# st.graphviz_chart(graph)

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
