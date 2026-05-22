import streamlit as st
import pandas as pd
import hashlib
import os
import time
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")
os.makedirs(USER_DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(USER_DATA_DIR, "users.csv")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def read_users_csv():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["Username", "Email", "Password_Hash", "Signup_Time"])
    try:
        return pd.read_csv(CSV_FILE)
    except Exception:
        return pd.DataFrame(columns=["Username", "Email", "Password_Hash", "Signup_Time"])

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def authenticate_user(username_email, password):
    df = read_users_csv()
    if df.empty:
        return False

    hashed_pass = hash_password(password)
    
    # Check if username/email and password match
    user = df[(df['Username'] == username_email) | (df['Email'] == username_email)]
    
    if not user.empty and user.iloc[0]['Password_Hash'] == hashed_pass:
        return user.iloc[0]['Username']
    return False

# UI Header
st.markdown("<h1 style='text-align: center; color: #FACC15;'>🔐 Welcome Back</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Login to access your dashboard</p>", unsafe_allow_html=True)

# Login Form
with st.container():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # Create the form
    with st.form("login_form", clear_on_submit=True):
        username_email = st.text_input("👤 Username or Email", placeholder="Enter username or email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            remember = st.checkbox(" ", value=False, key="remember_me")
        with col2:
            st.markdown("Remember Me")
        
        # Form submit button - THIS RETURNS True WHEN CLICKED
        submitted = st.form_submit_button("🔓 Login", use_container_width=True)
        
        # Now check if form was submitted
        if submitted:
            if not username_email or not password:
                st.error("⚠️ Please fill in all fields")
            elif '@' in username_email and not is_valid_email(username_email):
                st.error("❌ Please enter a valid email address")
            else:
                user = authenticate_user(username_email, password)
                if user:
                    # CRITICAL: Set ALL session states properly
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.session_state.guest_mode = False  # Explicitly set to False
                    st.session_state.viz_count = 0  # Reset for registered user
                    st.session_state.is_registered_user = True  # Add this flag
                    
                    st.success(f"✅ Welcome back, {user}!")
                    st.balloons()
                    
                    # Give time to see success message, then redirect
                    time.sleep(1.5)
                    
                    # Redirect to home page
                    st.switch_page("pages/3_🏠_Home.py")
                else:
                    st.markdown("""
                    <div class='error-box'>
                        ❌ Invalid username/email or password
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
# Guest Mode Option
st.markdown("---")  # Add a separator line
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <p style="color: #64748b; font-style: italic;">No account? Try guest mode:</p>
</div>
""", unsafe_allow_html=True)

# Guest button with better styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("👤 Continue as Guest", use_container_width=True, type="secondary"):
        st.session_state.guest_mode = True
        st.session_state.logged_in = True
        st.session_state.username = "Guest User"
        st.success("Entering guest mode...")
        st.switch_page("pages/3_🏠_Home.py")
# Footer
st.markdown("""
<hr>
<div style='text-align: center; color: #64748b; margin-top: 30px;'>
    <p>Don't have an account? <a href='/1_📊_Sign_Up' target='_self'>Sign Up</a></p>
    <p style='font-size: 12px;'>Developed by Muhammad Zarq Ali</p>
</div>
""", unsafe_allow_html=True)