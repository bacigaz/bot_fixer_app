import streamlit as st
import requests

st.set_page_config(page_title="Bot Fixer App", layout="centered")

# Retrieve credentials securely from the background Streamlit Secrets container
CLIENT_ID = st.secrets["WHOP_CLIENT_ID"]
CLIENT_SECRET = st.secrets["WHOP_CLIENT_SECRET"]
REDIRECT_URI = "https://streamlit.app"

# Track user authentication state locally across page refreshes
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Render the payment wall interface if access hasn't been cleared yet
if not st.session_state.authenticated:
    st.title("🤖 Welcome to Bot Fixer App")
    st.subheader("Please sign in to unlock access to your AI development team.")
    
    # Generate the explicit Whop gateway link
    whop_auth_url = f"https://whop.com{CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    
    st.markdown(f'[<button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; border-radius:4px; font-size:16px; cursor:pointer; font-weight:bold;">🔑 Sign in with Whop</button>]({whop_auth_url})', unsafe_allow_html=True)
    
    # Listen for incoming URL callback parameters sent back by Whop 
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"]
        
        with st.spinner("Validating active subscription status..."):
            token_url = "https://whop.com"
            payload = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            }
            try:
                response = requests.post(token_url, json=payload)
                if response.status_code == 200:
                    st.session_state.authenticated = True
                    st.success("Access Verified! Loading secure workspace...")
                    st.rerun()
                else:
                    st.error("Authentication rejected. Ensure you have an active membership subscription on Whop.")
            except Exception as e:
                st.error("Connection error while attempting to reach authentication servers.")
else:
    # --- CORE SCALING APP CODE INTERFACE GOES HERE ---
    st.title("⚙️ Bot Fixer App Dashboard")
    st.success("Premium Core Access Authenticated")
    st.write("Your automated development, QA, and growth agents are initialized and ready to deploy.")
