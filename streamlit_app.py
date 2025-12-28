import streamlit as st
import streamlit.components.v1 as components

# Cấu hình page
st.set_page_config(
    page_title="Demo App",
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

# Initialize session state
if 'iframe_url' not in st.session_state:
    st.session_state.iframe_url = ""
if 'iframe_height' not in st.session_state:
    st.session_state.iframe_height = 600

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    iframe_url = st.text_input(
        "Enter URL to load:",
        value="https://example.com",
        help="Enter the full URL including https://"
    )
    
    iframe_height = st.slider(
        "Iframe Height:",
        min_value=300,
        max_value=1200,
        value=600,
        step=50
    )
    
    scrolling = st.checkbox("Enable Scrolling", value=True)
    
    if st.button("Load Iframe", type="primary"):
        st.session_state.iframe_url = iframe_url
        st.session_state.iframe_height = iframe_height
        st.rerun()

# Main content
st.title("🎯 Streamlit Iframe Loader")
st.markdown("---")

# Tabs for different iframe methods
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Basic Iframe", 
    "🔧 Custom HTML", 
    "💉 JS Injection",
    "🎨 Advanced"
])

with tab1:
    st.subheader("Method 1: components.iframe()")
    
    if st.session_state.iframe_url:
        try:
            components.iframe(
                st.session_state.iframe_url,
                height=st.session_state.iframe_height,
                scrolling=scrolling
            )
            st.success(f"✅ Loaded: {st.session_state.iframe_url}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👈 Enter a URL in the sidebar and click 'Load Iframe'")

with tab2:
    st.subheader("Method 2: Custom HTML with components.html()")
    
    custom_url = st.text_input("URL for custom HTML:", value="https://example.com")
    
    if st.button("Load Custom HTML"):
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}
                iframe {{
                    border: none;
                    width: 100%;
                    height: 600px;
                }}
            </style>
        </head>
        <body>
            <iframe src="{custom_url}" 
                    sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                    referrerpolicy="no-referrer">
            </iframe>
        </body>
        </html>
        """
        
        components.html(html_code, height=620)
        st.success(f"✅ Custom HTML loaded: {custom_url}")

with tab3:
    st.subheader("Method 3: Iframe with JS Injection")
    
    target_url = st.text_input("Target URL:", value="https://example.com", key="js_url")
    js_payload = st.text_area(
        "JavaScript Payload:",
        value="""console.log('Loaded from Streamlit');
alert('Hello from injected JS!');""",
        height=150
    )
    
    if st.button("Inject & Load"):
        # Create HTML page with JS injection
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
            </style>
        </head>
        <body>
            <div id="info">
                🎯 Target: <span id="url">{target_url}</span> | 
                Status: <span id="status">Loading...</span>
            </div>
            <iframe id="targetFrame" src="{target_url}"></iframe>
            
            <script>
                // Your injected payload
                {js_payload}
                
                // Monitor iframe loading
                const frame = document.getElementById('targetFrame');
                const status = document.getElementById('status');
                
                frame.onload = function() {{
                    status.textContent = '✅ Loaded';
                    status.style.color = '#00ff00';
                    
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
                    console.log('Received message:', event.data);
                }});
                
                // Send message to parent (Streamlit)
                if (window.parent !== window) {{
                    window.parent.postMessage({{
                        type: 'streamlit_child',
                        status: 'loaded',
                        url: '{target_url}'
                    }}, '*');
                }}
            </script>
        </body>
        </html>
        """
        
        components.html(injection_html, height=650, scrolling=False)

with tab4:
    st.subheader("Method 4: Advanced - Multiple Iframes")
    
    st.markdown("**Load multiple pages simultaneously:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        url1 = st.text_input("URL 1:", value="https://example.com", key="url1")
    with col2:
        url2 = st.text_input("URL 2:", value="https://httpbin.org/html", key="url2")
    
    if st.button("Load Both"):
        advanced_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 10px;
                    background: #0e1117;
                    font-family: sans-serif;
                }}
                .container {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                    height: 100vh;
                }}
                .iframe-wrapper {{
                    border: 2px solid #333;
                    border-radius: 8px;
                    overflow: hidden;
                    background: #1a1a1a;
                }}
                .iframe-header {{
                    padding: 8px;
                    background: #262626;
                    color: #00ff00;
                    font-size: 12px;
                    font-family: monospace;
                }}
                iframe {{
                    width: 100%;
                    height: calc(100% - 32px);
                    border: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="iframe-wrapper">
                    <div class="iframe-header">🌐 Frame 1: {url1}</div>
                    <iframe src="{url1}" sandbox="allow-scripts allow-same-origin"></iframe>
                </div>
                <div class="iframe-wrapper">
                    <div class="iframe-header">🌐 Frame 2: {url2}</div>
                    <iframe src="{url2}" sandbox="allow-scripts allow-same-origin"></iframe>
                </div>
            </div>
            
            <script>
                console.log('Multiple iframes loaded');
                
                // Monitor both frames
                document.querySelectorAll('iframe').forEach((frame, index) => {{
                    frame.onload = () => console.log(`Frame ${{index + 1}} loaded`);
                    frame.onerror = () => console.log(`Frame ${{index + 1}} error`);
                }});
            </script>
        </body>
        </html>
        """
        
        components.html(advanced_html, height=700)

# Footer info
st.markdown("---")
st.markdown("""
### 📝 Usage Notes:
- **Basic Iframe**: Simple wrapper using `components.iframe()`
- **Custom HTML**: Full control over iframe attributes
- **JS Injection**: Inject custom JavaScript alongside iframe
- **Advanced**: Load multiple iframes with custom styling

### ⚠️ Security Notes:
- Iframes have sandbox restrictions
- Cross-origin access is limited by CORS
- Use `allow-scripts` carefully in production
- PostMessage is the safe way to communicate between frames
""")

# Debug info
with st.expander("🔍 Debug Info"):
    st.json({
        "current_url": st.session_state.iframe_url,
        "iframe_height": st.session_state.iframe_height,
        "session_state": dict(st.session_state)
    })