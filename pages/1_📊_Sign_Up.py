import streamlit as st
import pandas as pd
import hashlib
import os
import re
from datetime import datetime


st.set_page_config(page_title="Data Visualization App", page_icon="📊", layout="centered")

# Hide sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .signup-box {
        background: linear-gradient(135deg, #1a1f35 0%, #0f172a 100%);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid #334155;
        max-width: 500px;
        margin: 0 auto;
    }
    
    .success-box {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    
    .password-strength {
        margin-top: -10px;
        margin-bottom: 10px;
        font-size: 12px;
    }
    
    .weak { color: #ef4444; }
    .medium { color: #f59e0b; }
    .strong { color: #10b981; }
</style>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Validate email format"""
    # Regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_password_strength(password):
    """Check password strength and return feedback"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    # Digit check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Determine strength level
    if score <= 2:
        return "weak", "🔴 Weak", feedback
    elif score <= 4:
        return "medium", "🟡 Medium", feedback
    else:
        return "strong", "🟢 Strong", feedback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")
os.makedirs(USER_DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(USER_DATA_DIR, "users.csv")


def read_users_csv():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["Username", "Email", "Password_Hash", "Signup_Time"])
    try:
        return pd.read_csv(CSV_FILE)
    except Exception:
        return pd.DataFrame(columns=["Username", "Email", "Password_Hash", "Signup_Time"])

# ---------- SESSION STATE ----------
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = False
if 'new_user' not in st.session_state:
    st.session_state.new_user = None
if 'password_strength' not in st.session_state:
    st.session_state.password_strength = ""

# ---------- UI ----------
st.markdown("<h1 style='text-align: center; color: #FACC15;'>🚀 Create Account</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Join our data visualization platform</p>", unsafe_allow_html=True)

if st.session_state.signup_success:
    # Success message
    st.markdown(f"""
    <div class='success-box'>
        <h2>✅ Account Created Successfully!</h2>
        <p>Welcome, <strong>{st.session_state.new_user}</strong>!</p>
        <p>Your account has been created successfully.</p>
        <br>
        <p>You can now log in to access your dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Go to Login", use_container_width=True):
            st.session_state.signup_success = False
            st.switch_page("pages/2_🔐_Log_In.py")
    with col2:
        if st.button("🏠 Go to Home", use_container_width=True):
            st.session_state.signup_success = False
            st.session_state.logged_in = True
            st.session_state.username = st.session_state.new_user
            st.switch_page("pages/3_🏠_Home.py")
    
    st.stop()

# ---------- SIGNUP FORM ----------
with st.container():
    st.markdown("<div class='signup-box'>", unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        email = st.text_input("📧 Email", placeholder="example@email.com")
        
        password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password", 
                               help="Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters")
        
        # Password strength indicator
        if password:
            strength_level, strength_text, feedback = check_password_strength(password)
            st.session_state.password_strength = strength_level
            st.markdown(f'<div class="password-strength {strength_level}">{strength_text}</div>', unsafe_allow_html=True)
            
            if feedback:
                with st.expander("🔍 How to improve your password"):
                    for item in feedback:
                        st.write(f"• {item}")
        
        confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            agree = st.checkbox(" ", value=False)
        with col2:
            st.markdown("I agree to the [Terms & Conditions](#)")
        
        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submitted:
            errors = []
            
            # Validate username
            if not username:
                errors.append("Username is required")
            elif len(username) < 3:
                errors.append("Username must be at least 3 characters")
            elif not username.isalnum():
                errors.append("Username can only contain letters and numbers")
            
            # Validate email
            if not email:
                errors.append("Email is required")
            elif not is_valid_email(email):
                errors.append("Please enter a valid email address (e.g., example@domain.com)")
            
            # Validate password
            if not password:
                errors.append("Password is required")
            elif len(password) < 8:
                errors.append("Password must be at least 8 characters")
            elif password != confirm_password:
                errors.append("Passwords do not match")
            elif st.session_state.password_strength == "weak":
                errors.append("Please use a stronger password")
            
            # Check agreement
            if not agree:
                errors.append("Please accept Terms & Conditions")
            
            # Check for existing user
            df = read_users_csv()
            if not df.empty:
                if username in df['Username'].values:
                    errors.append("Username already exists")
                if email in df['Email'].values:
                    errors.append("Email already registered")
            
            # If no errors, proceed with registration
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                hashed_pass = hash_password(password)
                
                user_data = {
                    "Username": username,
                    "Email": email,
                    "Password_Hash": hashed_pass,
                    "Signup_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                df_new = pd.DataFrame([user_data])
                
                try:
                    df_old = read_users_csv()
                    if df_old.empty:
                        df_final = df_new
                    else:
                        df_final = pd.concat([df_old, df_new], ignore_index=True)

                    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
                        df_final.to_csv(csv_file, index=False)

                    st.session_state.signup_success = True
                    st.session_state.new_user = username
                    st.rerun()
                except PermissionError:
                    st.error("⚠️ Unable to save your account because the storage file is locked or not writable. Close any program using users.csv and try again.")
                except Exception as err:
                    st.error(f"⚠️ An unexpected error occurred while saving your account: {err}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Guest vs Registered Comparison
st.markdown("""
<div style="background: #0f172a; padding: 2rem; border-radius: 15px; margin-top: 2rem; border: 1px solid #334155;">
    <h3 style="text-align: center; color: #FACC15;">🤔 Guest vs Registered Account</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
        <div style="text-align: center; padding: 1rem; border-radius: 10px; background: #1e293b;">
            <h4>👤 Guest Mode</h4>
            <div style="text-align: left; margin-top: 1rem;">
                <p>✓ Try basic features</p>
                <p>✓ Quick access</p>
                <p>✓ No registration needed</p>
                <p>✗ Data not saved</p>
                <p>✗ Limited file size (10MB)</p>
                <p>✗ No export options</p>
            </div>
        </div>
        <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #1e293b 0%, #0f766e 50%); border: 2px solid #0d9488;">
            <h4 style="color: #2dd4bf;">🚀 Registered Account</h4>
            <div style="text-align: left; margin-top: 1rem;">
                <p>✓ Save & resume work</p>
                <p>✓ Export reports (PDF/PNG/HTML)</p>
                <p>✓ Advanced analytics</p>
                <p>✓ Larger files (100MB)</p>
                <p>✓ Team collaboration</p>
                <p>✓ Priority support</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<hr>
<div style='text-align: center; color: #64748b; margin-top: 30px;'>
    <p>Already have an account? <a href='/2_🔐_Log_In' target='_self'>Log In</a></p>
    <p style='font-size: 12px;'>Developed by Muhammad Zarq Ali</p>
</div>
""", unsafe_allow_html=True)