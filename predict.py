import streamlit as st
import tensorflow as tf
import urllib
import pickle
import tarfile

def load_model():
    if "model" not in st.session_state:
        urllib.request.urlretrieve(
            "https://github.com/Rishit-dagli/DygnosTech/releases/download/weights/model.tar.gz",
        )
        file = tarfile.open('serialized.tar.gz')
        file.extractall('./')
        file.close()

        with open('serialized', 'rb') as f:
            st.session_state["model"] = pickle.load(f)
    return st.session_state["model"]

def predict(drug_name):
    return load_model().predict(drug_name)