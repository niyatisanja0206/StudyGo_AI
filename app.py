# app.py
import streamlit as st
from auth_ui import show_auth_ui
from auth import logout, delete_user
from utils import load_css
from timetable import timetable_page, display_saved_timetables
from chat import chat_interface

# Set app configuration
st.set_page_config(page_title="StudyGo AI", layout="wide", page_icon="🎓")
load_css()

# Show login/signup + welcome if not authenticated
if "user_id" not in st.session_state and "is_guest" not in st.session_state:
    with st.sidebar:
        show_auth_ui()

    # Main window welcome content
    st.title("🎓 StudyGo AI")
    
    st.markdown('''
    <div class="welcome-section">
        <h2>Welcome to StudyGo AI</h2>
        <p>Your AI-powered assistant to build efficient and personalized learning experiences</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        <div class="welcome-section">
            <h3 style="color: inherit;">✨ What you can do with LearnMate AI</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(0, 123, 255, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #007bff;">
                        <p style="margin: 0;"><strong>📚 Smart Timetables:</strong><br>Create structured, efficient learning schedules from any topic list.</p>
                    </div>
                    <div style="background: rgba(40, 167, 69, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #28a745;">
                        <p style="margin: 0;"><strong>🧠 Intelligent Learning:</strong><br>Topics are prioritized by complexity and your available time.</p>
                    </div>
                    <div style="background: rgba(255, 193, 7, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #ffc107;">
                        <p style="margin: 0;"><strong>🗓️ Flexible Planning:</strong><br>Plan your studies by day and hour with total control.</p>
                    </div>
                    <div style="background: rgba(108, 117, 125, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #6c757d;">
                        <p style="margin: 0;"><strong>💾 Save & Track:</strong><br>Store your timetables and revisit them anytime.</p>
                    </div>
                    <div style="background: rgba(23, 162, 184, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #17a2b8;">
                        <p style="margin: 0;"><strong>🔍 AI Chat Assistant:</strong><br>Ask concept questions or for custom study advice on the go.</p>
                    </div>
                    <div style="background: rgba(220, 53, 69, 0.05); padding: 1rem; border-radius: 8px; border-left: 3px solid #dc3545;">
                        <p style="margin: 0;"><strong>🌐 Real-time Search:</strong><br>Get up-to-date content suggestions for deep learning.</p>
                    </div>
                </div>
        </div>

    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="info-card">
        <h4>👉 Getting Started</h4>
        <p>Use the sidebar to <strong>Log In</strong>, <strong>Sign Up</strong>, or continue as <strong>Guest</strong> to start your learning journey!</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.stop()

# 🎓 If logged in or guest, show main app
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.get('username', 'Guest')}**")
    
    # Logout button with professional styling
    st.markdown('<div class="danger-button">', unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Account deletion for registered users
    if not st.session_state.get("is_guest", False):
        st.markdown("---")
        st.markdown("**⚠️ Account Management**")
        st.markdown('<div class="danger-button">', unsafe_allow_html=True)
        if st.button("❌ Delete Account", use_container_width=True):
            if st.session_state.get("user_id"):
                delete_user(st.session_state["user_id"])
                logout()
                st.success("Account deleted successfully.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    tool = st.radio("🛠️ Choose a tool", ["📅 Timetable Generator", "🗨️ Chat Assistant"], key="tool_selector")

# 🔧 Main tool view
st.title("🎓 StudyGo AI")
st.markdown("Your personalized learning assistant for any course, subject, or technology.")

if tool == "📅 Timetable Generator":
    display_saved_timetables()
    st.markdown("---")
    timetable_page()
elif tool == "🗨️ Chat Assistant":
    chat_interface()