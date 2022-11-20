import streamlit as st
import tensorflow as tf
import urllib
import pickle
import tarfile
import cv2
import pytesseract
from PIL import Image

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

def ocr(file):
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = Image.open(file)
    del file
    img = img.save("img.jpg")
    img = cv2.imread('img.jpg')
    custom_config = r'--oem 1 --psm 6'
    a = pytesseract.image_to_string(get_grayscale(img), config=custom_config).split("\n")
    for i in a:
        if i.startswith("Drugs"):
            drugs = i
    pos = 0
    for i in drugs:
        if i == "-":
            drugs = drugs[pos+1:]
        pos += 1
    drugs = drugs.lower().split(",")
    drugs_updated = []
    for i in drugs:
        drugs_updated.append(i.strip())
    return drugs_updated
