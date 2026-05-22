import streamlit as st
import time
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Data Visualization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for guest mode
if 'guest_mode' not in st.session_state:
    st.session_state.guest_mode = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Custom CSS with advanced animations
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main Header with animated gradient and floating effect */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #667eea 100%);
        background-size: 300% 300%;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: gradientFlow 8s ease infinite, floatUpDown 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Title text animation */
    .title-text {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        background: linear-gradient(90deg, 
            #FFD700, 
            #FFA500, 
            #FF6347, 
            #FF1493, 
            #9370DB, 
            #00BFFF);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: colorFlow 5s linear infinite, textGlow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    @keyframes colorFlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(255, 215, 0, 0.3), 0 0 20px rgba(255, 215, 0, 0.2); }
        to { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5), 0 0 30px rgba(255, 215, 0, 0.3); }
    }
    
    /* Subtitle animation */
    .subtitle-text {
        font-size: 1.5rem;
        opacity: 0.9;
        animation: fadeInOut 3s ease-in-out infinite;
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0.7; transform: scale(0.98); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    /* Animated buttons with bounce effect */
    .animated-button {
        animation: buttonPulse 2s infinite, buttonBounce 1s infinite alternate;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes buttonPulse {
        0% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(250, 204, 21, 0); }
        100% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0); }
    }
    
    @keyframes buttonBounce {
        from { transform: translateY(0); }
        to { transform: translateY(-5px); }
    }
    
    /* Button hover effects */
    .animated-button:hover {
        animation: none;
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 30px rgba(250, 204, 21, 0.3);
    }
    
    /* Button text animation */
    .button-text {
        display: inline-block;
        animation: textShake 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes textShake {
        from { transform: translateX(-2px); }
        to { transform: translateX(2px); }
    }
    
    /* Option cards with floating animation */
    .option-card {
        padding: 2rem;
        border-radius: 15px;
        background: #1e293b;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
        animation: cardFloat 6s ease-in-out infinite;
    }
    
    @keyframes cardFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-8px) rotate(0.5deg); }
        50% { transform: translateY(0) rotate(0deg); }
        75% { transform: translateY(8px) rotate(-0.5deg); }
    }
    
    /* Moving icons */
    .icon-container {
        position: relative;
        height: 120px;
        width: 100%;
        margin-bottom: 1rem;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .moving-icon {
        font-size: 4rem;
        position: absolute;
        animation-duration: 2s;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
    }
    
    .rocket {
        animation-name: rocketLaunch;
        color: #3b82f6;
    }
    
    .lock {
        animation-name: lockBounce;
        color: #10b981;
    }
    
    .guest {
        animation-name: guestFloat;
        color: #f59e0b;
    }
    
    @keyframes rocketLaunch {
        0% { transform: translateY(40px) scale(0.8); opacity: 0.5; }
        50% { transform: translateY(0) scale(1.2); opacity: 1; }
        100% { transform: translateY(-40px) scale(0.8); opacity: 0.5; }
    }
    
    @keyframes lockBounce {
        0% { transform: translateY(30px) rotate(0deg); }
        25% { transform: translateY(0) rotate(15deg); }
        50% { transform: translateY(-30px) rotate(0deg); }
        75% { transform: translateY(0) rotate(-15deg); }
        100% { transform: translateY(30px) rotate(0deg); }
    }
    
    @keyframes guestFloat {
        0% { transform: translateY(35px) scale(1) rotate(0deg); }
        33% { transform: translateY(0) scale(1.1) rotate(5deg); }
        66% { transform: translateY(-25px) scale(1) rotate(-5deg); }
        100% { transform: translateY(35px) scale(0.9) rotate(0deg); }
    }
    
    /* Badge animation */
    .badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        animation: badgeSpin 3s linear infinite, badgePulse 2s ease-in-out infinite;
        z-index: 10;
    }
    
    @keyframes badgeSpin {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(5deg); }
        50% { transform: rotate(0deg); }
        75% { transform: rotate(-5deg); }
        100% { transform: rotate(0deg); }
    }
    
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Sparkles animation */
    .sparkle {
        position: absolute;
        font-size: 1.5rem;
        opacity: 0;
        animation: sparkleTwinkle 2s infinite;
    }
    
    @keyframes sparkleTwinkle {
        0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.5) rotate(180deg); }
    }
    
    /* Floating particles */
    .floating-particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: radial-gradient(circle, rgba(250, 204, 21, 0.8), rgba(250, 204, 21, 0));
        border-radius: 50%;
        animation: particleDrift 10s linear infinite;
        pointer-events: none;
    }
    
    @keyframes particleDrift {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translate(var(--tx, 100px), var(--ty, -100px)) rotate(360deg); opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for dynamic particles and interactions
interactive_js = """
<script>
// Create floating particles
function createParticles() {
    const container = document.querySelector('.main-header');
    if (!container) return;
    
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.setProperty('--tx', (Math.random() * 200 - 100) + 'px');
        particle.style.setProperty('--ty', (Math.random() * 200 - 100) + 'px');
        particle.style.animationDelay = Math.random() * 5 + 's';
        container.appendChild(particle);
    }
}

// Add sparkles to buttons
function addSparkles() {
    const buttons = document.querySelectorAll('.animated-button');
    buttons.forEach(button => {
        setInterval(() => {
            if (Math.random() > 0.7) {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.innerHTML = '✨';
                sparkle.style.left = Math.random() * 80 + 10 + '%';
                sparkle.style.top = Math.random() * 80 + 10 + '%';
                button.appendChild(sparkle);
                
                setTimeout(() => {
                    if (sparkle.parentNode) {
                        sparkle.parentNode.removeChild(sparkle);
                    }
                }, 2000);
            }
        }, 1000);
    });
}

// Button click effects
function addButtonEffects() {
    document.querySelectorAll('.animated-button').forEach(button => {
        button.addEventListener('click', function() {
            // Create ripple effect
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = event.clientX - rect.left - size/2;
            const y = event.clientY - rect.top - size/2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.parentNode.removeChild(ripple);
                }
            }, 600);
        });
    });
}

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    addSparkles();
    addButtonEffects();
    
    // Add floating effect to cards
    const cards = document.querySelectorAll('.option-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.5) + 's';
    });
});
</script>
"""

# Inject JavaScript
html(interactive_js, height=0)

# Main landing page with animated title
st.markdown("""
<div class='main-header'>
    <div class='title-text'>📊 Advanced Data Visualization Dashboard</div>
    <div class='subtitle-text'>Analyze, Visualize, and Transform Your Data</div>
</div>
""", unsafe_allow_html=True)

# Guest mode warning/notice
if st.session_state.guest_mode:
    st.markdown("""
    <div style='background: #fef3c7; border-left: 5px solid #f59e0b; padding: 1rem; border-radius: 10px; margin-top: 1rem; color: #92400e; animation: warningPulse 2s infinite;'>
        <strong>👤 Guest Mode Active</strong> - You're using the app as a guest. 
        <a href='/?clear_guest=true' style='color: #92400e; text-decoration: underline;'>Click here to switch to registered mode</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Choose Your Access Level")
st.markdown("Select how you want to use our platform:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='option-card'>
        <div class='icon-container'>
            <div class='moving-icon rocket'>🚀</div>
        </div>
        <h2>Sign Up</h2>
        <p style='color: #94a3b8; margin-bottom: 15px;'>Create a permanent account with full features</p>
        <div style='display: flex; flex-direction: column; gap: 8px; margin-top: 15px; text-align: left; width: 100%;'>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Save your work
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Export reports
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Advanced analytics
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Animated button with moving text
    signup_button = st.button("🚀 **Get Started** 🚀", 
                             key="signup_btn", 
                             use_container_width=True,
                             type="primary")
    
    if signup_button:
        st.switch_page("pages/1_📊_Sign_Up.py")

with col2:
    st.markdown("""
    <div class='option-card'>
        <div class='icon-container'>
            <div class='moving-icon lock'>🔐</div>
        </div>
        <h2>Log In</h2>
        <p style='color: #94a3b8; margin-bottom: 15px;'>Access your existing account</p>
        <div style='display: flex; flex-direction: column; gap: 8px; margin-top: 15px; text-align: left; width: 100%;'>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Load saved projects
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Access history
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Team collaboration
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Animated button with moving text
    login_button = st.button("🔐 **Login Now** 🔐", 
                            key="login_btn", 
                            use_container_width=True,
                            type="primary")
    
    if login_button:
        st.switch_page("pages/2_🔐_Log_In.py")

with col3:
    st.markdown("""
    <div class='option-card'>
        <div class="icon-container">
            <div class='moving-icon guest'>👤</div>
        </div>
        <div class='badge'>FREE</div>
        <h2>Guest Access</h2>
        <p style='color: #94a3b8; margin-bottom: 15px;'>Try basic features immediately</p>
        <div style='display: flex; flex-direction: column; gap: 8px; margin-top: 15px; text-align: left; width: 100%;'>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Quick visualization
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px;'>✅</span> Basic charts
            </div>
            <div style='display: flex; align-items: center; font-size: 12px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.05);'>
                <span style='margin-right: 8px; font-size: 14px; color: #ef4444;'>⚠️</span> Data not saved
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Animated button with moving text
    guest_button = st.button("👤 **Try as Guest** 👤", 
                            key="guest_btn", 
                            use_container_width=True,
                            type="secondary")
    
    if guest_button:
        st.session_state.guest_mode = True
        st.session_state.logged_in = True
        st.session_state.username = "Guest User"
        st.switch_page("pages/3_🏠_Home.py")

# Add CSS for button animations
st.markdown("""
<style>
    /* Apply animations to all buttons */
    div[data-testid="stButton"] > button {
        animation: buttonPulse 2s infinite, buttonBounce 1s infinite alternate !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        animation: none !important;
        transform: translateY(-8px) scale(1.05) !important;
        box-shadow: 0 15px 30px rgba(250, 204, 21, 0.3) !important;
    }
    
    /* Specific button colors */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6) !important;
        border: none !important;
    }
    
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(45deg, #f59e0b, #d97706) !important;
        border: none !important;
        color: white !important;
    }
    
    /* Add moving text effect */
    @keyframes textMove {
        0% { letter-spacing: 0px; }
        50% { letter-spacing: 1px; }
        100% { letter-spacing: 0px; }
    }
    
    div[data-testid="stButton"] > button span {
        display: inline-block;
        animation: textMove 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Benefits comparison with animations
st.markdown("""
<div style="background: #0f172a; padding: 2rem; border-radius: 15px; margin-top: 2rem; border-left: 5px solid #10b981; animation: slideIn 1s ease-out;">
    <h3 style="text-align: center; color: #FACC15; margin-bottom: 1.5rem;">🎯 Why Create an Account?</h3>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
        <div style="padding: 1rem; border-radius: 10px; background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; animation: float 4s ease-in-out infinite;">
            <h4 style="color: #3b82f6; display: flex; align-items: center; gap: 10px;">🔄 <span>Save & Resume</span></h4>
            <p style="color: #94a3b8;">Your work is automatically saved. Come back anytime to continue where you left off.</p>
        </div>
        <div style="padding: 1rem; border-radius: 10px; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; animation: float 4s ease-in-out infinite 0.5s;">
            <h4 style="color: #10b981; display: flex; align-items: center; gap: 10px;">📤 <span>Export & Share</span></h4>
            <p style="color: #94a3b8;">Export visualizations as PNG, PDF, or interactive HTML files. Share with your team.</p>
        </div>
        <div style="padding: 1rem; border-radius: 10px; background: rgba(139, 92, 246, 0.1); border: 1px solid #8b5cf6; animation: float 4s ease-in-out infinite 1s;">
            <h4 style="color: #8b5cf6; display: flex; align-items: center; gap: 10px;">📊 <span>Advanced Analytics</span></h4>
            <p style="color: #94a3b8;">Access predictive analytics, machine learning models, and custom algorithms.</p>
        </div>
        <div style="padding: 1rem; border-radius: 10px; background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; animation: float 4s ease-in-out infinite 1.5s;">
            <h4 style="color: #f59e0b; display: flex; align-items: center; gap: 10px;">👥 <span>Collaboration</span></h4>
            <p style="color: #94a3b8;">Work with team members, share dashboards, and collaborate in real-time.</p>
        </div>
    </div>
</div>

<style>
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes warningPulse {
        0% { border-left-color: #f59e0b; box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
        70% { border-left-color: #d97706; box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
        100% { border-left-color: #f59e0b; box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="margin-top: 3rem; border: 1px solid #334155;">
<div style="text-align: center; color: #64748b; padding: 1rem; animation: fadeIn 2s;">
    <p>Developed by Muhammad Zarq Ali • v2.0 • 
    <a href="https://linkedin.com/in/engeenior" target="_blank" style="color: #64748b; text-decoration: none; animation: linkGlow 3s infinite;">LinkedIn</a> • 
    <a href="https://github.com/engeenior" target="_blank" style="color: #64748b; text-decoration: none; animation: linkGlow 3s infinite 0.5s;">GitHub</a> • 
    <a href="tel:+923313267202" style="color: #64748b; text-decoration: none; animation: linkGlow 3s infinite 1s;">Contact</a></p>
</div>

<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes linkGlow {
        0%, 100% { color: #64748b; text-shadow: none; }
        50% { color: #FACC15; text-shadow: 0 0 10px rgba(250, 204, 21, 0.3); }
    }
</style>
""", unsafe_allow_html=True)