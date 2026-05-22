import streamlit as st

st.set_page_config(page_title="Privacy Policy", page_icon="🔒", layout="centered")

st.title("🔒 Privacy Policy")

st.markdown("""
### 📋 Our Commitment to Privacy
We are committed to protecting your privacy and ensuring the security of your data.

### 📊 Data Collection
- We only collect data that you explicitly upload
- Account information (username, email) for registered users
- Session data for app functionality

### 🔒 Data Security
- All passwords are encrypted using SHA-256 hashing
- Your uploaded data is processed locally and not stored permanently
- We implement industry-standard security measures

### 🚫 No Third-Party Sharing
We do not sell, trade, or share your personal information with third parties.

### 📧 Contact Information
For privacy concerns or data deletion requests:
- **Email:** zarq.ali@example.com
- **Phone:** +92 331 3267202

### 📝 Policy Updates
We may update this policy periodically. Continued use of the app constitutes acceptance of changes.
""")

if st.button("← Back to Dashboard"):
    st.switch_page("pages/3_🏠_Home.py")