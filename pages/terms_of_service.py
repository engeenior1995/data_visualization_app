import streamlit as st

st.set_page_config(page_title="Terms of Service", page_icon="📝", layout="centered")

st.title("📝 Terms of Service")

st.markdown("""
### ✅ Acceptance of Terms
By accessing and using this Data Visualization App, you accept and agree to be bound by these Terms of Service.

### 👤 User Accounts
- You must be at least 13 years old to use this service
- You are responsible for maintaining the confidentiality of your account
- Provide accurate and complete registration information

### 📁 Data Responsibility
- You retain ownership of all data you upload
- You are responsible for the content and legality of uploaded data
- Do not upload sensitive or confidential information

### ⚠️ Limitations
- The app is provided "as is" without warranties
- We are not liable for data loss or corruption
- Service may be temporarily unavailable for maintenance

### 📊 Acceptable Use
Do not use the app for:
- Illegal activities
- Malicious purposes
- Violating others' rights
- Uploading harmful content

### 🔄 Modifications
We reserve the right to modify these terms at any time.

### 📧 Contact
For questions about these terms:
- **Email:** m.zarqali@outlook.com
- **Phone:** +92 331 3267202
""")

if st.button("← Back to Dashboard"):
    st.switch_page("pages/home.py")