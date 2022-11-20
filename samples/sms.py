import streamlit as st
from twilio.rest import Client

account_sid = "AC20aaa1377b72c680707b052d7659c45c"
auth_token = st.secrets["TWILIO_AUTH"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    messaging_service_sid="MG5457bf2f2adfefe7e211ff4440d90d42",
    body="Hello",
    to="number",
)

print(message.sid)
